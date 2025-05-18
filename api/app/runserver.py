import re
import pdfplumber
import fitz  # PyMuPDF

QUOTE_PAIRS = [
    ('"', '"'), ('“', '”'), ('„', '“'), ('«', '»'), ('‹', '›'),
    ('‟', '”'), ('❝', '❞'), ('〝', '〞'), ('＂', '＂')
]

def extract_bold_underlined_quoted_text(page_fitz, line_text):
    if not line_text:
        return None

    blocks = page_fitz.get_text("dict").get("blocks", [])
    spans = []
    for b in blocks:
        for l in b.get("lines", []):
            for s in l.get("spans", []):
                spans.append(s)

    line_text_stripped = line_text.strip()
    candidates = []

    for span in spans:
        span_text = span.get("text", "")
        if not span_text:
            continue
        if span_text.strip() in line_text_stripped:
            font_flags = span.get("flags", 0)
            is_bold = (font_flags & 2) != 0
            is_underline = span.get("underline", False)
            is_quoted = False
            for open_q, close_q in QUOTE_PAIRS:
                if span_text.startswith(open_q) and span_text.endswith(close_q):
                    is_quoted = True
                    break
            if is_bold or is_underline or is_quoted:
                candidates.append(span_text.strip())

    if candidates:
        return max(candidates, key=len)
    return None

def extract_section_headers(pdf_path, non_table_pages, max_page=7):
    # Regex updated to capture section number and rest of line correctly
    section_header_re = re.compile(
        r'^\s*('
        r'(?:\d+(?:\.\d+)*)'             # Numbers with dots, e.g. 1 or 1.2 or 1.2.3
        r'|[a-zA-Z]'                     # Single letter
        r'|M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})'  # Roman numerals
        r')\.?\s*(.*)'
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
                if not line:
                    continue
                line = line.strip()
                if not line:
                    continue
                match = section_header_re.match(line)
                if match:
                    section_num = match.group(1)
                    rest_of_line = match.group(2).strip() if match.group(2) else ""

                    title = extract_bold_underlined_quoted_text(page_fitz, line)
                    if not title:
                        title = rest_of_line

                    headers.append({
                        "page": page_num,
                        "section": section_num,
                        "title": title
                    })

    return headers

# Usage example
if __name__ == "__main__":
    pdf_path = "your_pdf_file.pdf"
    non_table_pages = list(range(1, 8))  # first 7 pages (non-table)
    results = extract_section_headers(pdf_path, non_table_pages)
    import json
    print(json.dumps(results, indent=2))
