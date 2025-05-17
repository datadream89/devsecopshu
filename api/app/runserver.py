import pdfplumber
import re
import json

def extract_sections(pdf_path):
    # Match section identifiers like 1., 1.1, (a), A), "Title", etc.
    section_pattern = re.compile(
        r'^\s*(\(?[a-zA-Z0-9]+\)?)[\.\):]?\s*(["\']?.+?["\']?)?\s*$'
    )

    sections = {}
    current_section_number = None
    buffer = []

    def flush_section():
        """Flush the buffered lines into paragraphs under the current section."""
        if current_section_number and buffer:
            raw_text = "\n".join(buffer).strip()
            paragraphs = [p.strip() for p in re.split(r'\n\s*\n', raw_text) if p.strip()]
            sections[current_section_number]["paragraphs"].extend(paragraphs)

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            lines = (page.extract_text() or '').split('\n')

            for line in lines:
                match = section_pattern.match(line.strip())
                if match:
                    flush_section()
                    buffer = []

                    raw_number = match.group(1).strip("(). ")
                    raw_title = match.group(2)
                    title = raw_title.strip("\"' ") if raw_title else ""

                    current_section_number = raw_number

                    if current_section_number not in sections:
                        sections[current_section_number] = {
                            "section_title": title,
                            "pages": [page_num],
                            "paragraphs": [],
                            "tables": []
                        }
                elif current_section_number:
                    buffer.append(line)
                    if page_num not in sections[current_section_number]["pages"]:
                        sections[current_section_number]["pages"].append(page_num)

            # Capture tables for this page
            if current_section_number:
                tables = page.extract_tables()
                if tables:
                    sections[current_section_number]["tables"].extend(tables)

    # Final section
    flush_section()
    return sections

def save_to_json(data, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ==== USAGE ====
if __name__ == "__main__":
    pdf_file = "your_file.pdf"               # Replace with your PDF file
    output_file = "final_sectioned_output.json"

    data = extract_sections(pdf_file)
    save_to_json(data, output_file)
    print(f"Extraction complete. Output saved to: {output_file}")
