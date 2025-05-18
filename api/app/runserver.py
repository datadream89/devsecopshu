import pdfplumber
import fitz  # PyMuPDF
import re
import json
from collections import defaultdict

QUOTE_PAIRS = [
    ('"', '"'), ('“', '”'), ('„', '“'), ('«', '»'), ('‹', '›'), ('‟', '”'),
    ('❝', '❞'), ('〝', '〞'), ('＂', '＂')
]

section_pattern = re.compile(
    r"^(?P<section>(\d+(\.\d+)*|[a-zA-Z]|\([a-zA-Z0-9]+\))\.)\s+(?P<rest>.+)")

# Extract formatted text for titles using fitz
def get_formatted_titles(pdf_path):
    doc = fitz.open(pdf_path)
    formatted = defaultdict(dict)
    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")['blocks']
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span.get("text", "").strip()
                    if not text:
                        continue
                    flags = span.get("flags", 0)
                    is_bold = flags & 2
                    is_underline = flags & 4
                    if is_bold or is_underline:
                        formatted[page_num][text] = True
    return formatted

def extract_title(text):
    for open_q, close_q in QUOTE_PAIRS:
        pattern = re.escape(open_q) + r'(.+?)' + re.escape(close_q)
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip(), text.replace(match.group(0), '').strip()
    return None, text

def build_hierarchy(pdf_path):
    formatted_titles = get_formatted_titles(pdf_path)
    hierarchy = {}
    current_path = []
    current_node = hierarchy
    node_stack = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            lines = page.extract_text().split("\n")
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                match = section_pattern.match(line)
                if match:
                    section_id = match.group("section")
                    rest = match.group("rest").strip()
                    title, remaining = extract_title(rest)
                    if not title:
                        for txt in formatted_titles.get(page_num, {}):
                            if txt in rest:
                                title = txt
                                remaining = rest.replace(txt, '').strip()
                                break

                    section_parts = section_id.strip('.').split('.')
                    current = hierarchy
                    for part in section_parts:
                        if part not in current:
                            current[part] = {
                                "section": part,
                                "title": title if title else None,
                                "paragraph": "",
                                "page": [page_num],
                                "children": {}
                            }
                        else:
                            if page_num not in current[part]["page"]:
                                current[part]["page"].append(page_num)
                        current = current[part]["children"]

                    current_path = section_parts
                    node_stack = [hierarchy[p] if i == 0 else node_stack[-1]["children"][p]
                                  for i, p in enumerate(section_parts)]

                    if remaining:
                        node_stack[-1]["paragraph"] += remaining + " "
                elif node_stack:
                    node_stack[-1]["paragraph"] += line + " "

    return hierarchy

def flatten_hierarchy(hierarchy):
    flat = []
    def recurse(node, parent_topic=None):
        for key in sorted(node.keys(), key=lambda x: [int(s) if s.isdigit() else s for s in x.split('.')]):
            entry = node[key]
            flat.append({
                "section": entry["section"],
                "title": entry.get("title"),
                "topic": parent_topic,
                "paragraph": entry.get("paragraph", "").strip(),
                "page": entry["page"][0] if entry["page"] else None
            })
            recurse(entry["children"], parent_topic=entry.get("title") or parent_topic)
    recurse(hierarchy)
    return flat

def save_to_json(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    pdf_path = "your_file.pdf"  # Replace with actual path
    hierarchy = build_hierarchy(pdf_path)
    flat = flatten_hierarchy(hierarchy)

    save_to_json(flat, "flat_sections.json")
    print("Extracted", len(flat), "sections.")
