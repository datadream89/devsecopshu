import pdfplumber
import re
import json

def extract_sections_by_paragraph(pdf_path):
    # Match headers like "1", "1.1", "2.3.4 Title"
    section_pattern = re.compile(r'^\s*(\d+(\.\d+)*\.?)\s+([A-Z][^\n]{2,})')

    sections = {}
    current_section = None
    buffer = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ''
            lines = text.split('\n')

            for line in lines:
                match = section_pattern.match(line)
                if match:
                    # Save previous section content if exists
                    if current_section and buffer:
                        sections[current_section]["paragraphs"].extend(
                            [p.strip() for p in "\n".join(buffer).split('\n\n') if p.strip()]
                        )
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
                    buffer.append(line)
                elif current_section:
                    if page_num not in sections[current_section]["pages"]:
                        sections[current_section]["pages"].append(page_num)
                    buffer.append(line)

            # Extract tables
            tables = page.extract_tables()
            if current_section and tables:
                sections[current_section]["tables"].extend(tables)

        # Save the last section content
        if current_section and buffer:
            sections[current_section]["paragraphs"].extend(
                [p.strip() for p in "\n".join(buffer).split('\n\n') if p.strip()]
            )

    return sections

def save_to_json(data, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ========== USAGE ==========
if __name__ == "__main__":
    pdf_file = "your_file.pdf"               # Replace with your file
    output_file = "section_paragraph_output.json"

    sections = extract_sections_by_paragraph(pdf_file)
    save_to_json(sections, output_file)

    print(f"Extraction complete. Output saved to '{output_file}'")
