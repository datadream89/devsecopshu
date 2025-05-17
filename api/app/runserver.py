import pdfplumber
import fitz  # PyMuPDF
import re
import json
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction
from langchain.vectorstores import Chroma

QUOTE_PAIRS = [
    ('"', '"'), ('“', '”'), ('„', '“'), ('«', '»'), ('‹', '›'), ('‟', '”'),
    ('❝', '❞'), ('〝', '〞'), ('＂', '＂')
]

section_header_re = re.compile(
    r"""^\s*
    (?P<header>
        (?:\d+(?:\.\d+)*\.)     # e.g. 1. or 1.1. or 2.6.4.
        | [a-zA-Z]\.            # e.g. a. or B.
        | \([a-zA-Z0-9]+\)      # e.g. (a), (1)
    )
    \s*
    (?P<rest>.*)?$
    """, re.VERBOSE
)

def is_top_level_section(header):
    return bool(re.match(r"^\d+\.$", header))

def split_section_numbers(header):
    h = header.rstrip('.')
    if header.startswith('(') and header.endswith(')'):
        return [header]
    if re.match(r"^[a-zA-Z]\.$", header):
        return [header]
    return h.split('.')

def extract_title_and_rest(text):
    text = text.strip()
    title = None
    remainder = text

    for open_q, close_q in QUOTE_PAIRS:
        pattern = re.escape(open_q) + r'(.+?)' + re.escape(close_q)
        match = re.search(pattern, text)
        if match:
            title = match.group(1).strip()
            remainder = text.replace(match.group(0), '').strip()
            return title, remainder

    if text and (text.isupper() or (text.istitle() and len(text.split()) <= 6)):
        return text, ""

    return None, remainder

def extract_styles_from_fitz_page(page):
    """
    Extract lines from PyMuPDF page with info about bold/underline.
    Returns list of dicts: {'text': line_text, 'bold': bool, 'underline': bool}
    """
    lines = []
    blocks = page.get_text("dict")["blocks"]
    for block in blocks:
        if block["type"] != 0:
            continue  # Skip non-text blocks
        for line in block["lines"]:
            line_text = ""
            bold = False
            underline = False
            for span in line["spans"]:
                line_text += span["text"]
                # Detect bold by fontname or flags
                fontname = span.get("font", "").lower()
                if "bold" in fontname or "black" in fontname:
                    bold = True
                # Detect underline by flags (4 means underline)
                if span.get("flags", 0) & 4:
                    underline = True
            lines.append({"text": line_text.strip(), "bold": bold, "underline": underline})
    return lines

def insert_section(root, section_numbers, section_data):
    current = root
    for i, part in enumerate(section_numbers):
        if "children" not in current:
            current["children"] = {}

        key = part if i != 0 else f"{part}_page_{section_data['page']}"

        if key not in current["children"]:
            current["children"][key] = {
                "section_header": part + ('.' if not part.endswith('.') else ''),
                "paragraph": "",
            }
        current = current["children"][key]

        if i == len(section_numbers) - 1:
            for k, v in section_data.items():
                if k == "paragraph":
                    current[k] += (v + "\n")
                else:
                    current[k] = v

def flatten_tree(node):
    def helper(node):
        res = {}
        for k in ("page", "section_header", "topic", "section_title", "paragraph"):
            if k in node:
                res[k] = node[k].strip() if isinstance(node[k], str) else node[k]
        if "children" in node:
            res["children"] = [helper(child) for key, child in sorted(node["children"].items())]
        return res
    return helper(node)

def extract_sections(pdf_path):
    root = {"section_header": "root", "paragraph": "", "children": {}}
    current_section_numbers = None
    current_section_data = {}
    buffer = []

    # Open pdfs for both pdfplumber and PyMuPDF
    pdf_p = pdfplumber.open(pdf_path)
    pdf_fitz = fitz.open(pdf_path)

    def flush():
        nonlocal current_section_numbers, current_section_data, buffer
        if current_section_numbers:
            current_section_data["paragraph"] = "\n".join(buffer).strip()
            insert_section(root, current_section_numbers, current_section_data)
        buffer = []
        current_section_numbers = None
        current_section_data = {}

    total_pages = len(pdf_p.pages)
    for page_num in range(1, total_pages + 1):
        page_p = pdf_p.pages[page_num - 1]
        page_f = pdf_fitz.load_page(page_num - 1)

        # Get styles info for this page lines
        styled_lines = extract_styles_from_fitz_page(page_f)

        # Extract raw text lines from pdfplumber
        text = page_p.extract_text() or ""
        lines = text.split("\n")

        # Map each text line to its style info (bold, underline)
        # We rely on order of lines here, so be careful if mismatch
        for idx, line in enumerate(lines):
            line_text = line.strip()
            style_info = styled_lines[idx] if idx < len(styled_lines) else {"bold": False, "underline": False, "text": ""}
            match = section_header_re.match(line_text)
            if match:
                # Flush existing section buffer before starting new section
                flush()
                header = match.group("header").strip()
                rest_of_line = match.group("rest") or ""

                current_section_numbers = split_section_numbers(header)
                current_section_data = {
                    "page": page_num,
                    "section_header": header
                }

                # Check if rest_of_line contains bold or underlined title, else check styled lines
                title, rest = extract_title_and_rest(rest_of_line)

                # If title missing in rest_of_line, try to detect if line after section header is bold/underline
                # Sometimes the title is in the styled line (which is same as line_text here)
                if not title and (style_info["bold"] or style_info["underline"]):
                    title = line_text[len(header):].strip()
                    rest = ""

                # If still no title, check next line for bold/underline if exists and append
                elif not title and idx + 1 < len(lines):
                    next_line_text = lines[idx + 1].strip()
                    next_style = styled_lines[idx + 1] if idx + 1 < len(styled_lines) else {"bold": False, "underline": False}
                    if next_style["bold"] or next_style["underline"]:
                        title = next_line_text
                        # Skip next line from paragraph by incrementing idx — handled by not appending next line to buffer
                        # We'll do that by adding a flag to skip below (see next)

                        # We'll set a flag so next line is skipped from paragraph buffer
                        # Implemented outside for loop is simpler: just skip adding next line to buffer this iteration

                # Assign title as topic or section_title depending on header level
                if title:
                    if is_top_level_section(header):
                        current_section_data["topic"] = title
                    else:
                        current_section_data["section_title"] = title

                if rest:
                    buffer.append(rest)
                continue  # Start next line after flush and section start

            # If no new section header, append line to buffer (current section)
            if current_section_numbers:
                buffer.append(line_text)

        # End of page, do NOT flush yet — because next page may continue this section

    # After last page, flush remaining buffered section
    flush()

    pdf_p.close()
    pdf_fitz.close()

    return flatten_tree(root)

def generate_chunks(node, parent_metadata=None):
    chunks = []
    parent_metadata = parent_metadata or {}

    metadata = parent_metadata.copy()
    for key in ("page", "section_title", "topic"):
        if key in node:
            metadata[key] = node[key]

    paragraph = node.get("paragraph", "").strip()
    if paragraph:
        chunks.append({
            "data": paragraph,
            "metadata": metadata
        })

    for child in node.get("children", []):
        chunks.extend(generate_chunks(child, metadata))

    return chunks

def save_to_json(data, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ---------- Main Program ----------

