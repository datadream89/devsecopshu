import re
import json
from docx import Document
import fitz  # PyMuPDF

# --- Step 1: Extract structure from DOCX ---
def extract_docx_structure(doc_path):
    doc = Document(doc_path)
    hierarchy = []
    current_section = None
    current_subsection = None

    def is_section(para):
        return para.paragraph_format.alignment == 1 and any(run.bold for run in para.runs if run.text.strip())

    def is_subsection(para):
        text = para.text.strip()
        match = re.match(r"^(\d+(\.)?)\s+(.*)", text)
        if not match:
            return False
        title = match.group(3)
        for run in para.runs:
            if run.text.strip() and title.startswith(run.text.strip()):
                if run.bold and run.underline:
                    return True
        return False

    def is_bullet(para):
        return para.style.name and "List" in para.style.name

    def add_content(text, ctype):
        if current_subsection is not None:
            current_subsection["content"].append({"type": ctype, "text": text})
        elif current_section is not None:
            current_section["content"].append({"type": ctype, "text": text})
        else:
            hierarchy.append({"heading": None, "content": [{"type": ctype, "text": text}]})

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        if is_section(para):
            if current_section:
                if current_subsection:
                    current_section["subsections"].append(current_subsection)
                    current_subsection = None
                hierarchy.append(current_section)
            current_section = {"heading": text, "content": [], "subsections": []}
            current_subsection = None
            continue

        if is_subsection(para):
            if current_subsection:
                current_section["subsections"].append(current_subsection)
            current_subsection = {"subheading": text, "content": []}
            continue

        ctype = "bullet" if is_bullet(para) else "paragraph"
        add_content(text, ctype)

    if current_subsection:
        current_section["subsections"].append(current_subsection)
    if current_section:
        hierarchy.append(current_section)

    # Attach tables
    for table in doc.tables:
        table_data = []
        for row in table.rows:
            table_data.append([cell.text.strip() for cell in row.cells])
        table_entry = {"type": "table", "data": table_data}

        if hierarchy:
            last_section = hierarchy[-1]
            if last_section["subsections"]:
                last_section["subsections"][-1]["content"].append(table_entry)
            else:
                last_section["content"].append(table_entry)
        else:
            hierarchy.append({"heading": None, "content": [table_entry], "subsections": []})

    return hierarchy

# --- Step 2: Classify paragraph types using PDF text ---

def extract_pdf_text(pdf_path):
    doc = fitz.open(pdf_path)
    pdf_text = []
    for page in doc:
        pdf_text.append(page.get_text())
    return "\n".join(pdf_text)

def classify_prefix(text, pdf_text):
    text_escaped = re.escape(text[:50])  # Use a snippet to avoid regex overflow
    patterns = {
        "numeric subsection": rf"\b\d+\.\d+\s+{text_escaped}",
        "alpha subsection": rf"\b([a-zA-Z]|[a-zA-Z]\.|\([a-zA-Z]\))\s+{text_escaped}",
        "roman subsection": rf"\b(i{1,3}|iv|v|vi{1,3}|ix|x|xi{0,3}|xiv|xv|xvi{1,3})\s+{text_escaped}",
    }
    for typ, pattern in patterns.items():
        if re.search(pattern, pdf_text, re.IGNORECASE):
            return typ
    return None

def update_json_with_subtypes(data, pdf_text):
    def update_block(block):
        for item in block.get("content", []):
            if item["type"] in ["paragraph", "bullet"]:
                subtype = classify_prefix(item["text"], pdf_text)
                if subtype:
                    item["type"] = subtype
        for subsection in block.get("subsections", []):
            update_block(subsection)
    for section in data:
        update_block(section)
    return data

# --- Main Execution ---
if __name__ == "__main__":
    docx_path = "your_file.docx"   # Replace with your .docx path
    pdf_path = "your_file.pdf"     # Replace with matching .pdf path

    # Step 1: Extract structure
    result = extract_docx_structure(docx_path)
    with open("docx_structure.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # Step 2: Refine types using PDF
    pdf_text = extract_pdf_text(pdf_path)
    updated_result = update_json_with_subtypes(result, pdf_text)
    with open("updated_structure.json", "w", encoding="utf-8") as f:
        json.dump(updated_result, f, ensure_ascii=False, indent=2)

    # Optional: Print
    import pprint
    pprint.pprint(updated_result)
