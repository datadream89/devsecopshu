import fitz  # PyMuPDF
import pdfplumber
import json

def get_non_table_pages_first_n(pdf_path, max_pages=7):
    non_table_pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages[:max_pages]):
            if not page.extract_tables():
                non_table_pages.append(i + 1)
    return non_table_pages

def extract_all_bold_text(pdf_path, non_table_pages):
    doc = fitz.open(pdf_path)
    bold_entries = []

    for page_num in non_table_pages:
        page = doc[page_num - 1]
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span["text"].strip()
                    font = span.get("font", "").lower()

                    if "bold" in font and text:
                        bold_entries.append({
                            "page": page_num,
                            "text": text
                        })

    return bold_entries

# Example usage
pdf_path = "your_file.pdf"  # <-- Replace with your PDF path
non_table_pages = get_non_table_pages_first_n(pdf_path)
bold_texts = extract_all_bold_text(pdf_path, non_table_pages)

# Output to JSON
with open("bold_texts.json", "w") as f:
    json.dump(bold_texts, f, indent=2)

print("Done. Bold text saved to bold_texts.json")
