import pdfplumber
import re
import json
import os
def extract_title_and_rest(text):
    # Extract quoted or uppercase or underlined-like (--- below it) parts as title
    title = None
    remainder = text.strip()

    # Double quoted title
    quote_match = re.search(r'"([^"]+)"', text)
    if quote_match:
        title = quote_match.group(1)
        remainder = text.replace(quote_match.group(0), "").strip()

    # ALL CAPS title
    elif text.isupper() or text.istitle() and len(text.split()) <= 6:
        title = text
        remainder = ""

    return title, remainder

def extract_sections(pdf_path):
    section_pattern = re.compile(
        r"""^\s*
        (?P<header>
            (?:\d+(?:\.\d+)*\.)     # 1., 1.1., 2.3.4.
            | [a-zA-Z]\.            # a., B.
            | \([a-zA-Z0-9]+\)      # (a), (1)
        )
        \s*
        (?P<rest>.*)?$             # rest of the line
        """, re.VERBOSE
    )

    sections = []
    current = None
    buffer = []

    def flush():
        if current and buffer:
            if "paragraph" not in current:
                current["paragraph"] = ""
            current["paragraph"] += "\n".join(buffer).strip()
            sections.append(current.copy())
            buffer.clear()

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            lines = text.split("\n")
            for line in lines:
                line = line.strip()
                match = section_pattern.match(line)
                if match:
                    flush()
                    header = match.group("header").strip()
                    rest_of_line = match.group("rest") or ""

                    current = {
                        "page": page_num,
                        "section_header": header
                    }

                    title, rest = extract_title_and_rest(rest_of_line)
                    if title:
                        current["section_title"] = title
                    if rest:
                        buffer.append(rest)
                elif current:
                    buffer.append(line)

        flush()

    return sections

def save_to_json(data, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ========== Example Usage ==========
if __name__ == "__main__":
    pdf_path = "your_file.pdf"  # Replace with your PDF
    output_path = "sections_with_titles_and_paragraphs.json"

    sections = extract_sections(pdf_path)
    save_to_json(sections, output_path)

    print(f"Done. Output saved to {output_path}")
