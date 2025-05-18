import re
import json
from docx import Document

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

    def classify_with_prefix(text):
        patterns = {
            "numeric section":    r"^\s*(\d+\.?)\s+",
            "numeric subsection": r"^\s*(\d+\.\d+\.?)\s+",
            "alpha subsection":   r"^\s*[(]?([a-zA-Z])[).]?\s+",
            "roman subsection":   r"^\s*[(]?((?i)ix|iv|v?i{0,3}|x)[).]?\s+",
        }
        for label, pattern in patterns.items():
            match = re.match(pattern, text)
            if match:
                return label, match.group(1)
        return None, None

    def add_content(text, base_type):
        full_type, prefix = classify_with_prefix(text)
        ctype = full_type if full_type else base_type
        content_entry = {"type": ctype, "text": text}
        if prefix:
            content_entry["prefix"] = prefix

        if current_subsection is not None:
            current_subsection["content"].append(content_entry)
        elif current_section is not None:
            current_section["content"].append(content_entry)
        else:
            hierarchy.append({"heading": None, "content": [content_entry]})

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

        base_type = "bullet" if is_bullet(para) else "paragraph"
        add_content(text, base_type)

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

# --- Usage ---
if __name__ == "__main__":
    docx_path = "your_file.docx"  # Replace with your Word file path
    result = extract_docx_structure(docx_path)

    with open("docx_structure.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
