import re
import json
from docx import Document
import fitz  # PyMuPDF for PDF text extraction

# Regex patterns for prefixes with optional leading whitespace
patterns = {
    "numeric_section": r"^\s*(\d+)(\.)?\s+",
    "numeric_subsection": r"^\s*(\d+\.\d+)(\.)?\s+",
    "alpha_subsection": r"^\s*(\(?[a-zA-Z]\)?)(\.)?\s+",
    "roman_subsection": r"^\s*(\(?[ivxlcdmIVXLCDM]+\)?)(\.)?\s+"
}

def extract_pdf_text(pdf_path):
    """Extract all text from PDF as a single string."""
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text

def find_prefix_in_pdf(paragraph_text, pdf_text):
    """
    Search paragraph_text in pdf_text and extract prefix if any.
    Returns (prefix, cleaned_paragraph_text) or (None, paragraph_text)
    """
    # Escape special regex chars in paragraph text
    escaped_para = re.escape(paragraph_text.strip())
    # Pattern to find prefix before paragraph text
    search_pattern = re.compile(r"(\S{1,10})\s+" + escaped_para, re.IGNORECASE)

    match = search_pattern.search(pdf_text)
    if match:
        possible_prefix = match.group(1)
        # Check if possible_prefix matches any prefix pattern
        for key, pattern in patterns.items():
            if re.fullmatch(pattern.strip("^$"), possible_prefix, re.IGNORECASE):
                return possible_prefix.strip(), paragraph_text.strip()
        # If no prefix pattern matches, maybe prefix is just a number or letter without dot:
        # fallback check:
        if re.match(r"^\(?[ivxlcdmIVXLCDM]+\)?\.?$", possible_prefix):
            return possible_prefix.strip(), paragraph_text.strip()
        if re.match(r"^\(?[a-zA-Z]\)?\.?$", possible_prefix):
            return possible_prefix.strip(), paragraph_text.strip()
        if re.match(r"^\d+\.?$", possible_prefix):
            return possible_prefix.strip(), paragraph_text.strip()
    # No prefix found, return None
    return None, paragraph_text.strip()

def assign_type_by_prefix(prefix):
    """Assign type based on prefix pattern."""
    if prefix is None:
        return None
    prefix = prefix.strip().lower()
    if re.match(r"^\d+(\.)?$", prefix):
        return "numeric_section"
    if re.match(r"^\d+\.\d+(\.)?$", prefix):
        return "numeric_subsection"
    if re.match(r"^\(?[a-z]\)?(\.)?$", prefix):
        return "alpha_subsection"
    if re.match(r"^\(?[ivxlcdm]+\)?(\.)?$", prefix):
        return "roman_subsection"
    return None

def is_bullet(para):
    """Simple check for bullet style."""
    return para.style.name and "List" in para.style.name

def extract_docx_structure(doc_path, pdf_text):
    doc = Document(doc_path)
    hierarchy = []
    current_section = None
    current_subsection = None

    def is_section(para):
        # Center aligned bold text is a section/topic
        alignment = para.paragraph_format.alignment
        return alignment == 1 and any(run.bold for run in para.runs if run.text.strip())

    def is_subsection(para):
        # Bold and underlined text starting with number prefix
        text = para.text.strip()
        for run in para.runs:
            if run.bold and run.underline:
                return True
        return False

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

        # Find prefix from pdf text for this paragraph
        prefix, cleaned_text = find_prefix_in_pdf(text, pdf_text)
        ctype = assign_type_by_prefix(prefix)

        if ctype is None:
            ctype = "bullet" if is_bullet(para) else "paragraph"

        # Use cleaned_text without prefix for content
        add_content(cleaned_text, ctype)

    if current_subsection:
        current_section["subsections"].append(current_subsection)
    if current_section:
        hierarchy.append(current_section)

    # Add tables (optional: can extend to detect prefix here as well)
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
    docx_path = "your_file.docx"  # Change to your Word file path
    pdf_path = "your_file.pdf"    # Change to your PDF file path

    pdf_text = extract_pdf_text(pdf_path)
    result = extract_docx_structure(docx_path, pdf_text)

    with open("docx_pdf_structure.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    import pprint
    pprint.pprint(result)
