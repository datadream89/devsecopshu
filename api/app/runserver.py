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
        | [a-zA-Z]\.               # e.g. a. or B.
        | \([a-zA-Z0-9]+\)        # e.g. (a), (1)
    )
    \s*
    (?P<rest>.*)?$
    """, re.VERBOSE
)

def extract_bold_underline_quoted_titles(pdf_path):
    doc = fitz.open(pdf_path)
    title_map = defaultdict(list)  # {page_num: [(section_id, title)]}
    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                line_text = " ".join(span["text"] for span in line["spans"])
                match = section_header_re.match(line_text.strip())
                if not match:
                    continue

                header = match.group("header")
                rest = match.group("rest") or ""

                title = None
                for span in line["spans"]:
                    text = span["text"].strip()
                    if not text:
                        continue
                    is_bold = span.get("flags", 0) & 2
                    is_underline = "underline" in span.get("font", "").lower()
                    if is_bold or is_underline:
                        title = text
                        break

                if not title:
                    for open_q, close_q in QUOTE_PAIRS:
                        q_match = re.search(re.escape(open_q) + r"(.+?)" + re.escape(close_q), rest)
                        if q_match:
                            title = q_match.group(1).strip()
                            break

                if title:
                    title_map[page_num].append((header, title))
    return title_map

def extract_hierarchy(pdf_path, title_map):
    hierarchy = {"children": []}
    node_stack = {}

    sections = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            lines = (page.extract_text() or "").split("\n")
            for line in lines:
                match = section_header_re.match(line.strip())
                if match:
                    header = match.group("header").strip()
                    level = header.count('.') + 1 if '.' in header else 2 if header.isalpha() else 3
                    title = None
                    for h, t in title_map.get(page_num, []):
                        if h == header:
                            title = t
                            break
                    sections.append({"level": level, "section": header, "title": title, "page": page_num})

    # Build hierarchy
    for item in sorted(sections, key=lambda x: (x["page"], x["section"])):
        level = item["level"]
        node = {"section": item["section"], "title": item["title"], "page": item["page"], "children": []}

        if level == 1:
            hierarchy["children"].append(node)
        else:
            parent = node_stack.get(level - 1)
            if parent:
                parent["children"].append(node)
            else:
                hierarchy["children"].append(node)

        node_stack[level] = node

    return hierarchy

def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    pdf_path = "sample.pdf"  # Replace with your PDF file path
    output_path = "hierarchy.json"

    title_map = extract_bold_underline_quoted_titles(pdf_path)
    hierarchy = extract_hierarchy(pdf_path, title_map)
    save_json(hierarchy, output_path)
    print("Hierarchy saved to", output_path)
