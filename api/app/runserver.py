import re
from docx import Document

def get_indent_level(para, max_level=10):
    indent = para.paragraph_format.left_indent
    first_line_indent = para.paragraph_format.first_line_indent

    indent_points = 0
    if indent:
        indent_points += indent.pt if hasattr(indent, 'pt') else 0
    if first_line_indent:
        indent_points += first_line_indent.pt if hasattr(first_line_indent, 'pt') else 0

    # Count tab characters as additional indent steps (each tab = ~12pt)
    tab_count = para.text.count('\t')
    indent_points += tab_count * 12

    level = int(indent_points // 12)
    return min(level, max_level)

def extract_docx_hierarchy_with_indent(doc_path):
    doc = Document(doc_path)
    hierarchy = []
    current_section = {"heading": None, "indent_level": 0, "subsections": []}
    current_subsection = {"subheading": None, "indent_level": 0, "content": []}

    def append_subsection():
        if current_subsection["subheading"] or current_subsection["content"]:
            current_section["subsections"].append(current_subsection.copy())
            current_subsection["content"] = []

    def append_section():
        append_subsection()
        if current_section["heading"] or current_section["subsections"]:
            hierarchy.append(current_section.copy())
            current_section["subsections"] = []

    def is_bold_underlined(para):
        for run in para.runs:
            if run.text.strip() and run.bold and run.underline:
                return True
        return False

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        level = get_indent_level(para)
        alignment = para.paragraph_format.alignment  # 1 = center
        is_bold = any(run.bold for run in para.runs if run.text.strip())

        # Detect Section (center aligned and bold)
        if alignment == 1 and is_bold:
            append_section()
            current_section["heading"] = text
            current_section["indent_level"] = level
            current_subsection = {"subheading": None, "indent_level": 0, "content": []}
            continue

        # Detect Subsection (bold and underlined)
        if is_bold_underlined(para):
            append_subsection()
            current_subsection = {"subheading": text, "indent_level": level, "content": []}
            continue

        # Determine content type (bullet or paragraph)
        if para.style.name and "List" in para.style.name:
            text_type = "bullet"
        else:
            text_type = "paragraph"

        current_subsection["content"].append({
            "type": text_type,
            "text": text,
            "indent_level": level
        })

    append_section()

    # Attach tables to the last subsection content with indent_level 0
    for table in doc.tables:
        table_data = []
        for row in table.rows:
            row_data = [cell.text.strip() for cell in row.cells]
            table_data.append(row_data)
        if hierarchy:
            if hierarchy[-1]["subsections"]:
                hierarchy[-1]["subsections"][-1]["content"].append({
                    "type": "table",
                    "data": table_data,
                    "indent_level": 0
                })
            else:
                hierarchy[-1]["subsections"].append({
                    "subheading": None,
                    "indent_level": 0,
                    "content": [{"type": "table", "data": table_data, "indent_level": 0}]
                })
        else:
            hierarchy.append({
                "heading": None,
                "indent_level": 0,
                "subsections": [{
                    "subheading": None,
                    "indent_level": 0,
                    "content": [{"type": "table", "data": table_data, "indent_level": 0}]
                }]
            })

    return hierarchy

# --- Usage example ---
if __name__ == "__main__":
    docx_path = "your_file.docx"  # Replace with your .docx file path
    result = extract_docx_hierarchy_with_indent(docx_path)

    import json
    with open("docx_hierarchy_with_indent.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    import pprint
    pprint.pprint(result)
