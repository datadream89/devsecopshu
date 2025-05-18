import re
from docx import Document
import json

def extract_docx_hierarchy(doc_path):
    doc = Document(doc_path)
    hierarchy = []
    current_section = {"heading": None, "subsections": []}
    current_subsection = {"subheading": None, "content": []}

    def append_subsection():
        if current_subsection["subheading"] or current_subsection["content"]:
            current_section["subsections"].append(current_subsection.copy())
            current_subsection["content"] = []

    def append_section():
        append_subsection()
        if current_section["heading"] or current_section["subsections"]:
            hierarchy.append(current_section.copy())
            current_section["subsections"] = []

    for para in doc.paragraphs:
        style = para.style.name
        text = para.text.strip()

        if not text:
            continue

        # Detect bold and underlined
        is_bold = any(run.bold for run in para.runs if run.text.strip())
        is_underlined = any(run.underline for run in para.runs if run.text.strip())

        # Check if it starts with a single digit + "." or space
        if re.match(r'^\d(\.|\s)', text) and is_bold and is_underlined:
            append_subsection()
            current_subsection = {"subheading": text, "content": []}
            continue

        # Check for Heading 1
        if style.startswith('Heading 1'):
            append_section()
            current_section["heading"] = text
            current_section["subsections"] = []
            current_subsection = {"subheading": None, "content": []}

        # Check for Heading 2
        elif style.startswith('Heading 2'):
            append_subsection()
            current_subsection = {"subheading": text, "content": []}

        # Bullet or paragraph
        else:
            if 'List' in style:
                text_type = "bullet"
            else:
                text_type = "paragraph"
            current_subsection["content"].append({"type": text_type, "text": text})

    append_section()

    # Append tables
    for table in doc.tables:
        table_data = []
        for row in table.rows:
            row_data = [cell.text.strip() for cell in row.cells]
            table_data.append(row_data)
        if hierarchy:
            if hierarchy[-1]["subsections"]:
                hierarchy[-1]["subsections"][-1]["content"].append({"type": "table", "data": table_data})
            else:
                hierarchy[-1]["subsections"].append({
                    "subheading": None,
                    "content": [{"type": "table", "data": table_data}]
                })
        else:
            hierarchy.append({
                "heading": None,
                "subsections": [{
                    "subheading": None,
                    "content": [{"type": "table", "data": table_data}]
                }]
            })

    return hierarchy

# Example usage
if __name__ == "__main__":
    docx_path = "your_file.docx"  # Replace with your actual DOCX file path
    result = extract_docx_hierarchy(docx_path)

    with open("docx_hierarchy.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    import pprint
    pprint.pprint(result)
