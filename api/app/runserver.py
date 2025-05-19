import json
from docx import Document

def parse_docx_with_formatting(doc_path):
    doc = Document(doc_path)
    output = []

    # Helper to classify paragraph type
    def classify_para(para):
        text = para.text.strip()
        if not text:
            return None

        first_run = next((run for run in para.runs if run.text.strip()), None)
        is_bold = first_run.bold if first_run else False
        is_underline = first_run.underline if first_run else False
        alignment = para.paragraph_format.alignment

        if alignment == 1 and is_bold:  # Centered + bold
            return "topic"
        elif is_bold and is_underline:
            return "header"
        elif is_underline and not is_bold:
            return "subsection"
        else:
            return "paragraph" if "List" not in para.style.name else "bullet"

    body = doc.element.body
    paragraphs = {p._p: p for p in doc.paragraphs}
    tables = {t._tbl: t for t in doc.tables}

    for child in body.iterchildren():
        if child.tag.endswith('p'):  # Paragraph
            para = paragraphs.get(child)
            if para:
                ptype = classify_para(para)
                if ptype:
                    output.append({
                        "type": ptype,
                        "text": para.text.strip()
                    })
        elif child.tag.endswith('tbl'):  # Table
            table = tables.get(child)
            if table:
                data = []
                for row in table.rows:
                    data.append([cell.text.strip() for cell in row.cells])
                output.append({
                    "type": "table",
                    "data": data
                })

    return output

# --- Usage ---
if __name__ == "__main__":
    docx_path = "your_file.docx"  # Replace with your file path
    data = parse_docx_with_formatting(docx_path)

    with open("intermediate_output.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
