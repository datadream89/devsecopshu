import re
import json
from docx import Document


def extract_docx_hierarchy(doc_path):
    doc = Document(doc_path)
    hierarchy = []
    current_section = {"heading": None, "subsections": []}
    current_subsection = {"subheading": None, "content": []}

    indent_stack = [0]  # base indent level

    def get_effective_indent(para):
        left = para.paragraph_format.left_indent or 0
        first = para.paragraph_format.first_line_indent or 0
        return (left + first).pt if (left or first) else 0

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

    def detect_prefix_type(text):
        if re.match(r"^\(?[ivxlcdmIVXLCDM]+\)?[.\s]", text):
            return "roman subsection"
        elif re.match(r"^\(?[a-zA-Z]\)?[.\s]", text):
            return "alpha subsection"
        elif re.match(r"^\d+\.\d+", text):
            return "numeric subsection"
        return None

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        alignment = para.paragraph_format.alignment  # 1 = center
        is_bold = any(run.bold for run in para.runs if run.text.strip())
        current_indent = get_effective_indent(para)

        while indent_stack and current_indent < indent_stack[-1]:
            indent_stack.pop()
        if not indent_stack or current_indent > indent_stack[-1]:
            indent_stack.append(current_indent)
        indent_level = len(indent_stack) - 1

        # Detect Section
        if alignment == 1 and is_bold:
            append_section()
            current_section["heading"] = text
            current_subsection = {"subheading": None, "content": []}
            continue

        # Detect Subsection
        if is_subsection(para):
            append_subsection()
            current_subsection = {"subheading": text, "content": []}
            continue

        # Detect content type
        if para.style.name and "List" in para.style.name:
            if is_bold_underlined(para):
                text_type = "heading"
            else:
                text_type = "bullet"
        else:
            text_type = "paragraph"

        # Tag special prefix types
        prefix_type = detect_prefix_type(text)
        if prefix_type:
            text_type = prefix_type

        current_subsection["content"].append({
            "type": text_type,
            "text": text,
            "indent": indent_level
        })

    append_section()

    # Extract Tables inline
    table_index = 0
    for block in doc.element.body:
        if block.tag.endswith('}tbl'):
            tbl = doc.tables[table_index]
            table_index += 1
            table_data = []
            for row in tbl.rows:
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


# Usage
if __name__ == "__main__":
    docx_path = "your_file.docx"  # Replace with your actual .docx file
    result = extract_docx_hierarchy(docx_path)

    with open("docx_hierarchy.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    import pprint
    pprint.pprint(result)
