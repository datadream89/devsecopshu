import fitz  # PyMuPDF
import pdfplumber
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

def extract_title_from_line(text):
    text = text.strip()
    for open_q, close_q in QUOTE_PAIRS:
        pattern = re.escape(open_q) + r'(.*?)' + re.escape(close_q)
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
    return None

def extract_structure(pdf_path):
    doc = fitz.open(pdf_path)
    structure = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")['blocks']

        for block in blocks:
            if 'lines' not in block:
                continue
            line_text = " ".join(span['text'] for line in block['lines'] for span in line['spans']).strip()
            match = section_header_re.match(line_text)
            if not match:
                continue

            header = match.group("header").strip()
            rest = match.group("rest") or ""
            title = None
            found = False

            for line in block['lines']:
                for span in line['spans']:
                    text = span['text'].strip()
                    if text in rest:
                        if span.get("flags", 0) in (2, 20, 22, 4) or span.get("underline", False):
                            title = text
                            found = True
                            break
                if found:
                    break

            if not title:
                title = extract_title_from_line(rest)

            structure.append({
                "section": header,
                "title": title or "",
                "page": page_num + 1
            })

    return structure

def nest_structure(structure):
    root = []
    index = {}

    for item in sorted(structure, key=lambda x: (x['page'], x['section'])):
        parts = re.split(r'\.|\(|\)', item['section'].strip('.'))
        parts = [p for p in parts if p and p != ' ']

        current = root
        for i, part in enumerate(parts):
            key = '.'.join(parts[:i+1])
            if key not in index:
                node = {
                    "section": key,
                    "page": item['page'],
                    "title": item['title'] if i == len(parts)-1 else "",
                    "children": []
                }
                index[key] = node
                current.append(node)
            current = index[key]["children"]

    return root

if __name__ == "__main__":
    pdf_path = "sample_with_sections_and_tables.pdf"  # Change to your file
    structure = extract_structure(pdf_path)
    nested = nest_structure(structure)

    with open("section_hierarchy_nested.json", "w") as f:
        json.dump(nested, f, indent=2)

    print("Hierarchy extraction complete.")
