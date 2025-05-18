import pdfplumber

def get_non_table_pages_first_n(pdf_path, max_pages=7):
    non_table_pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages[:max_pages]):
            tables = page.extract_tables()
            if not tables:
                non_table_pages.append(i + 1)  # +1 for 1-based page numbers
    return non_table_pages

# Example usage
pdf_path = "your_file.pdf"  # Replace with your actual file path
non_table_pages = get_non_table_pages_first_n(pdf_path)
print("First non-table pages (up to 7):", non_table_pages)
