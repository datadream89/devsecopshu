import re
import json
from docx import Document
import fitz  # PyMuPDF

# --- Step 1: Extract docx to intermediate JSON ---
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

# --- Step 2: Load all PDF text lines ---
def extract_pdf_lines(pdf_path):
    doc = fitz.open(pdf_path)
    lines = []
    for page in doc:
        page_text = page.get_text().splitlines()
        lines.extend(line.strip() for line in page_text if line.strip())
    return lines

# --- Step 3: Prefix detection ---
def detect_prefix(text):
    patterns = [
        (r"^\s*(\d+\.\d+\.?)\s+", "numeric_subsection"),
        (r"^\s*(\d+\.?)\s+", "numeric_section"),
        (r"^\s*(\(?[a-zA-Z]\)?\.?)\s+", "alpha_subsection"),
        (r"^\s*(\(?[ivxlcdmIVXLCDM]+\)?\.?)\s+", "roman_subsection"),
    ]
    for pat, ptype in patterns:
        match = re.match(pat, text)
        if match:
            return ptype, match.group(1).strip()
    return None, None

# --- Step 4: Match prefixes from PDF lines to JSON entries ---
def update_types_by_prefix(json_data, pdf_lines):
    for entry in json_data:
        if entry["type"] not in ("paragraph", "bullet"):
            continue
        para_text = entry["text"].strip()
        found = False
        for line in pdf_lines:
            if para_text in line:
                prefix_match = re.match(r"^\s*(\S{1,10})\s+", line)
                if prefix_match:
                    candidate_prefix = prefix_match.group(1)
                    prefix_type, prefix_val = detect_prefix(candidate_prefix + " ")
                    if prefix_type:
                        entry["type"] = prefix_type
                        entry["prefix"] = prefix_val
                        found = True
                        break
        if not found:
            entry["prefix"] = None
    return json_data

# --- Usage ---
if __name__ == "__main__":
    docx_path = "your_file.docx"  # Replace with actual file
    pdf_path = "your_file.pdf"    # Replace with actual file

    intermediate_json = extract_docx_to_json(docx_path)
    with open("intermediate.json", "w", encoding="utf-8") as f:
        json.dump(intermediate_json, f, indent=2, ensure_ascii=False)

    pdf_lines = extract_pdf_lines(pdf_path)
    final_json = update_types_by_prefix(intermediate_json, pdf_lines)
    with open("final_output.json", "w", encoding="utf-8") as f:
        json.dump(final_json, f, indent=2, ensure_ascii=False)
