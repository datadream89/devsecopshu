import pdfplumber
import re
import json

def extract_nested_sections(pdf_path):
    # Matches numeric (1, 1.2), alphabetic (a, A), and parenthesized (a), (1)
    section_pattern = re.compile(
        r"""^\s*
        (?P<section>
            (?:\d+(?:\.\d+)*)
            | [a-zA-Z]
            | \([a-zA-Z0-9]+\)
        )
        [\.\):]?\s+
        (?P<title>["']?.+?["']?)?
        \s*$""", re.VERBOSE
    )

    root = {}

    def clean_section_id(section_str):
        return section_str.strip().strip("().")

    def get_path(section_id):
        if "." in section_id:
            return section_id.split(".")
        else:
            return [section_id]

    def insert_into_tree(path, title, page):
        node = root
        for i, part in enumerate(path):
            if part not in node:
                node[part] = {
                    "section_title": "" if i < len(path) - 1 else title,
                    "pages": [],
                    "paragraphs": [],
                    "tables": [],
                    "subsections": {}
                }
            node[part]["pages"] = sorted(set(node[part]["pages"] + [page]))
            if i < len(path) - 1:
                node = node[part]["subsections"]
        return node[path[-1]]

    def flush_buffer(section_node, buffer):
        if buffer:
            text = "\n".join(buffer).strip()
            paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
            section_node["paragraphs"].extend(paragraphs)
            buffer.clear()

    with pdfplumber.open(pdf_path) as pdf:
        current_path = []
        current_section = None
        buffer = []

        for page_num, page in enumerate(pdf.pages, start=1):
            lines = (page.extract_text() or "").split("\n")
            for line in lines:
                match = section_pattern.match(line.strip())
                if match:
                    # Flush previous section
                    if current_section:
                        flush_buffer(current_section, buffer)

                    raw_id = match.group("section")
                    section_id = clean_section_id(raw_id)
                    title = (match.group("title") or "").strip("\"' ")

                    path = get_path(section_id)
                    current_path = path
                    current_section = insert_
