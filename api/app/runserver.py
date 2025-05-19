import json
import re
import pdfplumber

def get_pdf_lines(pdf_path):
    lines = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                for line in text.split('\n'):
                    lines.append(line.strip())
    return lines

def detect_prefix(text):
    text = text.strip()
    patterns = [
        (r'^(?P<prefix>\d{1,2}\.?)\s+(?P<content>.+)', 'numeric section'),
        (r'^(?P<prefix>\d{1,2}\.\d{1,2}\.?)\s+(?P<content>.+)', 'numeric subsection'),
        (r'^(?P<prefix>\(?[a-zA-Z]\)?)\s+(?P<content>.+)', 'alpha subsection'),
        (r'^(?P<prefix>\(?[ivxlcIVXLC]+\)?)\s+(?P<content>.+)', 'roman subsection'),
    ]
    for pattern, prefix_type in patterns:
        match = re.match(pattern, text)
        if match:
            return prefix_type, match.group('prefix'), match.group('content')
    return None, None, None

def match_and_update(json_path, pdf_path, updated_path):
    with open(json_path, "r", encoding="utf-8") as f:
        doc_data = json.load(f)

    pdf_lines = get_pdf_lines(pdf_path)

    def try_match_and_update(item):
        if item["type"] in ("paragraph", "bullet"):
            for line in pdf_lines:
                if item["text"].strip() in line:
                    prefix_type, prefix, content = detect_prefix(line)
                    if prefix_type and content.lower().startswith(item["text"].strip().lower()[:20]):
                        item["type"] = prefix_type
                        item["prefix"] = prefix
                        break
        return item

    updated_data = []
    for item in doc_data:
        if item["type"] == "table":
            updated_data.append(item)
        else:
            updated_data.append(try_match_and_update(item))

    with open(updated_path, "w", encoding="utf-8") as f:
        json.dump(updated_data, f, ensure_ascii=False, indent=2)

    return updated_data

# --- Usage ---
if __name__ == "__main__":
    input_json = "intermediate_docx_output.json"   # from previous step
    pdf_file = "your_input_file.pdf"               # your PDF file path
    output_json = "updated_with_pdf_prefix.json"   # updated output file

    result = match_and_update(input_json, pdf_file, output_json)

    import pprint
    pprint.pprint(result)
