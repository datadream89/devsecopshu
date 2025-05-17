import pdfplumber
import re
import json

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

    # Consider uppercase or titlecase short text as title
    if text and (text.isupper() or (text.istitle() and len(text.split()) <= 6)):
        return text, ""

    return None, remainder

# Regex to match full section headers:
# e.g. 1.  1.1.  2.6.4.  a.  (a)
section_header_re = re.compile(
    r"""^\s*
    (?P<header>
        (?:\d+(?:\.\d+)*\.)     # e.g. 1. or 1.1. or 2.6.4.
        | [a-zA-Z]\.            # e.g. a. or B.
        | \([a-zA-Z0-9]+\)      # e.g. (a), (1)
    )
    \s*
    (?P<rest>.*)?$
    """, re.VERBOSE
)

def is_top_level_section(header):
    return bool(re.match(r"^\d+\.$", header))

def split_section_numbers(header):
    # Remove trailing dot, then split by dot
    # "1.2.3." -> ['1','2','3']
    h = header.rstrip('.')
    if header.startswith('(') and header.endswith(')'):
        # e.g. (a) keep as one part
        return [header]
    if re.match(r"^[a-zA-Z]\.$", header):
        # e.g. a. keep as one part
        return [header]
    parts = h.split('.')
    return parts

def insert_section(root, section_numbers, section_data):
    current = root
    for i, part in enumerate(section_numbers):
        if "children" not in current:
            current["children"] = {}
        if part not in current["children"]:
            # Create new nested section node
            current["children"][part] = {
                "section_header": part + ('.' if not part.endswith('.') else ''),
                "paragraph": "",
            }
        current = current["children"][part]

        # At last part, update section_data keys
        if i == len(section_numbers) - 1:
            # Merge info (page, topic, section_title, paragraph)
            for k, v in section_data.items():
                if k == "paragraph":
                    current[k] += (v + "\n")
                else:
                    current[k] = v

def flatten_tree(tree):
    # Convert nested dict children into list with sorted keys
    def helper(node):
        res = {}
        for k in ("page", "section_header", "topic", "section_title", "paragraph"):
            if k in node:
                if k == "paragraph":
                    res[k] = node[k].strip()
                else:
                    res[k] = node[k]
        if "children" in node:
            res["children"] = []
            for key in sorted(node["children"].keys(), key=lambda x: (len(x), x)):
                res["children"].append(helper(node["children"][key]))
        return res
    return helper(tree)

def extract_sections(pdf_path):
    root = {
        "section_header": "root",
        "paragraph": "",
        "children": {}
    }

    current_section_numbers = None
    current_section_data = {}
    buffer = []

    def flush():
        nonlocal current_section_numbers, current_section_data, buffer
        if current_section_numbers:
            current_section_data["paragraph"] = "\n".join(buffer).strip()
            insert_section(root, current_section_numbers, current_section_data)
        buffer = []
        current_section_numbers = None
        current_section_data = {}

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            lines = text.split("\n")
            for line in lines:
                line = line.strip()
                match = section_header_re.match(line)
                if match:
                    flush()

                    header = match.group("header").strip()
                    rest_of_line = match.group("rest") or ""

                    current_section_numbers = split_section_numbers(header)
                    current_section_data = {
                        "page": page_num,
                        "section_header": header
                    }

                    title, rest = extract_title_and_rest(rest_of_line)
                    if title:
                        if is_top_level_section(header):
                            current_section_data["topic"] = title
                        else:
                            current_section_data["section_title"] = title
                    if rest:
                        buffer.append(rest)
                else:
                    if current_section_numbers:
                        buffer.append(line)

        flush()

    # Flatten root children to list/tree structure
    return flatten_tree(root)

def save_to_json(data, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# === Example usage ===
if __name__ == "__main__":
    pdf_path = "your_file.pdf"  # Replace with your PDF file path
    output_path = "nested_sections.json"

    nested_sections = extract_sections(pdf_path)
    save_to_json(nested_sections, output_path)

    print(f"Done. Nested output saved to {output_path}")
