import re
from docx import Document
import json

def bullet_is_subheading(para):
    text = para.text.lstrip()
    print(f"Checking paragraph text: '{text}'")

    prefix_match = re.match(r"^(\d+(\.)?)\s*", text)
    if not prefix_match:
        print("No number prefix found.")
        return False

    prefix_len = len(prefix_match.group(0))
    print(f"Number prefix found: '{prefix_match.group(0)}' with length {prefix_len}")

    pos = 0
    for i, run in enumerate(para.runs):
        run_text = run.text or ""
        run_len = len(run_text)
        run_start = pos
        run_end = pos + run_len
        pos = run_end

        print(f"Run {i}: '{run_text}' from {run_start} to {run_end}, bold={run.bold}, underline={run.underline}")

        # Skip runs fully inside prefix (number and spaces)
        if run_end <= prefix_len:
            print(f"Run {i} is within prefix, skipping.")
            continue

        # For runs starting after prefix
        if run_start >= prefix_len:
            if run_text.strip() and run.bold and run.underline:
                print("Found bold and underlined run after prefix - returning True")
                return True

    print("No bold and underlined run found after prefix - returning False")
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

        alignment = para.paragraph_format.alignment  # 1 = center
        is_bold = any(run.bold for run in para.runs if run.text.strip())

        # Detect Section (center aligned and bold)
        if alignment == 1 and is_bold:
            append_section()
            current_section["heading"] = text
            current_subsection = {"subheading": None, "content": []}
            continue

        # Detect Subsection (bullet list items with number prefix + bold & underline)
        if para.style.name and "List" in para.style.name:
            if bullet_is_subheading(para):
                text_type = "subheading"
            elif is_bold_underlined(para):
                text_type = "heading"
            else:
                text_type = "bullet"
        else:
            text_type = "paragraph"

        current_subsection["content"].append({"type": text_type, "text": text})

    append_section()

    # Extract tables and append them under last subsection content if exists
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

if __name__ == "__main__":
    docx_path = "your_file.docx"  # Replace with your file path
    result = extract_docx_hierarchy(docx_path)

    with open("docx_hierarchy.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    import pprint
    pprint.pprint(result)
