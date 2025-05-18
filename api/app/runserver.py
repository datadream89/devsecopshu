import pdfplumber
import fitz  # PyMuPDF

def get_non_table_pages(pdf_path, max_pages=7):
    non_table_pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages[:max_pages], start=1):
            tables = page.find_tables()
            if not tables:
                non_table_pages.append(i)
    return non_table_pages

def extract_filtered_toc(pdf_path, non_table_pages):
    doc = fitz.open(pdf_path)
    toc = doc.get_toc(simple=False)
    doc.close()
    # Filter TOC entries only on non-table pages
    filtered_toc = [entry for entry in toc if entry[2] in non_table_pages]
    return filtered_toc

if __name__ == "__main__":
    pdf_path = "your_file.pdf"
    non_table_pages = get_non_table_pages(pdf_path, max_pages=7)
    print("Non-table pages (1-7):", non_table_pages)

    filtered_toc = extract_filtered_toc(pdf_path, non_table_pages)
    for level, title, page in filtered_toc:
        print(f"Level {level} - Page {page}: {title}")
