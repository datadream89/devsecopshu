import pdfplumber
import re
import json
import os
def extract_nested_sections(pdf_path):
    section_pattern = re.compile(
        r"""^\s*
        (?P<section>
            \d+(?:\.\d+)*        # 1, 1.1, 2.3.4
            | [a-zA-Z]           # a, A, b, B
            | \([a-zA-Z0-9]+\)   # (a), (1), (i)
        )
        [\.\):]?\s*              # Optional punctuation after section
        (?P<title>["']?.+?["']?)?  # Optional title
        \s*$""", re.VERBOSE
    )

    root = {}

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
                    # Flush current section text
                    if current_section:
                        flush_buffer(current_section, buffer)

                    section_id = match.group("section").strip("().")
                    title = (match.group("title") or "").strip("\"' ")

                    # Build the path for nesting
                    path_parts = section_id.split(".")
                    current_path = path_parts
                    current_section = insert_into_tree(current_path, title, page_num)
                elif current_section:
                    buffer.append(line)

            # Extract tables for current section
            if current_section:
                tables = page.extract_tables()
                if tables:
                    current_section["tables"].extend(tables)

        # Final flush
        if current_section:
            flush_buffer(current_section, buffer)

    return root


def save_to_json(data, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ========== Example Usage ==========
if __name__ == "__main__":
    pdf_path = "your_file.pdf"  # Replace with your actual file
    output_path = "nested_sections.json"

    result = extract_nested_sections(pdf_path)
    save_to_json(result, output_path)

    print(f"Done! Output saved to {output_path}")
