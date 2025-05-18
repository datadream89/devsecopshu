import pdfplumber
import fitz  # PyMuPDF
import re
import json
from collections import defaultdict

QUOTE_PAIRS = [
    ('"', '"'), ('“', '”'), ('„', '“'), ('«', '»'), ('‹', '›'), ('‟', '”'),
    ('❝', '❞'), ('〝', '〞'), ('＂', '＂')
]

section_header_re = re.compile(
    r"""^\s*
    (?P<header>
        (?:\d+(?:\.\d+)*\.)     # e.g. 1. or 1.1. or 2.6.4.
        | [a-zA-Z]\.
        | \([a-zA-Z0-9]+\)
    )
    \s*
    (?P<rest>.*)?$
    """, re.VERBOSE
)

def extract_title(rest, styles):
    rest = rest.strip()
    for open_q, close_q in QUOTE_PAIRS:
        pattern = re.escape(open_q) + r'(.*?)' + re.escape(close_q)
        match = re.search(pattern, rest)
        if match:
            return match.group(1).strip(), rest.replace(match.group(0), '').strip()

    for style in styles:
        if style.get("text") and (style.get("is_bold") or style.get("is_underlined")):
            if rest.startswith(style["text"]):
                return style["text"].strip(), rest.replace(style["text"], '').strip()

    return None, rest

def extract_text_styles(page):
    styles = []
    blocks = page.get_text("dict")["blocks"]
    for b in blocks:
        for l in b.get("lines", []):
            for s in l.get("spans", []):
                styles.append({
                    "text": s.get("text", "").strip(),
                    "is_bold": "bold" in s.get("font", "").lower(),
                    "is_underlined": s.get("underline", 0) == 1
                })
    return styles

def insert_section(root, parts, section_data):
    node = root
    for i, part in enumerate(parts):
        key = part if i != 0 else f"{part}_p{section_data['page'][0]}"
        if "children" not in node:
            node["children"] = {}
        if key not in node["children"]:
            node["children"][key] = {"section_id": part, "paragraph": "", "page": []}
        node = node["children"][key]
        if i == len(parts) - 1:
            node["paragraph"] += section_data["paragraph"] + "\n"
            node["page"].extend(section_data["page"])
            if "title" in section_data:
                node["title"] = section_data["title"]


def flatten(node, parent_title=None):
    out = []
    this_node = {
        "section": node.get("section_id", ""),
        "page": node.get("page", [])[0] if node.get("page") else None,
        "title": node.get("title", ""),
        "paragraph": node.get("paragraph", "").strip(),
        "topic": parent_title if parent_title else node.get("title", "")
    }
    out.append(this_node)
    for k, child in sorted_children(node.get("children", {})):
        out.extend(flatten(child, parent_title=node.get("title", "")))
    return out

def sorted_children(children):
    def sort_key(item):
        node = item[1]
        page = node.get("page", [9999])[0]
        parts = node.get("section_id", "").split('.')
        sortable_parts = tuple(f"{int(p):04}" if p.isdigit() else p.lower() for p in parts)
        return (page, sortable_parts)
    return sorted(children.items(), key=sort_key)

def process_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    plumber = pdfplumber.open(pdf_path)
    root = {}
    current_parts = None
    current_section = {"paragraph": "", "page": []}

    for i, page in enumerate(doc):
        styles = extract_text_styles(page)
        text = plumber.pages[i].extract_text() or ""
        lines = text.split("\n")

        for line in lines:
            match = section_header_re.match(line.strip())
            if match:
                if current_parts:
                    insert_section(root, current_parts, current_section)
                header = match.group("header")
                rest = match.group("rest") or ""
                parts = header.rstrip('.').split('.')
                title, remaining = extract_title(rest, styles)
                current_parts = parts
                current_section = {
                    "page": [i + 1],
                    "paragraph": remaining,
                }
                if title:
                    current_section["title"] = title
            else:
                if current_parts:
                    current_section["paragraph"] += " " + line.strip()
                    if (i + 1) not in current_section["page"]:
                        current_section["page"].append(i + 1)

    if current_parts:
        insert_section(root, current_parts, current_section)

    return flatten(root)

def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    file_path = "sample.pdf"  # Replace with your PDF file path
    output_path = "output.json"
    structured_data = process_pdf(file_path)
    save_json(structured_data, output_path)
    print(f"Extracted and saved {len(structured_data)} sections to {output_path}.")
