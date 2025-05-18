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

def extract_bold_and_underlined(pdf_path, non_table_pages):
    doc = fitz.open(pdf_path)
    output = {
        "bold_numbers": [],
        "bold_underlined_texts": []
    }

    for page_num in non_table_pages:
        page = doc[page_num - 1]
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            for line in block.get("lines", []):
                current_text = ""
                collecting = False

                for span in line.get("spans", []):
                    text = span["text"]
                    font = span.get("font", "").lower()
                    flags = span.get("flags", 0)

                    is_bold = "bold" in font
                    is_underlined = bool(flags & 4)

                    if is_bold and is_underlined:
                        collecting = True
                        current_text += text  # preserve spacing within the line
                    elif collecting:
                        # Finalize the collected underlined + bold phrase
                        output["bold_underlined_texts"].append({
                            "page": page_num,
                            "text": current_text.strip()
                        })
                        current_text = ""
                        collecting = False

                    if is_bold and not is_underlined and is_number_like(text.strip()):
                        output["bold_numbers"].append({
                            "page": page_num,
                            "text": text.strip()
                        })

                # If still collecting at end of line
                if collecting and current_text.strip():
                    output["bold_underlined_texts"].append({
                        "page": page_num,
                        "text": current_text.strip()
                    })

    return output

# === Example usage ===
pdf_path = "your_file.pdf"  # Replace with actual path
non_table_pages = get_non_table_pages_first_n(pdf_path)
result = extract_bold_and_underlined(pdf_path, non_table_pages)

with open("bold_and_underlined_output.json", "w") as f:
    json.dump(result, f, indent=2)

print("Done. Output written to bold_and_underlined_output.json")
