import pdfplumber
import fitz  # PyMuPDF
import re
import json

QUOTE_PAIRS = [
    ('"', '"'), ('“', '”'), ('„', '“'), ('«', '»'), ('‹', '›'), ('‟', '”'),
    ('❝', '❞'), ('〝', '〞'), ('＂', '＂')
]

def extract_quoted(text):
    for open_q, close_q in QUOTE_PAIRS:
        pattern = re.escape(open_q) + r'(.+?)' + re.escape(close_q)
        match = re.match(pattern, text)
        if match:
            return match.group(1).strip()
    return None

section_header_re = re.compile(
    r"""^\s*
    (?P<header>
        (?:\d+(?:\.\d+)*\.?)     # e.g. 1, 1.1, 2.6.4, optionally ending with dot
        | [ivxlcdmIVXLCDM]+\.?   # roman numerals like iv.
        | [a-zA-Z]\.             # e.g. a. or B.
        | \([a-zA-Z0-9]+\)       # e.g. (a), (1)
    )
    \s*
    (?P<rest>.*)?$
    """, re.VERBOSE
)

def is_section_header(text):
    return section_header_re.match(text) is not None

def split_section_numbers(header):
    h = header.rstrip('.')
    if header.startswith('(') and header.endswith(')'):
        return [header]
    if re.match(r"^[a-zA-Z]\.?$", header):
        return [header]
    if re.match(r"^[ivxlcdmIVXLCDM]+\.?$", header):
        return [header.lower()]
    return h.split('.')

def is_bold_underline_or_quoted(text, page_num, page_blocks):
    # text must be found in page_blocks with bold or underline or quoted
    # page_blocks: list of dicts with keys 'text', 'bold', 'underline', 'block_no'
    # We'll check if text is fully in any block with bold or underline
    for block in page_blocks:
        block_text = block['text'].strip()
        if block_text.startswith(text) or text.startswith(block_text):
            if block.get('bold') or block.get('underline'):
                return True
            # also check quoted - quoted handled in extract_quoted so no need here
    return False

def extract_bold_underline_blocks(doc, page_num):
    # Using fitz to get blocks with formatting on page
    page = doc.load_page(page_num - 1)
    blocks = []
    for block in page.get_text("dict")["blocks"]:
        if block["type"] != 0:
            continue
        for line in block["lines"]:
            for span in line["spans"]:
                blocks.append({
                    "text": span["text"].strip(),
                    "bold": "bold" in span["font"].lower() or span.get("flags", 0) & 2 != 0,
                    "underline": span.get("underline", False),
                })
    return blocks

def insert_section(root, section_numbers, section_data):
    current = root
    for i, part in enumerate(section_numbers):
        if "children" not in current:
            current["children"] = []

        # Avoid duplicates: check if part already present among children
        found = None
        for child in current["children"]:
            if child.get("section_header", "") == part or child.get("section_id", "") == part:
                found = child
                break
        if not found:
            found = {
                "section_header": part + ('.' if not part.endswith('.') else ''),
                "section_id": part,
                "page_list": [],
                "paragraph": "",
                "children": []
            }
            current["children"].append(found)
        current = found
    # Update data on last section node
    # Append pages if not duplicate
    for p in section_data.get("pages", []):
        if p not in current["page_list"]:
            current["page_list"].append(p)
    # Append paragraph text (with newline)
    if "paragraph" in section_data:
        if current["paragraph"]:
            current["paragraph"] += "\n" + section_data["paragraph"].strip()
        else:
            current["paragraph"] = section_data["paragraph"].strip()

    # Update title/topic if present (overwrite to latest)
    if "title" in section_data:
        current["title"] = section_data["title"]
    if "topic" in section_data:
        current["topic"] = section_data["topic"]

def sort_children(children):
    # Sort children by first page in page_list asc, then by section_id in natural order
    def natural_key(s):
        # For section like 6.1 or (a) or iv
        # Return tuple for sorting
        sec_id = s.get("section_id", "")
        # Normalize roman numerals to int for sorting
        roman_map = {'i':1,'v':5,'x':10,'l':50,'c':100,'d':500,'m':1000}
        def roman_to_int(r):
            r = r.lower()
            total = 0
            prev = 0
            for c in reversed(r):
                val = roman_map.get(c, 0)
                if val < prev:
                    total -= val
                else:
                    total += val
                prev = val
            return total
        # Parse numeric parts
        if re.match(r"^\d+(\.\d+)*$", sec_id):
            parts = [int(x) for x in sec_id.split('.')]
            return (0, parts)
        elif re.match(r"^\([a-zA-Z0-9]+\)$", sec_id):
            return (2, sec_id)
        elif re.match(r"^[ivxlcdm]+$", sec_id.lower()):
            return (1, roman_to_int(sec_id))
        elif re.match(r"^[a-zA-Z]$", sec_id):
            return (3, sec_id.lower())
        else:
            return (4, sec_id)

    return sorted(children, key=lambda c: (min(c.get("page_list", [9999])), natural_key(c)))

