import pdfplumber
import fitz
import re

def split_table_non_table_pages(pdf_path, max_page=7):
    table_pages = []
    non_table_pages = []

    with pdfplumber.open(pdf_path) as pdf:
        total_pages = min(len(pdf.pages), max_page)
        for i in range(total_pages):
            page = pdf.pages[i]
            tables = page.extract_tables()
            if tables and len(tables) > 0:
                table_pages.append(i + 1)
            else:
                non_table_pages.append(i + 1)

    return table_pages, non_table_pages

def extract_bold_underlined_quoted_text(page_fitz, line_text):
    """
    Extract the bold, underlined, or quoted portion immediately following section header
    This is a placeholder function. You need to implement the logic by checking text spans in
    the page using PyMuPDF (fitz).
    """

    # Example: extract spans on the line that are bold or underlined or quoted
    # For now, return None to fallback to rest of line
    # You can expand this by scanning text spans on the page_fitz

    # Pseudocode:
    # for span in page_fitz.get_text("dict")["blocks"]:
    #     for line in span["lines"]:
    #         for span in line["spans"]:
    #             if span['text'] in line_text and (span['flags'] & BOLD_FLAG or UNDERLINE_FLAG):
    #                 collect that span text as title

    return None

def extract_section_headers(pdf_path, non_table_pages, max_page=7):
    # Regex to match section headers like: 1. 1.1 6.1.2 a. (a) i. IV etc.
    section_header_re = re.compile(
        r'^\s*(\d+(\.\d+)*|[ivxlcdmIVXLCDM]+|[a-zA-Z]|\([a-zA-Z0-9]+\))\.?\s*(.*)'
    )

    headers = []
    with pdfplumber.open(pdf_path) as pdf:
        doc = fitz.open(pdf_path)
        for page_num in non_table_pages:
            if page_num > max_page:
                continue

            page_plumber = pdf.pages[page_num - 1]
            page_fitz = doc.load_page(page_num - 1)
            text = page_plumber.extract_text() or ""
            lines = text.split('\n')

            for line in lines:
                line = line.strip()
                if not line:
                    continue
                match = section_header_re.match(line)
                if match:
                    section_num = match.group(1)
                    rest = match.group(3).strip()

                    title = extract_bold_underlined_quoted_text(page_fitz, line)

                    headers.append({
                        "page": page_num,
                        "section": section_num,
                        "title": title if title else rest
                    })
    return headers

if __name__ == "__main__":
    pdf_path = "your_file.pdf"  # Replace with your PDF file path

    # Step 1: Split first 7 pages into table and non-table pages
    table_pages, non_table_pages = split_table_non_table_pages(pdf_path, max_page=7)
    print(f"Table pages (up to 7): {table_pages}")
    print(f"Non-table pages (up to 7): {non_table_pages}")

    # Step 2: Extract section headers only on non-table pages within first 7 pages
    headers = extract_section_headers(pdf_path, non_table_pages, max_page=7)
    print("Extracted headers:")
    for h in headers:
        print(h)
