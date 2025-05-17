import pdfplumber
import fitz  # PyMuPDF
import re
import json
from collections import defaultdict

# --- Helper functions ---
QUOTE_PAIRS = [('"', '"'), ('“', '”'), ("‘", "’"), ("'", "'")]

def extract_quoted(text):
    for open_q, close_q in QUOTE_PAIRS:
        pattern = re.escape(open_q) + r'(.+?)' + re.escape(close_q)
        match = re.match(pattern, text)
        if match:
            return match.group(1).strip()
    return None

section_header_re = re.compile(
    r"""^\s*
    (?P<header>
        (?:\d+(?:\.\d+)*\.?)     # e.g. 1, 1.1, 2.6.4
        | [ivxlcdmIVXLCDM]+\.?   # roman numerals
        | [a-zA-Z]\.             # letters like a.
        | [a-zA-Z0-9]+       # (a), (i)
    )
    \s*
    (?P<rest>.*)?$
    """, re.VERBOSE
)

def is_section_header(text):
    return section_header_re.match(text.strip())

def split_section_numbers(section_id):
    return re.findall(r'\d+|[a-zA-Z]+|[a-zA-Z0-9]+', section_id)

def extract_bold_underline_blocks(doc, page_num):
    page = doc.load_page(page_num)
    blocks = []
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                blocks.append({
                    "text": span["text"].strip(),
                    "bold": "bold" in span["font"].lower() or span.get("flags", 0) & 2 != 0,
                    "underline": span.get("underline", False),
                })
    return blocks

def get_non_table_pages(pdf_path):
    table_pages = set()
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            if page.find_tables():
                table_pages.add(i + 1)  # 1-based index
    return table_pages

def is_bold_underline_or_quoted(text, bold_underline_blocks):
    quoted = extract_quoted(text)
    if quoted:
        return quoted
    for block in bold_underline_blocks:
        if text.startswith(block["text"]) and (block["bold"] or block["underline"]):
            return block["text"]
    return None

def insert_section(root, section_numbers, section_data):
    current = root
    for num in section_numbers:
        current = current.setdefault("children", {})
        current = current.setdefault(num, {})
    current.update(section_data)

def sort_hierarchy(node):
    if "children" in node:
        children = node["children"]
        sorted_keys = sorted(children.keys(), key=lambda x: [int(s) if s.isdigit() else s for s in re.findall(r'\d+|[a-zA-Z]+', x)])
        node["children"] = {k: children[k] for k in sorted_keys}
        for k in node["children"]:
            sort_hierarchy(node["children"][k])

def flatten_children(node):
    if "children" in node:
        node["children"] = [flatten_children(v) for v in node["children"].values()]
        for child in node["children"]:
            child["page"] = min(child.get("pages", [0]))
            if "pages" in child:
                del child["pages"]
    return node

# --- Main Extraction Function ---
def extract_sections_excluding_table_pages(pdf_path):
    doc = fitz.open(pdf_path)
    table_pages = get_non_table_pages(pdf_path)
    root = {}

    with pdfplumber.open(pdf_path) as pdf:
        current_section_id = None
        current_paragraph = []
        current_title = None
        current_topic = None
        current_pages = []
        
        for i, page in enumerate(pdf.pages):
            page_num = i + 1
            if page_num in table_pages:
                continue  # skip pages with tables

            text_lines = page.extract_text().split("\n") if page.extract_text() else []
            bold_underline_blocks = extract_bold_underline_blocks(doc, i)

            for line in text_lines:
                match = is_section_header(line)
                if match:
                    if current_section_id:
                        insert_section(root, split_section_numbers(current_section_id), {
                            "section_id": current_section_id,
                            "title": current_title,
                            "paragraph": " ".join(current_paragraph).strip(),
                            "pages": current_pages,
                            "topic": current_topic
                        })
                    header = match.group("header")
                    rest = match.group("rest") or ""
                    title_candidate = is_bold_underline_or_quoted(rest, bold_underline_blocks)
                    current_title = title_candidate
                    current_topic = header if '.' not in header and '(' not in header else None
                    current_section_id = header
                    current_paragraph = [rest.replace(title_candidate, "", 1).strip()] if title_candidate else [rest.strip()]
                    current_pages = [page_num]
                else:
                    current_paragraph.append(line.strip())
                    if page_num not in current_pages:
                        current_pages.append(page_num)

        if current_section_id:
            insert_section(root, split_section_numbers(current_section_id), {
                "section_id": current_section_id,
                "title": current_title,
                "paragraph": " ".join(current_paragraph).strip(),
                "pages": current_pages,
                "topic": current_topic
            })

    sort_hierarchy(root)
    flattened = flatten_children(root)
    return flattened["children"] if "children" in flattened else []

# --- Save to JSON ---
def save_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