def flatten_tree(node):
    # convert page_list to single int (smallest page)
    flat = {}
    for key in ("section_header", "title", "topic", "paragraph"):
        if key in node:
            flat[key] = node[key]
    if "page_list" in node:
        flat["page"] = min(node["page_list"]) if node["page_list"] else None
    if "children" in node:
        sorted_children = sort_children(node["children"])
        flat["children"] = [flatten_tree(child) for child in sorted_children]
    return flat

def extract_sections(pdf_path):
    # Open PDF with both pdfplumber and fitz for formatting detection
    doc = fitz.open(pdf_path)
    with pdfplumber.open(pdf_path) as pdf:
        root = {"children": [], "paragraph": "", "page_list": []}

        current_section_numbers = None
        current_section_data = {"pages": [], "paragraph": ""}
        last_page_num = None

        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            lines = text.split("\n")

            # Extract formatting blocks from fitz for this page
            page_blocks = extract_bold_underline_blocks(doc, page_num)

            for idx, line in enumerate(lines):
                line_strip = line.strip()
                match = section_header_re.match(line_strip)
                if match:
                    # Flush previous section
                    if current_section_numbers is not None:
                        insert_section(root, current_section_numbers, current_section_data)
                    header = match.group("header").strip()
                    rest = match.group("rest") or ""
                    section_numbers = split_section_numbers(header)

                    # Extract title: only if the very next chunk after header is bold/underline/quoted in same line
                    # Try to extract the first token/phrase after header that is bold/underline or quoted
                    title_candidate = None
                    rest_strip = rest.strip()

                    # Check quoted
                    quoted = extract_quoted(rest_strip)
                    if quoted:
                        title_candidate = quoted
                        paragraph_part = rest_strip.replace(f'"{quoted}"', '').strip()
                    else:
                        # check bold/underline in page_blocks
                        # get first word or phrase after header on this line
                        words = rest_strip.split()
                        # We'll try incremental chunks from first word, adding words until bold/underline detected or no more words
                        title_candidate = None
                        for end in range(1, len(words)+1):
                            phrase = " ".join(words[:end])
                            if is_bold_underline_or_quoted(phrase, page_num, page_blocks):
                                title_candidate = phrase
                            else:
                                # stop if phrase not bold/underline and we already had title_candidate
                                if title_candidate is not None:
                                    break
                        paragraph_part = rest_strip[len(title_candidate):].strip() if title_candidate else rest_strip

                    current_section_numbers = section_numbers
                    current_section_data = {
                        "pages": [page_num],
                        "paragraph": paragraph_part,
                        "title": title_candidate if title_candidate else None,
                        "topic": None,
                    }
                    last_page_num = page_num

                    # If this is a top-level section (single number like "6" or "3"), mark topic
                    if len(section_numbers) == 1 and re.match(r"^\d+$", section_numbers[0]):
                        current_section_data["topic"] = current_section_data["title"]
                    continue

                # If line is not a section header, append to current paragraph if inside a section
                if current_section_numbers is not None:
                    if line_strip == "":
                        # Blank line, could indicate page end but we continue until next section
                        current_section_data["paragraph"] += "\n"
                    else:
                        current_section_data["paragraph"] += ("\n" if current_section_data["paragraph"] else "") + line_strip
                    # Track pages spanned by this section
                    if page_num != last_page_num:
                        current_section_data["pages"].append(page_num)
                        last_page_num = page_num

            # After last line of page, don't flush, continue to next page to catch spanning sections

        # Flush last section after all pages
        if current_section_numbers is not None:
            insert_section(root, current_section_numbers, current_section_data)

        return root

def save_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    pdf_path = "your_file.pdf"  # Change to your file path
    nested = extract_sections(pdf_path)
    nested_sorted = flatten_tree(nested)
    save_json(nested_sorted, "nested_sections.json")

    print("Extraction done, saved to nested_sections.json")
