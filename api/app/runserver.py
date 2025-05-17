import pdfplumber
import re
import json

def extract_sections_split_lines(pdf_path):
    # Regex for section and subsection headers like 1, 1.1, 2.3.4 Title
    section_pattern = re.compile(r'^\s*(\d+(\.\d+)*\.?)\s+([A-Z][^\n]{2,})')

    sections = {}
    current_section = None

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ''
            lines = text.split('\n')

            for line in lines:
                match = section_pattern.match(line)
                if match:
                    section_number = match.group(1).strip()
                    section_title = match.group(3).strip()
                    current_section = f"{section_number} {section_title}"
                    if current_section not in sections:
                        sections[current_section] = {
                            "pages": [page_num],
                            "lines": [line],
                            "tables": []
                        }
                elif current_section:
                    sections[current_section]["lines"].append(line)
                    if page_num not in sections[current_section]["pages"]:
                        sections[current_section]["pages"].append(page_num)

            # Extract tables and add to current section
            tables = page.extract_tables()
            if current_section and tables:
                sections[current_section]["tables"].extend(tables)

    return sections

def save_to_json(data, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ========== USAGE ==========
if __name__ == "__main__":
    pdf_file = "your_file.pdf"               # <-- Replace with your PDF path
    output_file = "split_sections_output.json"

    sections = extract_sections_split_lines(pdf_file)
    save_to_json(sections, output_file)

    print(f"Extraction complete. Output saved to '{output_file}'")
