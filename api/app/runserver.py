import pdfplumber
import fitz  # PyMuPDF
import re
import json

# Regex to detect section headers (numbers, letters, roman numerals)
section_header_re = re.compile(
    r"""^\s*
    (?P<header>
        (\d+(\.\d+)*\.?)      # e.g. 6. or 6.1 or 2.3.4
        | [ivxlcdm]+\.+       # roman numerals like ii.
        | [a-zA-Z]\.          # letters like a.
        | \([a-zA-Z0-9]+\)    # bracketed like (a), (1)
    )
    \s*
    (?P<rest>.*)$
    """, re.VERBOSE | re.IGNORECASE
)

def split_section_numbers(header):
    h = header.rstrip('.').lower()
    # normalize roman numerals or bracketed separately
    if header.startswith('(') and header.endswith(')'):
        return [header]
    if re.match(r"^[a-zA-Z]\.?$", header):
        return [header]
    if re.match(r"^[ivxlcdm]+\.$", header, re.IGNORECASE):
        return [header]
    return h.split('.')

def is_section_header(line):
    return bool(section_header_re.match(line))

def get_font_flags(fitz_span):
    # Returns True if span is bold or underlined
    is_bold = "Bold" in f"{fitz_span.font}".lower() or f"bold" in f"{fitz_span.font}".lower()
    is_underline = f["flags"] & 4 != 0  # 4 means underline flag in PyMuPDF span flags
    # Note: Sometimes underline detection is tricky; PyMuPDF uses span["flags"]
    return is_bold, is_underline

def extract_title_from_line(page, y0, y1, line_text, section_header_len):
    """
    Extract bold/underline/quoted substring immediately after section header from PyMuPDF page.

    Parameters:
        page (fitz.Page): page object from PyMuPDF
        y0, y1 (float): vertical bbox coordinates of the line in the page
        line_text (str): entire text line
        section_header_len (int): length of section header portion in line_text
    
    Returns:
        (title:str or None, remainder:str) - title extracted, remainder text appended to paragraph
    """

    # We want to find the first substring after section_header_len characters that is:
    # - Bold or Underlined
    # - or Quoted (starting with " or “ or similar)
    #
    # Use PyMuPDF spans: spans have bbox, font info and text.
    # Find spans overlapping with y0,y1, and text position after section header.

    spans = []
    for block in page.get_text("dict")["blocks"]:
        if block["type"] != 0:
            continue
        for line in block["lines"]:
            ly0 = line["bbox"][1]
            ly1 = line["bbox"][3]
            # Check vertical overlap with line bbox
            if ly1 < y0 or ly0 > y1:
                continue
            # get spans within this line
            for span in line["spans"]:
                spans.append(span)

    # Now concatenate spans in reading order
    full_text = "".join([s["text"] for s in spans])
    # The line_text may be slightly different but should be close.
    # We'll try to identify which part of spans corresponds to the text after section header.

    after_header_text = line_text[section_header_len:].strip()

    # Find the starting index of after_header_text in full_text to sync span indices
    idx_in_full = full_text.find(after_header_text)
    if idx_in_full == -1:
        # fallback: use whole line_text after header as text to analyze
        after_header_text = line_text[section_header_len:].strip()
        idx_in_full = 0

    # We'll check spans in order to find first bold/underline/quoted substring at start of after_header_text

    # Step 1: Identify spans that cover after_header_text start
    combined_text = ""
    candidate_spans = []
    start_found = False
    for span in spans:
        combined_text += span["text"]
        if not start_found and combined_text.find(after_header_text) != -1:
            start_found = True

    # Instead of complicated matching, simpler approach:
    # Iterate spans overlapping line and extract consecutive spans with bold/underline
    # concatenated at start of after_header_text

    # We'll build candidate substrings from spans in reading order
    title_parts = []
    collecting = False
    collected_text = ""
    for span in spans:
        span_text = span["text"]
        # Skip spans before after_header_text start in the line_text
        if not collecting:
            if after_header_text.startswith(span_text) or span_text.startswith(after_header_text[:len(span_text)]):
                collecting = True
            else:
                continue
        if collecting:
            is_bold = "bold" in span["font"].lower()
            is_underline = span.get("flags", 0) & 4 != 0
            # Check for quoted substrings in span_text
            quoted_match = re.match(r'["“”«»‹›❝❞〝〞＂](.+?)["“”«»‹›❝❞〝〞＂]', span_text)
            if is_bold or is_underline or quoted_match:
                title_parts.append(span_text)
                collected_text += span_text
            else:
                # If non bold/underline span encountered after collecting, stop
                if collected_text:
                    break
                else:
                    # Not bold or underline and no collected text yet - skip
                    continue
    title = "".join(title_parts).strip()
    if title:
        # Remove title from after_header_text remainder
        remainder = after_header_text[len(title):].strip()
        return title, remainder
    else:
        # Try quoted substring from after_header_text
        quoted = re.match(r'["“”«»‹›❝❞〝〞＂](.+?)["“”«»‹›❝❞〝〞＂]', after_header_text)
        if quoted:
            return quoted.group(1).strip(), after_header_text[quoted.end():].strip()
        else:
            return None, after_header_text

