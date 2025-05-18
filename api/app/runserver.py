import re
from docx import Document
import json

def get_text_after_number_prefix(text):
    # Matches number prefix optionally with '.' or ')' or whitespace, then captures rest of text
    m = re.match(r'^(\d+[\.\)]?\s+)(.*)', text)
    if m:
        return m.group(2).strip()
    return text.strip()

def get_indent_points_for_text(para, text_after_prefix):
    left_indent = para.paragraph_format.left_indent.pt if para.paragraph_format.left_indent else 0
    first_line_indent = para.paragraph_format.first_line_indent.pt if para.paragraph_format.first_line_indent else 0

    # Count leading spaces and tabs in text_after_prefix
    leading_ws = len(text_after_prefix) - len(text_after_prefix.lstrip(' \t'))
    tab_count = text_after_prefix.count('\t')

    # Approximate: tab = 12pt, 4 spaces = 12pt
    indent_points = left_indent + first_line_indent + (tab_count * 12) + (leading_ws / 4) * 12
    return indent_points

def get_indent_level(para, prev_indent_points=None, max_level=10):
    text = para.text.strip()
    text_after_prefix = get_text_after_number_prefix(text)
    indent_points = get_indent_points_for_text(para, text_after_prefix)

    # Basic indent level calculation: 12pt ~ 1 level
    level = int(indent_points // 12)

    # Optional smoothing with previous paragraph indent points to avoid jitter
    if prev_indent_points is not None:
        if indent_points > prev_indent_points + 6:
            level = min(level, max_level)
        elif indent_points < prev_indent_points - 6:
            level = max(level - 1, 0)

    return min(level, max_level), indent_points

def is_subsection(para):
    text = para.text.strip()
    # Only subsections start with a number + optional '.' + whitespace and bold+underline
    match = re.match(r'^(\d+[\.\)]?)\s+', text)
    if not match:
        return False

    # Check if the first run containing the title part is bold and underlined
    # (Simplify: if any run that overlaps with the title is bold and underlined)
    for run in para.runs:
        if run.text.strip() and run.bold and run.underline:
            return True
    return False

def is_bold_underlined(para):
    for run in para.runs:
        if run.text.strip() and run.bold and run.underline:
            return True
    return False

def extract_docx_hierarchy(doc_path):
    doc = Document(doc_path)
    hierarchy = []
    current_section = {"heading": None, "subsections": []}
    current_subsection = {"subheading": None, "content": []}
    prev_indent_points = None

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
        text = para.text.strip()
        if not text:
            continue

        alignment = para.paragraph_format.alignment  # 1 means centered
        is_bold = any(run.bold for run in para.runs if run.text.strip())

        # Detect Section (center aligned + bold)
        if alignment == 1 and is_bold:
            append_section()
            current_section["heading"] = text
            current_subsection = {"subheading": None, "content": []}
            prev_indent_points = None
            continue

        # Detect Subsection (starts with number + '.' + whitespace + bold+underline)
        if is_subsection(para):
            append_subsection()
            current_subsection = {"subheading": text, "content": []}
            prev_indent_points = None
            continue

        # Determine content type: bullet or paragraph or heading
        if para.style.name and "List" in para.style.name:
            if is_bold_underlined(para):
                text_type = "heading"
            else:
                text_type = "bullet"
        else:
            if is_bold_underlined(para):
                text_type = "heading"
            else:
                text_type = "paragraph"

        # Calculate indent level ignoring prefix indentation
        indent_level, prev_indent_points = get_indent_level(para, prev_indent_points)

        current_subsection["content"].append({
            "type": text_type,
            "text": text,
            "indent_level": indent_level
        })

    append_section()

    # Add tables immediately after last content element of last subsection of last section
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

# --- Usage example ---
if __name__ == "__main__":
    docx_path = "your_file.docx"  # Replace with your docx path
    result = extract_docx_hierarchy(docx_path)

    with open("docx_hierarchy_with_indent.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    import pprint
    pprint.pprint(result)
