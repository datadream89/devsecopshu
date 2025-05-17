import pdfplumber
import re
import json

def extract_sections_by_paragraphs(pdf_path):
    # Pattern to match numbered section headers: "1", "1.1", "2.3.4 Title"
    section_pattern = re.compile(r'^\s*(\d+(\.\d+)*\.?)\s+(.+)')

    sections = {}
    current_section = None
    buffer = []

    def flush_section():
        """Process and store buffered lines into paragraphs for the current section."""
        if current_section and buffer:
            # Combine lines into a block and split on blank lines or multiple newlines
            raw_text = "\n".join(buffer).strip()
            paragraphs = [p.strip() for p in re.split(r'\n\s*\n', raw_text) if p.strip()]
            sections[current_section]["paragraphs"].extend(paragraphs)

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            lines = (page.extract_text() or '').split('\n')

            for line in lines:
                match = section_pattern.match(line)
                if match:
                    # Flush previous section
                    flush_section()
                    buffer = []

                    # Start new section
                    section_number = match.group(1).strip()
                    section_title = match.group(3).strip()
                    current_section = f"{section_number} {section_title}"

                    if current_section not in sections:
                        sections[current_section] = {
                            "pages": [page_num],
                            "paragraphs": [],
                            "tables": []
                        }
                elif current_section:
                    buffer.append(line)
                    if page_num not in sections[current_section]["pages"]:
                        sections[current_section]["pages"].append(page_num)

            # Tables from the current page
            tables = page.extract_tables()
            if current_section and tables:
                sections[current_section]["tables"].extend(tables)

    # Final flush
    flush_section()
    return sections

def save_to_json(data, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ====== USAGE ======
if __name__ == "__main__":
    pdf_file = "your_file.pdf"                 # Replace with your PDF path
    output_file = "sections_with_paragraphs.json"

    sections = extract_sections_by_paragraphs(pdf_file)
    save_to_json(sections, output_file)

    print(f"Done! Output saved to: {output_file}")
