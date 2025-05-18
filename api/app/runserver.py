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

    def is_subsection(para):
        text = para.text.strip()
        match = re.match(r'^(\d+(\.)?)\s+(.*)', text)
        if not match:
            return False
        _, _, title = match.groups()

        for run in para.runs:
            run_text = run.text.strip()
            if run_text and title.startswith(run_text):
                if run.bold and run.underline:
                    return True
        return False

    def is_bold_underlined(para):
        for run in para.runs:
            if run.text.strip() and run.bold and run.underline:
                return True
        return False

    def get_indent_level(para):
        # Indentation is in inches, where 720 = 0.5 inch
        indent = para.paragraph_format.left_indent
        if indent is None:
            return 0
        points = indent.pt if hasattr(indent, 'pt') else indent / 12700 * 72
        if points > 20:
            return 2
        elif points > 0:
            return 1
        return 0

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        alignment = para.paragraph_format.alignment  # 1 = center
        is_bold = any(run.bold for run in para.runs if run.text.strip())

        # --- Detect Section ---
        if alignment == 1 and is_bold:
            append_section()
            current_section["heading"] = text
            current_subsection = {"subheading": None, "content": []}
            continue

        # --- Detect Subsection ---
        if is_subsection(para):
            append_subsection()
            current_subsection = {"subheading": text, "content": []}
            continue

        # --- Detect Type ---
        indent_level = get_indent_level(para)
        if para.style.name and "List" in para.style.name:
            if is_bold_underlined(para):
                text_type = "heading"
            elif indent_level == 1:
                text_type = "level 1"
            elif indent_level >= 2:
                text_type = "level 2"
            else:
                text_type = "bullet"
        else:
            if indent_level == 1:
                text_type = "level 1"
            elif indent_level >= 2:
                text_type = "level 2"
            else:
                text_type = "paragraph"

        current_subsection["content"].append({"type": text_type, "text": text})

    append_section()

    # --- Extract Tables ---
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

# --- Example usage ---
if __name__ == "__main__":
    docx_path = "your_file.docx"  # Replace with your actual DOCX file path
    result = extract_docx_hierarchy(docx_path)

    with open("docx_hierarchy.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    import pprint
    pprint.pprint(result)
