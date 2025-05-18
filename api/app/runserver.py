import re
from docx import Document
import json

def starts_with_number_prefix_and_bold_underlined(para):
    text = para.text
    # Match number prefix like '1.' or '1' followed by whitespace(s)
    prefix_match = re.match(r'^\s*(\d+\.?)\s+', text)
    if not prefix_match:
        return False

    prefix_end = prefix_match.end()  # index after number prefix + spaces
    pos = 0
    for run in para.runs:
        run_text = run.text
        run_len = len(run_text)
        run_start = pos
        run_end = pos + run_len
        pos = run_end

        # Only consider runs *after* prefix ends
        if run_end <= prefix_end:
            continue
        if run.bold and run.underline and run_text.strip():
            return True
    return False

def extract_docx_hierarchy(doc_path):
    doc = Document(doc_path)
    hierarchy = []

    current_section = {"heading": None, "subsections": []}
    current_subsection = {"subheading": None, "content": []}

    def append_subsection():
        if current_subsection["subheading"] or current_subsection["content"]:
            current_section["subsections"].append(current_subsection.copy())
            current_subsection["content"].clear()

    def append_section():
        append_subsection()
        if current_section["heading"] or current_section["subsections"]:
            hierarchy.append(current_section.copy())
            current_section["subsections"].clear()

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        alignment = para.paragraph_format.alignment  # 1=center
        is_bold = any(run.bold for run in para.runs if run.text.strip())

        # Section detection: center-aligned and bold
        if alignment == 1 and is_bold:
            append_section()
            current_section["heading"] = text
            current_subsection = {"subheading": None, "content": []}
            continue

        # Subheading detection: number prefix + bold & underlined after prefix
        if starts_with_number_prefix_and_bold_underlined(para):
            append_subsection()
            current_subsection = {"subheading": text, "content": []}
            continue

        # Else add paragraph or bullet depending on style
        if para.style.name and "List" in para.style.name:
            text_type = "bullet"
        else:
            text_type = "paragraph"

        current_subsection["content"].append({"type": text_type, "text": text})

    append_section()

    # Insert tables immediately after last content of current subsection or section
    for table in doc.tables:
        table_data = []
        for row in table.rows:
            row_data = [cell.text.strip() for cell in row.cells]
            table_data.append(row_data)

        # Add to last subsection if exists, else to last section
        if hierarchy:
            if hierarchy[-1]["subsections"]:
                hierarchy[-1]["subsections"][-1]["content"].append({"type": "table", "data": table_data})
            else:
                # No subsections, create one with no heading
                hierarchy[-1]["subsections"].append({
                    "subheading": None,
                    "content": [{"type": "table", "data": table_data}]
                })
        else:
            # Empty document case
            hierarchy.append({
                "heading": None,
                "subsections": [{
                    "subheading": None,
                    "content": [{"type": "table", "data": table_data}]
                }]
            })

    return hierarchy

if __name__ == "__main__":
    docx_path = "your_doc.docx"  # Change to your file path
    result = extract_docx_hierarchy(docx_path)

    with open("output_hierarchy.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    import pprint
    pprint.pprint(result)
