import re
import json
from docx import Document
import fitz  # PyMuPDF

# --- Step 1: Extract docx content with default types ---
def extract_docx_to_json(doc_path):
    doc = Document(doc_path)
    content = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        ctype = "bullet" if para.style.name and "List" in para.style.name else "paragraph"
        content.append({
            "text": text,
            "type": ctype,
            "prefix": None
        })

    for table in doc.tables:
        table_data = []
        for row in table.rows:
            table_data.append([cell.text.strip() for cell in row.cells])
        content.append({
            "type": "table",
            "data": table_data
        })

    return content

# --- Step 2: Detect prefixes and update types ---
def extract_pdf_text(pdf_path):
    doc = fitz.open(pdf_path)
    return "\n".join(page.get_text() for page in doc)

def detect_prefix(text):
    patterns = [
        (r"^\s*(\d+\.\d+)(\.)?\s+", "numeric_subsection"),
        (r"^\s*(\d+)(\.)?\s+", "numeric_section"),
        (r"^\s*(\(?[a-zA-Z]\)?)(\.)?\s+", "alpha_subsection"),
        (r"^\s*(\(?[ivxlcdmIVXLCDM]+\)?)(\.)?\s+", "roman_subsection"),
    ]
    for pat, ptype in patterns:
        match = re.match(pat, text)
        if match:
            return ptype, match.group(1).strip()
    return None, None

def update_types_by_pdf(json_data, pdf_text):
    for entry in json_data:
        if entry["type"] not in ("paragraph", "bullet"):
            continue
        para_text = entry["text"]
        if not para_text:
            continue

        escaped_text = re.escape(para_text)
        pattern = re.compile(r"(\S{1,10})\s+" + escaped_text, re.IGNORECASE)
        match = pattern.search(pdf_text)

        if match:
            candidate_prefix = match.group(1)
            prefix_type, prefix_val = detect_prefix(candidate_prefix + " ")
            if prefix_type:
                entry["type"] = prefix_type
                entry["prefix"] = prefix_val

    return json_data

# --- Usage ---
if __name__ == "__main__":
    docx_path = "your_file.docx"  # Replace with your .docx path
    pdf_path = "your_file.pdf"    # Replace with your .pdf path

    intermediate_json = extract_docx_to_json(docx_path)

    with open("intermediate.json", "w", encoding="utf-8") as f:
        json.dump(intermediate_json, f, indent=2, ensure_ascii=False)

    pdf_text = extract_pdf_text(pdf_path)
    final_json = update_types_by_pdf(intermediate_json, pdf_text)

    with open("final_output.json", "w", encoding="utf-8") as f:
        json.dump(final_json, f, indent=2, ensure_ascii=False)
