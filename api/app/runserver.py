import pdfplumber
import re
import json

# Matches numbered headers like 1., 1.1., 2.3.4 or lettered (a), (i), A., etc.
section_header_re = re.compile(r"""
    ^\s*
    (?P<number>
        (?:\d+(?:\.\d+)*\.)        # 1. or 1.1. or 2.4.5.
        | [a-zA-Z]\.               # A., b.
        | \([a-zA-Z0-9]+\)         # (a), (1), (i)
    )
    (?P<title>.*)                 # The rest of the line is the title
""", re.VERBOSE)

def split_section_number(header):
    if header.startswith("("):
        return [header]
    return header.strip(".").split(".")

def insert_nested_section(root, number_parts, title, page):
    node = root
    for i, part in enumerate(number_parts):
        if "children" not in node:
            node["children"] = {}
        if part not in node["children"]:
            node["children"][part] = {"title": "", "children": {}}
        node = node["children"][part]
    node["title"] = title.strip()
    node["page"] = page

def flatten_tree(node):
    result = []
    for key, val in sorted(node.get("children", {}).items(), key=lambda x: x[0]):
        item = {
            "section": key,
            "title": val.get("title", ""),
            "page": val.get("page", ""),
        }
        children = flatten_tree(val)
        if children:
            item["children"] = children
        result.append(item)
    return result

def extract_outline(pdf_path):
    root = {"children": {}}

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if not text:
                continue
            for line in text.split("\n"):
                match = section_header_re.match(line.strip())
                if match:
                    number = match.group("number").strip()
                    title = match.group("title").strip()
                    number_parts = split_section_number(number)
                    insert_nested_section(root, number_parts, title, page_num)

    return flatten_tree(root)

# Example usage
pdf_path = "your_file.pdf"
outline = extract_outline(pdf_path)

# Save to JSON
with open("section_hierarchy.json", "w", encoding="utf-8") as f:
    json.dump(outline, f, indent=2, ensure_ascii=False)
