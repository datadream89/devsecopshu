import pdfplumber
import re

def extract_sections_with_tables(pdf_path):
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
                    sections[current_section] = {
                        "pages": [page_num],
                        "text": line,
                        "tables": []
                    }
                elif current_section:
                    sections[current_section]["text"] += "\n" + line
                    if page_num not in sections[current_section]["pages"]:
                        sections[current_section]["pages"].append(page_num)

            # Extract tables from this page
            tables = page.extract_tables()
            if current_section and tables:
                for table in tables:
                    sections[current_section]["tables"].append(table)

    return sections

# Example usage
pdf_file = "your_file.pdf"
sections = extract_sections_with_tables(pdf_file)

# Display extracted content
for title, data in sections.items():
    print(f"\nSection: {title} (Pages: {data['pages']})")
    print("Text Preview:", data["text"][:200], "...")
    print("Tables Found:", len(data["tables"]))
