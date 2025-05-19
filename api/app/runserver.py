import json
from docx import Document

def parse_docx_with_formatting(doc_path):
    doc = Document(doc_path)
    output = []

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        first_run = next((run for run in para.runs if run.text.strip()), None)
        is_bold = first_run.bold if first_run else False
        is_underline = first_run.underline if first_run else False
        alignment = para.paragraph_format.alignment

        if alignment == 1 and is_bold:
            para_type = "topic"
        elif is_bold and is_underline:
            para_type = "header"
        elif is_underline and not is_bold:
            para_type = "subsection"
        else:
            para_type = "paragraph" if "List" not in para.style.name else "bullet"

        output.append({
            "type": para_type,
            "text": text
        })

    # Add tables in-place
    for i, table in enumerate(doc.tables):
        table_data = []
        for row in table.rows:
            table_data.append([cell.text.strip() for cell in row.cells])
        output.append({"type": "table", "data": table_data})

    return output

# --- Usage ---
if __name__ == "__main__":
    docx_path = "your_file.docx"  # Replace with your file path
    data = parse_docx_with_formatting(docx_path)

    with open("intermediate_output.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
