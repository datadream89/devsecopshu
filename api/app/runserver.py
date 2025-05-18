import re
import json
from docx import Document
import fitz  # PyMuPDF for PDF reading

def extract_docx_structure(doc_path):
    doc = Document(doc_path)
    hierarchy = []
    current_section = None
    current_subsection = None

    def is_section(para):
        return para.paragraph_format.alignment == 1 and any(run.bold for run in para.runs if run.text.strip())

    def is_subsection(para):
        text = para.text.strip()
        # Check if starts with number + optional dot + whitespace + rest
        match = re.match(r"^\d+(\.)?\s+", text)
        if not match:
            return False
        # Check if any run with bold+underline matches the title start
        title = text[match.end():].strip()
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

    # Attach tables inline at the last known position
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


def extract_pdf_text(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text


def detect_prefix_type(text, pdf_text):
    # Patterns with optional leading whitespace (for matching start of text)
    patterns = {
        "numeric_section": r"^\s*(\d+(\.)?)\s+",
        "numeric_subsection": r"^\s*((\d+\.)+\d+(\.)?)\s+",
        "alpha_subsection": r"^\s*((\(?[a-zA-Z]\)?)(\.|\s))\s*",
        "roman_subsection": r"^\s*((\(?[ivxlcdmIVXLCDM]+\)?)(\.|\s))\s*",
    }

    # We want to check numeric_subsection first (like 1.1 or 2.3.1), then numeric_section (1. or 1)
    # Because numeric_subsection pattern can match numeric_section as well
    check_order = ["numeric_subsection", "numeric_section", "alpha_subsection", "roman_subsection"]

    for key in check_order:
        regex = re.compile(patterns[key], re.IGNORECASE)
        m = regex.match(text)
        if m:
            prefix = m.group(1)
            # Check if prefix exists in pdf_text (ignore whitespace differences)
            # Normalize spaces for matching
            prefix_norm = re.sub(r"\s+", "", prefix.lower())
            pdf_text_norm = re.sub(r"\s+", "", pdf_text.lower())
            if prefix_norm in pdf_text_norm:
                return key, prefix
    return None, None


def classify_types(hierarchy, pdf_text):
    def classify_content_list(content_list):
        for c in content_list:
            if c["type"] in ["paragraph", "bullet"]:
                ctype, prefix = detect_prefix_type(c["text"], pdf_text)
                if ctype:
                    c["type"] = ctype
                    c["prefix"] = prefix
            # Tables and others remain as is

    for section in hierarchy:
        # Check heading and subheading for prefix
        ctype, prefix = detect_prefix_type(section["heading"], pdf_text) if section["heading"] else (None, None)
        if ctype == "numeric_section":
            section["type"] = ctype
            section["prefix"] = prefix
        else:
            section["type"] = "section"

        for subsection in section.get("subsections", []):
            ctype, prefix = detect_prefix_type(subsection["subheading"], pdf_text) if subsection["subheading"] else (None, None)
            if ctype == "numeric_subsection":
                subsection["type"] = ctype
                subsection["prefix"] = prefix
            else:
                subsection["type"] = "subsection"

            classify_content_list(subsection.get("content", []))

        classify_content_list(section.get("content", []))

    return hierarchy


if __name__ == "__main__":
    docx_path = "sample.docx"  # Your Word doc file path
    pdf_path = "sample.pdf"    # Your PDF file path

    # Extract structure from Word
    hierarchy = extract_docx_structure(docx_path)

    # Extract full text from PDF
    pdf_text = extract_pdf_text(pdf_path)

    # Classify paragraphs, bullets, headings based on PDF prefixes
    classified_hierarchy = classify_types(hierarchy, pdf_text)

    # Output to JSON
    with open("structured_output.json", "w", encoding="utf-8") as f:
        json.dump(classified_hierarchy, f, indent=2, ensure_ascii=False)
