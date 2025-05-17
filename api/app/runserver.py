import pdfplumber
import re
import json

def extract_sections_with_tables(pdf_path):
    # Regex for section headers (e.g., 1, 1.1, 2.3.4 Introduction)
    section_pattern = re.compile(r'^\s*(\d+(\.\d+)*\.?)\s+([A-Z][^\n]{2,})')

    sections = {}
    current_section = None

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            # Extract text
            text = page.extract_text() or ''
            lines = text.split('\n')

            # Process each line to find section headers
            for line in lines:
                match = section_pattern.match(line)
                if match:
                    section_number = match.group(1).strip()
                    section_title = match.group(3).strip()
                    current_section = f"{section_number} {section_title}"
                    sections[current_section] = {
                        "pages": [page_num],
                        "text": line,
                        "tables": []
                    }
                elif current_section:
                    sections[current_section]["text"] += "\n" + line
                    if page_num not in sections[current_section]["pages"]:
                        sections[current_section]["pages"].append(page_num)

            # Extract tables from current page
            tables = page.extract_tables()
            if current_section and tables:
                for table in tables:
                    sections[current_section]["tables"].append(table)

    return sections

def save_sections_to_json(sections, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(sections, f, indent=2, ensure_ascii=False)

# ======== Main ========
if __name__ == "__main__":
    pdf_file = "your_file.pdf"               # Replace with your PDF file path
    output_file = "extracted_sections.json"  # Output JSON

    sections = extract_sections_with_tables(pdf_file)
    save_sections_to_json(sections, output_file)

    print(f"Extraction complete. Sections saved to '{output_file}'")
