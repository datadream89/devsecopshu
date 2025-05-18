import re
import pdfplumber
import fitz  # PyMuPDF

QUOTE_PAIRS = [
    ('"', '"'), ('“', '”'), ('„', '“'), ('«', '»'), ('‹', '›'),
    ('‟', '”'), ('❝', '❞'), ('〝', '〞'), ('＂', '＂')
]

def is_quoted(text):
    for open_q, close_q in QUOTE_PAIRS:
        if text.startswith(open_q) and text.endswith(close_q):
            return True
    return False

def extract_bold_underlined_quoted_text_after_section(page_fitz, line, section_num):
    """
    Extract the bold/underlined/quoted text immediately after the section number in the line.
    Return None if no such text found.
    """
    # Get spans from page
    blocks = page_fitz.get_text("dict").get("blocks", [])
    spans = []
    for b in blocks:
        for l in b.get("lines", []):
            for s in l.get("spans", []):
                spans.append(s)

    # Find start index of section number in line text
    section_index = line.find(section_num)
    if section_index == -1:
        return None

    # Remaining text after section number (strip leading whitespace and dots)
    after_section = line[section_index + len(section_num):].lstrip(" .")

    if not after_section:
        return None

    # We'll try to find spans which are inside the after_section substring

    # Strategy:
    # - Find span(s) whose text is a substring of after_section starting from beginning
    # - Among those, pick the longest bold/underlined/quoted span (or combination if contiguous)

    # Collect candidates: spans whose text appears at start of after_section
    candidates = []
    after_section_lower = after_section.lower()

    for span in spans:
        span_text = span.get("text", "").strip()
        if not span_text:
            continue
        # Check if after_section starts with this span text (case insensitive)
        if after_section_lower.startswith(span_text.lower()):
            # Check formatting
            font_flags = span.get("flags", 0)
            is_bold = (font_flags & 2) != 0
            is_underline = span.get("underline", False)
            quoted = is_quoted(span_text)

            if is_bold or is_underline or quoted:
                candidates.append(span_text)

    if not candidates:
        return None

    # Return the longest candidate as the best title
    best_title = max(candidates, key=len)
    return best_title

def extract_section_headers(pdf_path, non_table_pages, max_page=7):
    # Regex matches:
    #  - Numbered sections like 1. or 1.2. or 1.2.3.
    #  - Single letters with trailing dot like a. or B.
    #  - Roman numerals with trailing dot like i. or iv.
    section_header_re = re.compile(
        r'^\s*('
        r'(?:\d+(?:\.\d+)*\.)'             # e.g. 1. or 1.2. or 2.6.4.
        r'|[a-zA-Z]\.'                     # e.g. a. or B.
        r'|M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\.'  # Roman numerals with dot
        r')\s*(.*)$'
    )

    headers = []

    with pdfplumber.open(pdf_path) as pdf:
        doc = fitz.open(pdf_path)
        for page_num in non_table_pages:
            if page_num > max_page:
                break

            page_plumber = pdf.pages[page_num - 1]
            page_fitz = doc.load_page(page_num - 1)

            text = page_plumber.extract_text()
            if not text:
                continue
            lines = text.split('\n')

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                match = section_header_re.match(line)
                if match:
                    section_num = match.group(1)
                    rest_of_line = match.group(2).strip()

                    # Extract title as only bold/underline/quoted text immediately after section_num
                    title = extract_bold_underlined_quoted_text_after_section(page_fitz, line, section_num)

                    # If no title found by formatting, fallback to None or empty (don't use full rest_of_line)
                    if not title:
                        title = None

                    headers.append({
                        "page": page_num,
                        "section": section_num.rstrip('.'),  # remove trailing dot
                        "title": title
                    })

    return headers

# Example usage:
if __name__ == "__main__":
    pdf_path = "your_pdf_file.pdf"
    non_table_pages = list(range(1, 8))  # first 7 pages
    headers = extract_section_headers(pdf_path, non_table_pages)
    import json
    print(json.dumps(headers, indent=2))
