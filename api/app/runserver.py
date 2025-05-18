import pdfplumber
import fitz  # PyMuPDF
import re
import json
from collections import defaultdict

# Quotation character pairs for international support
QUOTE_PAIRS = [('“', '”'), ('"', '"'), ("'", "'"), ('‘', '’'), ('«', '»')]

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
        (?:\d+(?:\.\d+)*\.?)       # Numbers like 1, 2.1, 3.4.5
        | [ivxlcdmIVXLCDM]+\.?     # Roman numerals
        | [a-zA-Z]\.               # Letters like a.
        | \([a-zA-Z0-9]+\)         # (a), (1)
    )
    \s*
    (?P<rest>.*)?$
    """, re.VERBOSE
)

def is_section_header(text):
    return bool(section_header_re.match(text.strip()))

def split_section_numbers(header):
    if header.startswith('('):
        return [header.strip('()')]
    if re.match(r'[ivxlcdmIVXLCDM]+', header):
        return [header.lower()]
    return header.strip('.').split('.')

def extract_bold_underline_blocks(doc, page_num):
    page = doc.load_page(page_num - 1)
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

def is_bold_underline_or_quoted(line, blocks):
    for block in blocks:
        if line.strip().startswith(block["text"]) and (block["bold"] or block["underline"]):
            return block["text"]
    return extract_quoted(line)

def insert_section(root, section_numbers, section_data):
    node = root
    for sec in section_numbers:
        node = node.setdefault("children", {}).setdefault(sec, {"section_id": sec})
    node.update(section_data)

def sort_children(children):
    def sort_key(item):
        node = item[1]
        page = node.get("page", 9999)
        parts = [int(p) if p.isdigit() else p for p in node.get("section_id", "").split('.')]
        return (page, parts)
    sorted_items = sorted(children.items(), key=sort_key)
    for k, v in sorted_items:
        if "children" in v:
            v["children"] = sort_children(v["children"])
    return [v for k, v in sorted_items]

def flatten_tree(node):
    if "page_list" in node:
        node["page"] = min(node.pop("page_list"))
    if "children" in node:
        node["children"] = sort_children(node["children"])
        for child in node["children"]:
            flatten_tree(child)
    return node

def extract_sections(pdf_path):
    with pdfplumber.open(pdf_path) as pdf, fitz.open(pdf_path) as doc:
        root = {}
        current_section = None
        current_paragraph = ""
        page_count = len(pdf.pages)

        for i, page in enumerate(pdf.pages):
            text_lines = page.extract_text().split('\n') if page.extract_text() else []
            bold_blocks = extract_bold_underline_blocks(doc, i + 1)

            for line in text_lines:
                match = section_header_re.match(line.strip())
                if match:
                    if current_section:
                        current_section["paragraph"] = current_paragraph.strip()
                        insert_section(root, current_section["section_numbers"], current_section)
                    header = match.group("header")
                    rest = match.group("rest").strip() if match.group("rest") else ""
                    section_numbers = split_section_numbers(header)
                    title_candidate = is_bold_underline_or_quoted(rest, bold_blocks)
                    title = title_candidate.strip() if title_candidate else ""
                    topic = title if len(section_numbers) == 1 else None
                    current_section = {
                        "section_id": '.'.join(section_numbers),
                        "section_numbers": section_numbers,
                        "title": title,
                        "topic": topic,
                        "page_list": [i + 1],
                    }
                    current_paragraph = rest if rest and not title else ""
                elif current_section:
                    if line.strip():
                        current_paragraph += " " + line.strip()
                        if (i + 1) not in current_section["page_list"]:
                            current_section["page_list"].append(i + 1)

        if current_section:
            current_section["paragraph"] = current_paragraph.strip()
            insert_section(root, current_section["section_numbers"], current_section)

        nested_sorted = sort_children(root.get("children", {}))
        return json.dumps({"children": [flatten_tree(child) for child in nested_sorted]}, indent=2)

# Example usage
if __name__ == "__main__":
    pdf_path = "your_pdf_with_sections.pdf"
    json_output = extract_sections(pdf_path)
    with open("section_hierarchy.json", "w") as f:
        f.write(json_output)
