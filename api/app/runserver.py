import pdfplumber
import fitz  # PyMuPDF
import re
import json

QUOTE_PAIRS = [
    ('"', '"'), ('“', '”'), ('„', '“'), ('«', '»'), ('‹', '›'), ('‟', '”'),
    ('❝', '❞'), ('〝', '〞'), ('＂', '＂')
]

section_header_re = re.compile(
    r"""^\s*
    (?P<header>
        (?:\d+(?:\.\d+)*\.)     # e.g. 1. or 1.1. or 2.6.4.
        | [a-zA-Z]\.                # e.g. a. or B.
        | \([a-zA-Z0-9]+\)         # e.g. (a), (1)
    )
    \s*
    (?P<rest>.*)?$
    """, re.VERBOSE
)

def extract_title_and_rest(line, styles):
    for quote_open, quote_close in QUOTE_PAIRS:
        quote_match = re.search(re.escape(quote_open) + r"(.+?)" + re.escape(quote_close), line)
        if quote_match:
            return quote_match.group(1).strip(), line.replace(quote_match.group(0), '').strip()

    for word, style in styles:
        if 'bold' in style or 'underline' in style:
            if line.startswith(word):
                return word.strip(), line.replace(word, '', 1).strip()

    return None, line

def split_section_numbers(header):
    h = header.rstrip('.')
    if header.startswith('(') and header.endswith(')'):
        return [header]
    if re.match(r"^[a-zA-Z]\.$", header):
        return [header]
    return h.split('.')

def is_top_level_section(header):
    return bool(re.match(r"^\d+\.$", header))

def insert_section(root, section_numbers, section_data):
    current = root
    for i, part in enumerate(section_numbers):
        if "children" not in current:
            current["children"] = {}

        key = part if i != 0 else f"{part}_page_{section_data['page'][0]}"

        if key not in current["children"]:
            current["children"][key] = {
                "section_header": part + ('.' if not part.endswith('.') else ''),
                "paragraph": "",
                "page": [],
            }
        current = current["children"][key]

        if i == len(section_numbers) - 1:
            for k, v in section_data.items():
                if k == "paragraph":
                    current[k] += (v + "\n")
                elif k == "page":
                    current[k] = list(sorted(set(current.get(k, []) + v)))
                else:
                    current[k] = v

def flatten_tree(node):
    def helper(node):
        res = {}
        page_list = node.get("page", [])
        res["page"] = page_list[0] if isinstance(page_list, list) and page_list else None
        for k in ("section_header", "title", "topic", "paragraph"):
            if k in node:
                res[k] = node[k].strip() if isinstance(node[k], str) else node[k]
        if "children" in node:
            res["children"] = [helper(child) for _, child in sorted(
                node["children"].items(), key=lambda x: (x[1].get("page", [float('inf')])[0], x[0]))]
        return res
    return helper(node)

def extract_sections(pdf_path):
    root = {"section_header": "root", "paragraph": "", "children": {}}
    current_section_numbers = None
    current_section_data = {}
    buffer = []

    def flush():
        nonlocal current_section_numbers, current_section_data, buffer
        if current_section_numbers:
            current_section_data["paragraph"] = "\n".join(buffer).strip()
            insert_section(root, current_section_numbers, current_section_data)
        buffer = []
        current_section_numbers = None
        current_section_data = {}

    with pdfplumber.open(pdf_path) as pdf:
        doc = fitz.open(pdf_path)
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            lines = text.split("\n")
            styles = [(span['text'], span) for span in doc[page_num - 1].get_text("dict")["blocks"] for line in span.get("lines", []) for span in line.get("spans", [])]
            for line in lines:
                line = line.strip()
                match = section_header_re.match(line)
                if match:
                    flush()
                    header = match.group("header").strip()
                    rest_of_line = match.group("rest") or ""
                    title, remainder = extract_title_and_rest(rest_of_line, styles)
                    current_section_numbers = split_section_numbers(header)
                    current_section_data = {
                        "page": [page_num],
                        "section_header": header
                    }
                    if title:
                        if is_top_level_section(header):
                            current_section_data["topic"] = title
                        else:
                            current_section_data["title"] = title
                    if remainder:
                        buffer.append(remainder)
                else:
                    if current_section_numbers:
                        buffer.append(line)
            # if no new section found, carry over the page
            if current_section_numbers:
                current_section_data["page"].append(page_num)

        flush()

    return flatten_tree(root)

def save_to_json(data, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# --- Main ---
if __name__ == "__main__":
    pdf_path = "sample.pdf"  # Your PDF path
    output_path = "section_hierarchy.json"
    nested_data = extract_sections(pdf_path)
    save_to_json(nested_data, output_path)
