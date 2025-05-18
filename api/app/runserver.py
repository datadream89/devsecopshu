import pdfplumber

def split_pdf_by_tables(pdf_path):
    table_pages = []
    non_table_pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            tables = page.find_tables()
            if tables:
                table_pages.append(i)
            else:
                non_table_pages.append(i)
    return table_pages, non_table_pages

# Usage
pdf_path = "your_file.pdf"
table_pages, non_table_pages = split_pdf_by_tables(pdf_path)
print("Pages with tables:", table_pages)
print("Pages without tables:", non_table_pages)