def insert_section(root, section_numbers, section_data):
    current = root
    for i, part in enumerate(section_numbers):
        if "children" not in current:
            current["children"] = {}

        key = part if i != 0 else f"{part}_page_{section_data['page_start']}"

        if key not in current["children"]:
            current["children"][key] = {
                "section_header": part + ('.' if not part.endswith('.') else ''),
                "paragraph": "",
                "tables": [],
            }
        current = current["children"][key]

        # Update data at last level
        if i == len(section_numbers) - 1:
            # Insert or append paragraph
            if "paragraph" not in current:
                current["paragraph"] = ""
            if "paragraph" in section_data:
                current["paragraph"] += section_data["paragraph"] + "\n"
            # Insert tables
            if "tables" in section_data:
                current["tables"].extend(section_data["tables"])
            # Insert/overwrite other metadata
            for k, v in section_data.items():
                if k not in ("paragraph", "tables"):
                    current[k] = v

def flatten_tree(node):
    def helper(node):
        res = {}
        for k in ("page_start", "page_end", "section_header", "topic", "section_title", "paragraph", "tables"):
            if k in node:
                res[k] = node[k].strip() if isinstance(node[k], str) else node[k]
        if "children" in node:
            res["children"] = [helper(child) for key, child in sorted(node["children"].items())]
        return res
    return helper(node)

def extract_sections(pdf_path):
    root = {"section_header": "root", "paragraph": "", "children": {}}
    current_section_numbers = None
    current_section_data = {"paragraph": "", "tables": []}
    last_section_numbers = None
    last_section_page = None

    # Open both pdfplumber and fitz document
    pdf_plumber = pdfplumber.open(pdf_path)
    pdf_fitz = fitz.open(pdf_path)

    # Keep track of current section start page and last page seen
    current_section_start_page = None

    # Helper to flush current buffer to root tree
    def flush_section():
        nonlocal current_section_numbers, current_section_data, current_section_start_page
        if current_section_numbers:
            current_section_data["page_end"] = last_section_page
            current_section_data["page_start"] = current_section_start_page
            insert_section(root, current_section_numbers, current_section_data)
        # Reset current section data buffer
        current_section_numbers = None
        current_section_data.clear()
        current_section_data["paragraph"] = ""
        current_section_data["tables"] = []

    # Helper to find if line is section header and parse it
    def parse_line_for_section_header(line):
        m = section_header_re.match(line)
        if m:
            header = m.group("header").strip()
            rest = m.group("rest") or ""
            return header, rest
        return None, None

    for page_num, (page_p, page_f) in enumerate(zip(pdf_plumber.pages, pdf_fitz), start=1):
        text = page_p.extract_text() or ""
        lines = text.split("\n")

        # Extract tables on page
        tables = page_p.extract_tables()

        # We'll keep track if table is found on page to insert later into section
        tables_for_section = []

        # Process each line in the page
        for line in lines:
            line = line.strip()
            header, rest_of_line = parse_line_for_section_header(line)

            if header:
                # Flush existing section before starting new
                flush_section()
                current_section_numbers = split_section_numbers(header)
                current_section_start_page = page_num
                last_section_page = page_num

                # Extract section title from PyMuPDF page line bbox & formatting
                # We need y0,y1 bbox of this line from PyMuPDF page

                # Find matching line bbox by searching lines in PyMuPDF dict blocks
                y0, y1 = None, None
                for block in page_f.get_text("dict")["blocks"]:
                    if block["type"] != 0:
                        continue
                    for l in block["lines"]:
                        text_line = "".join([span["text"] for span in l["spans"]]).strip()
                        if text_line == line:
                            y0, y1 = l["bbox"][1], l["bbox"][3]
                            break
                    if y0 and y1:
                        break

                section_title = None
                remainder = rest_of_line

                if y0 and y1:
                    section_title, remainder = extract_title_from_line(page_f, y0, y1, line, len(header))

                # If section title found, add metadata, else all rest_of_line is paragraph
                current_section_data = {
                    "section_header": header,
                    "paragraph": remainder.strip(),
                    "tables": [],
                    "section_title": section_title
                }

                # Set topic if this is subsection (parent section title)
                if len(current_section_numbers) > 1:
                    # Find parent section title from root tree
                    parent_nums = current_section_numbers[:-1]
                    parent = root
                    for num in parent_nums:
                        key = num if parent is root else num
                        # keys in children have page number suffix at first level
                        found_key = None
                        for k in parent.get("children", {}):
                            if k.startswith(num):
                                found_key = k
                                break
                        if found_key:
                            parent = parent["children"][found_key]
                        else:
                            parent = None
                            break
                    if parent and "section_title" in parent:
                        current_section_data["topic"] = parent["section_title"]

            else:
                # No section header: append line to current section paragraph buffer
                if current_section_numbers:
                    current_section_data["paragraph"] += "\n" + line
                    last_section_page = page_num

        # Add tables found on this page to current section
        if current_section_numbers and tables:
            current_section_data.setdefault("tables", []).extend(tables)

    # Flush last section at end
    flush_section()

    pdf_plumber.close()
    pdf_fitz.close()

    return flatten_tree(root)

def save_to_json(data, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    pdf_path = "your_file.pdf"  # Change to your PDF file path
    nested_output_path = "nested_output.json"

    nested_data = extract_sections(pdf_path)
    save_to_json(nested_data, nested_output_path)

    print(f"Extracted nested sections saved to {nested_output_path}")
