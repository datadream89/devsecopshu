import json
import re
from docx import Document

def extract_docx_structure(doc_path):
    doc = Document(doc_path)
    structure = []
    current_block = None

    def get_run_styles(run):
        return {
            "text": run.text,
            "bold": run.bold,
            "underline": run.underline,
        }

    def classify_paragraph(para):
        text = para.text.strip()
        if not text:
            return None, None

        alignment = para.paragraph_format.alignment  # 0-left, 1-center, 2-right, 3-justify

        runs = para.runs
        if alignment == 1 and any(run.bold for run in runs):
            return "topic", text

        # Check if text starts with bold+underline or underline only
        match = re.match(r"^([\s\S]*?)\b", text)
        if match:
            first_word = match.group(1)
            for run in runs:
                if run.text and first_word.startswith(run.text.strip()):
                    if run.bold and run.underline:
                        return "heading", text
                    elif run.underline and not run.bold:
                        return "subheading", text
                    break

        if para.style.name and "List" in para.style.name:
            return "bullet", text

        return "paragraph", text

    for para in doc.paragraphs:
        ptype, text = classify_paragraph(para)
        if not ptype:
            continue

        if ptype == "subheading":
            underline_part = ""
            non_underline_part = ""
            for run in para.runs:
                if run.underline and not run.bold:
                    underline_part += run.text
                else:
                    non_underline_part += run.text
            block = {
                "type": "subheading",
                "subheading": underline_part.strip(),
                "content": [{"type": "paragraph", "text": non_underline_part.strip()}] if non_underline_part.strip() else []
            }
            structure.append(block)
        else:
            block = {
                "type": ptype,
                "text": text
            }
            structure.append(block)

    # Append tables in place
    table_index = 0
    for i, tbl in enumerate(doc.tables):
        data = []
        for row in tbl.rows:
            row_data = [cell.text.strip() for cell in row.cells]
            data.append(row_data)

        # Insert table after the last paragraph before the table
        insert_index = len(structure)
        structure.insert(insert_index, {
            "type": "table",
            "data": data
        })
        table_index += 1

    return structure

# Usage
if __name__ == "__main__":
    docx_path = "your_file.docx"  # Replace with your DOCX file path
    output = extract_docx_structure(docx_path)
    with open("docx_parsed_output.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
