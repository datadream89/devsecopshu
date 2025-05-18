import re
import json
from docx import Document
from PyPDF2 import PdfReader

def get_prefix_type(text):
    stripped = text.strip()
    # Match prefix at start, allow optional parentheses and trailing dot or whitespace
    match = re.match(r'^\s*(\(?[ivxlcdm]+\)?|\(?[a-zA-Z]\)?|\d+(\.\d+)*)(?=[\s\.])', stripped, re.IGNORECASE)
    if not match:
        return None, None
    prefix = match.group(1).strip()
    # Determine type by prefix pattern
    if re.match(r'^\(?[ivxlcdm]+\)?$', prefix, re.IGNORECASE):
        return "roman subsection", prefix
    elif re.match(r'^\(?[a-zA-Z]\)?$', prefix):
        return "alpha subsection", prefix
    elif re.match(r'^\d+(\.\d+)+$', prefix):  # e.g. 1.1, 2.3.4
        return "numeric subsection", prefix
    elif re.match(r'^\d+(\.)?$', prefix):     # e.g. 1 or 2.
        return "numeric section", prefix
    return None, None

def extract_docx_structure(doc_path):
    doc = Document(doc_path)
    hierarchy = []
    current_section = None
    current_subsection = None

    def is_section(para):
        return para.paragraph_format.alignment == 1 and any(run.bold for run in para.runs if run.text.strip())

    def is_bullet(para):
        return para.style.name and "List" in para.style.name

    def add_content(text, ctype, prefix=None):
        content = {"type": ctype, "text": text}
        if prefix:
            content["prefix"] = prefix
        if current_subsection is not None:
            current_subsection["content"].append(content)
        elif current_section is not None:
            current_section["content"].append(content)
        else:
            hierarchy.append({"heading": None, "content": [content], "subsections": []})

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
        prefix_type, prefix = get_prefix_type(text)
        if prefix_type == "numeric subsection":
            if current_subsection:
                current_section["subsections"].append(current_subsection)
            current_subsection = {"subheading": text, "content": []}
            continue
        content_type = "bullet" if is_bullet(para) else "paragraph"
        if prefix_type:
            content_type = prefix_type
        add_content(text, content_type, prefix)

    if current_subsection:
        current_section["subsections"].append(current_subsection)
    if current_section:
        hierarchy.append(current_section)

    # Add tables in last section/subsection or top level if none
    for table in doc.tables:
        table_data = [[cell.text.strip() for cell in row.cells] for row in table.rows]
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

def extract_pdf_texts(pdf_path):
    reader = PdfReader(pdf_path)
    texts = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            # Split by lines, strip each
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            texts.extend(lines)
    return texts

def find_prefix_in_pdf(pdf_texts, para_text, max_chars=50):
    """
    Attempt to find prefix from pdf_texts matching start of para_text (first max_chars)
    Return prefix string if found else None
    """
    para_start = para_text[:max_chars].lower()
    for line in pdf_texts:
        line_lower = line.lower()
        # Check if para_start is contained within line (allow partial fuzzy)
        if para_start in line_lower or line_lower in para_start:
            # Try to extract prefix from pdf line start
            prefix_type, prefix = get_prefix_type(line)
            if prefix:
                return prefix
    return None

def update_types_with_pdf(hierarchy, pdf_texts):
    """
    Recursively update paragraph/bullet types based on prefixes found in pdf_texts.
    Only update type and add prefix if missing.
    """
    def recurse_sections(sections):
        for section in sections:
            # Update heading - no change as it's section heading
            if "subsections" in section:
                recurse_sections(section["subsections"])
            # Update content list
            for item in section.get("content", []):
                if item.get("type") in ["paragraph", "bullet"]:
                    if "prefix" not in item:
                        prefix = find_prefix_in_pdf(pdf_texts, item["text"])
                        if prefix:
                            ptype, _ = get_prefix_type(prefix)
                            if ptype:
                                item["type"] = ptype
                                item["prefix"] = prefix
    recurse_sections(hierarchy)
    return hierarchy

# --- Usage ---
if __name__ == "__main__":
    docx_path = "your_file.docx"  # Replace with your Word docx path
    pdf_path = "your_file.pdf"    # Replace with your PDF path

    # Step 1: Extract structure from DOCX
    structure = extract_docx_structure(docx_path)

    # Step 2: Extract lines of text from PDF
    pdf_lines = extract_pdf_texts(pdf_path)

    # Step 3: Update types and prefixes using PDF text lines
    updated_structure = update_types_with_pdf(structure, pdf_lines)

    # Save final JSON
    with open("final_structured_output.json", "w", encoding="utf-8") as f:
        json.dump(updated_structure, f, ensure_ascii=False, indent=2)

    print("Extraction and update done. Output saved to final_structured_output.json")
