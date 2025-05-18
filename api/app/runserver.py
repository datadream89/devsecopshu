import fitz  # PyMuPDF
import pdfplumber
import re
import json

def is_section_number(text):
    return bool(re.match(r'^\d+(\.\d+)*\.?$', text.strip()))

def extract_bold_titles_with_section_numbers(pdf_path, non_table_pages):
    doc = fitz.open(pdf_path)
    section_headers = []

    for page_num in non_table_pages:
        page = doc[page_num - 1]
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            for line in block.get("lines", []):
                spans = line.get("spans", [])
                for i, span in enumerate(spans):
                    text = span["text"].strip()
                    font = span.get("font", "").lower()

                    # Check for bold
                    if "bold" in font and text:
                        # Look for preceding span
                        preceding_text = ""
                        j = i - 1
                        while j >= 0:
                            prev_text = spans[j]["text"].strip()
                            if prev_text:
                                preceding_text = prev_text
                                break
                            j -= 1

                        # Must be a valid section number
                        if is_section_number(preceding_text):
                            section_headers.append({
                                "page": page_num,
                                "section": preceding_text,
                                "title": text
                            })

    return section_headers

def get_non_table_pages_first_n(pdf_path, max_pages=7):
    non_table_pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages[:max_pages]):
            if not page.extract_tables():
                non_table_pages.append(i + 1)
    return non_table_pages

# Example usage
pdf_path = "your_file.pdf"  # <-- Replace with your file path
non_table_pages = get_non_table_pages_first_n(pdf_path)
bold_sections = extract_bold_titles_with_section_numbers(pdf_path, non_table_pages)

# Output JSON
with open("bold_section_headers.json", "w") as f:
    json.dump(bold_sections, f, indent=2)

print("Extraction complete. Output saved to bold_section_headers.json")
