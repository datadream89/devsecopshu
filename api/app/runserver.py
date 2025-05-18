import re
import pdfplumber
import fitz  # PyMuPDF

# Helper: Recognize quotes
QUOTE_PAIRS = [
    ('"', '"'), ('“', '”'), ('„', '“'), ('«', '»'), ('‹', '›'),
    ('‟', '”'), ('❝', '❞'), ('〝', '〞'), ('＂', '＂')
]

def extract_bold_underlined_quoted_text(page_fitz, line_text):
    """
    Find the first bold/underline or quoted text *immediately after* the section number in line_text.
    Returns the matched string or None.
    """
    blocks = page_fitz.get_text("dict")["blocks"]
    # Flatten all spans of the page with their text and font flags
    spans = []
    for b in blocks:
        for l in b.get("lines", []):
            for s in l.get("spans", []):
                spans.append(s)

    # Try to find the part of line_text which is bold/underline or quoted, immediately after section number

    # We'll iterate over spans to find a span matching part of line_text,
    # then check if it's bold/underline or quoted.

    line_text_stripped = line_text.strip()
    candidates = []

    # We'll try to find all candidate spans that are substrings of line_text and have the style
    for span in spans:
        span_text = span.get("text", "").strip()
        if not span_text:
            continue

        # Check if span_text is in line_text
        if span_text in line_text_stripped:
            # Check for bold or underline or quoted
            font_flags = span.get("flags", 0)
            # font_flags bit 2 (value=2) = bold, bit 1 (value=1) = italic, bit 4 (value=4) = monospace, bit 5 (value=32) = serif, bit 6 (value=64) underline (check docs)
            is_bold = (font_flags & 2) != 0
            is_underline = (span.get("underline", False) is True)
            # Check quotes
            is_quoted = False
            for open_q, close_q in QUOTE_PAIRS:
                if span_text.startswith(open_q) and span_text.endswith(close_q):
                    is_quoted = True
                    break

            if is_bold or is_underline or is_quoted:
                candidates.append(span_text)

    if candidates:
        # Return the longest candidate (most likely the full title)
        return max(candidates, key=len)

    return None

def extract_section_headers(pdf_path, non_table_pages, max_page=7):
    # Regex to match section headers:
    # numbers with dots (like 1.2.3), single letters (a., B.), Roman numerals (IV., XII.)
    section_header_re = re.compile(
        r'^\s*('
        r'(?:\d+(?:\.\d+)+)'               # Numbers with dots like 1.2 or 3.1.4
        r'|[a-zA-Z]'                       # Single letter
        r'|M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})'  # Roman numerals
        r')\.?\s*(.*)'
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
                    rest_of_line = match.group(3).strip()

                    # Extract bold/underline/quoted text immediately following section number
                    title = extract_bold_underlined_quoted_text(page_fitz, line)

                    headers.append({
                        "page": page_num,
                        "section": section_num,
                        "title": title if title else rest_of_line
                    })
    return headers

# --- Example usage ---
if __name__ == "__main__":
    pdf_path = "your_pdf_file.pdf"
    # Example non-table pages (from your earlier step), here assumed pages 1 to 7 for demo
    non_table_pages = list(range(1, 8))

    section_headers = extract_section_headers(pdf_path, non_table_pages, max_page=7)

    import json
    print(json.dumps(section_headers, indent=2))
