import re
from docx import Document
import json

def get_indent_level_by_whitespace(para):
    raw_text = para.text
    cleaned = re.sub(r"^\(?[a-zA-Z0-9]+\)?\.?\s*", "", raw_text)
    leading_ws = len(raw_text) - len(raw_text.lstrip(' \t'))
    tab_count = raw_text.count('\t')
    indent_score = (tab_count * 4) + (leading_ws // 4)
    return indent_score

def get_indent_from_numbering(text):
    match = re.match(r'^(\d+(\.\d+)+)', text)
    if match:
        return match.group(1).count('.')
    return 0

def best_indent_level(para):
    text = para.text.strip()
    level1 = get_indent_from_numbering(text)
    level2 = get_indent_level_by_whitespace(para)
    return max(level1, level2)

def is_subsection(para):
    text = para.text.strip()
    match = re.match(r'^(\d+\.?\s+)(.*)', text)
    if not match:
        return False
    _, title = match.groups()
    for run in para.runs:
        run_text = run.text.strip()
        if run_text and title.startswith(run_text):
            if run.bold and run.underline:
                return True
    return False

def detect_subtype(text):
    if re.match(r"^\(?[aA]\)?[.\s]", text):
        return "alpha subsection"
    if re.match(r"^\(?[ivxlcdmIVXLCDM]+\)?[.\s]", text):
        return "roman subsection"
    if re.match(r"^\d+\.\d+", text):
        return "numeric subsection"
    return None

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

    def is_bold_underlined(para):
        for run in para.runs:
            if run.text.strip() and run.bold and run.underline:
                return True
        return False

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        alignment = para.paragraph_format.alignment  # 1 = center
        is_bold = any(run.bold for run in para.runs if run.text.strip())
        indent_level = best_indent_level(para)

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

        # --- Determine Content Type ---
        if para.style.name and "List" in para.style.name:
            if is_bold_underlined(para):
                text_type = "heading"
            else:
                text_type = "bullet"
        else:
            text_type = "paragraph"

        # Override type if prefix pattern matches
        subtype = detect_subtype(text)
        if subtype:
            text_type = subtype

        current_subsection["content"].append({
            "type": text_type,
            "text": text,
            "indent_level": indent_level
        })

    append_section()

    # --- Extract Tables and attach in sequence ---
    for table in doc.tables:
        table_data = []
        for row in table.rows:
            row_data = [cell.text.strip() for cell in row.cells]
            table_data.append(row_data)

        if hierarchy:
            if hierarchy[-1]["subsections"]:
                hierarchy[-1]["subsections"][-1]["content"].append({
                    "type": "table",
                    "data": table_data
                })
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

# --- Usage ---
if __name__ == "__main__":
    docx_path = "your_file.docx"  # Replace with actual path
    result = extract_docx_hierarchy(docx_path)

    with open("docx_hierarchy.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    import pprint
    pprint.pprint(result)
