import pdfplumber
import re
import json
import os
# Quote pairs for matching different double-quote styles
QUOTE_PAIRS = [
    ('"', '"'), ('“', '”'), ('„', '“'), ('«', '»'), ('‹', '›'), ('‟', '”'),
    ('❝', '❞'), ('〝', '〞'), ('＂', '＂')
]

def extract_title_and_rest(text):
    text = text.strip()
    title = None
    remainder = text

    for open_q, close_q in QUOTE_PAIRS:
        pattern = re.escape(open_q) + r'(.+?)' + re.escape(close_q)
        match = re.search(pattern, text)
        if match:
            title = match.group(1).strip()
            remainder = text.replace(match.group(0), '').strip()
            return title, remainder

    # If not quoted, consider short all caps or titlecased string as title
    if text and (text.isupper() or (text.istitle() and len(text.split()) <= 6)):
        return text, ""

    return None, remainder

def is_top_level_section(header):
    return bool(re.match(r"^\d+\.$", header))  # e.g., 1., 2.

def extract_sections(pdf_path):
    section_pattern = re.compile(
        r"""^\s*
        (?P<header>
            (?:\d+(?:\.\d+)*\.)     # 1., 1.1., 2.3.4.
            | [a-zA-Z]\.            # a., B.
            | \([a-zA-Z0-9]+\)      # (a), (1)
        )
        \s*
        (?P<rest>.*)?$
        """, re.VERBOSE
    )

    sections = []
    current = None
    buffer = []

    def flush():
        if current and buffer:
            current["paragraph"] = "\n".join(buffer).strip()
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
                        if is_top_level_section(header):
                            current["topic"] = title
                        else:
                            current["section_title"] = title
                    if rest:
                        buffer.append(rest)
                elif current:
                    buffer.append(line)

        flush()

    return sections

def save_to_json(data, output_path):
    with open(output_path, "w", encoding="utf-_
