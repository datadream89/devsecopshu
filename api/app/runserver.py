import fitz  # PyMuPDF
import pdfplumber
import json
import re

def get_non_table_pages_first_n(pdf_path, max_pages=7):
    non_table_pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages[:max_pages]):
            if not page.extract_tables():
                non_table_pages.append(i + 1)
    return non_table_pages

def is_number_like(text):
    return re.match(r'^([0-9]+(\.[0-9]+)*|[IVXLCDM]+)$', text.strip(), re.IGNORECASE)

def extract_section_titles(pdf_path, non_table_pages):
    doc = fitz.open(pdf_path)
    merged_output = []

    for page_num in non_table_pages:
        page = doc[page_num - 1]
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            for line in block.get("lines", []):
                line_spans = line.get("spans", [])
                bold_number = None
                bold_underlined_parts = []

                for span in line_spans:
                    text = span["text"].strip()
                    if not text:
                        continue
                    font = span.get("font", "").lower()
                    flags = span.get("flags", 0)
                    is_bold = "bold" in font
                    is_underlined = bool(flags & 4)

                    if is_bold and not is_underlined and is_number_like(text):
                        bold_number = text

                    elif is_bold and is_underlined:
                        bold_underlined_parts.append(text)

                if bold_number and bold_underlined_parts:
                    merged_output.append({
                        "page": page_num,
                        "section": bold_number,
                        "title": " ".join(bold_underlined_parts)
                    })

    return merged_output

# === Example usage ===
pdf_path = "your_file.pdf"  # Replace with actual path
non_table_pages = get_non_table_pages_first_n(pdf_path)
section_titles = extract_section_titles(pdf_path, non_table_pages)

with open("merged_section_titles.json", "w") as f:
    json.dump(section_titles, f, indent=2)

print("Done. Output written to merged_section_titles.json")
