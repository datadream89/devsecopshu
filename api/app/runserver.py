import re
import json
from docx import Document
import fitz  # PyMuPDF

def extract_docx_structure(doc_path):
    doc = Document(doc_path)
    hierarchy = []
    current_section = None
    current_subsection = None

    def is_section(para):
        return para.paragraph_format.alignment == 1 and any(run.bold for run in para.runs if run.text.strip())

    def is_subsection(para):
        text = para.text.strip()
        # Bold + underline check without prefix assumption
        for run in para.runs:
            if run.bold and run.underline and run.text.strip():
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
    # Regex patterns for prefixes at start, optional leading spaces allowed
    patterns = {
        "numeric_section": r"^\s*(\d+(\.)?)\s+",
        "numeric_subsection": r"^\s*((\d+\.)+\d+(\.)?)\s+",
        "alpha_subsection": r"^\s*((\(?[a-zA-Z]\)?)(\.|\s))\s*",
        "roman_subsection": r"^\s*((\(?[ivxlcdmIVXLCDM]+\)?)(\.|\s))\s*",
    }

    check_order = ["numeric_subsection", "numeric_section", "alpha_subsection", "roman_subsection"]

    for key in check_order:
        regex = re.compile(patterns[key], re.IGNORECASE)
        m = regex.match(text)
        if m:
            prefix = m.group(1)
            # Verify prefix exists in PDF text ignoring spaces/case
            prefix_norm = re.sub(r"\s+", "", prefix.lower())
            pdf_text_norm = re.sub(r"\s+", "", pdf_text.lower())
            if prefix_norm in pdf_text_norm:
                return key, prefix
    return None, None


def add_prefix_from_pdf(hierarchy, pdf_text):
    def classify_content_list(content_list):
        for c in content_list:
            # Only attempt if type is paragraph or bullet and prefix not present
            if c["type"] in ["paragraph", "bullet"] and "prefix" not in c:
                ctype, prefix = detect_prefix_type(c["text"], pdf_text)
                if ctype:
                    c["type"] = ctype
                    c["prefix"] = prefix

    for section in hierarchy:
        # Only add prefix if heading has no prefix yet
        if section.get("heading") and "prefix" not in section:
            ctype, prefix = detect_prefix_type(section["heading"], pdf_text)
            if ctype == "numeric_section":
                section["type"] = ctype
                section["prefix"] = prefix
            else:
                section["type"] = "section"
        else:
            section.setdefault("type", "section")

        for subsection in section.get("subsections", []):
            if subsection.get("subheading") and "prefix" not in subsection:
                ctype, prefix = detect_prefix_type(subsection["subheading"], pdf_text)
                if ctype == "numeric_subsection":
                    subsection["type"] = ctype
                    subsection["prefix"] = prefix
                else:
                    subsection["type"] = "subsection"
            else:
                subsection.setdefault("type", "subsection")

            classify_content_list(subsection.get("content", []))

        classify_content_list(section.get("content", []))

    return hierarchy


if __name__ == "__main__":
    docx_path = "sample.docx"  # Your Word document path
    pdf_path = "sample.pdf"    # Your PDF document path

    hierarchy = extract_docx_structure(docx_path)
    pdf_text = extract_pdf_text(pdf_path)
    updated_hierarchy = add_prefix_from_pdf(hierarchy, pdf_text)

    with open("structured_output.json", "w", encoding="utf-8") as f:
        json.dump(updated_hierarchy, f, indent=2, ensure_ascii=False)
