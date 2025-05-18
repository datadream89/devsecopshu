from docx import Document
import json

def extract_docx_hierarchy(doc_path):
    doc = Document(doc_path)
    hierarchy = []
    current_section = {"heading": None, "subsections": []}
    current_subsection = {"subheading": None, "content": []}

    def append_subsection():
        if current_subsection["subheading"] or current_subsection["content"]:
            current_section["subsections"].append(current_subsection.copy())
            current_subsection["content"] = []

    def append_section():
        append_subsection()
        if current_section["heading"] or current_section["subsections"]:
            hierarchy.append(current_section.copy())
            current_section["subsections"] = []

    para_iter = iter(doc.paragraphs)
    for para in para_iter:
        style = para.style.name
        text = para.text.strip()

        if style.startswith('Heading 1'):
            append_section()
            current_section["heading"] = text
            current_section["subsections"] = []
            current_subsection = {"subheading": None, "content": []}

        elif style.startswith('Heading 2'):
            append_subsection()
            current_subsection = {"subheading": text, "content": []}

        elif 'List' in style:
            current_subsection["content"].append({"type": "bullet", "text": text})

        elif text:
            current_subsection["content"].append({"type": "paragraph", "text": text})

    # Append any remaining content
    append_section()

    # Add tables globally or inside the last known context (you can enhance this to insert per position)
    for table in doc.tables:
        table_data = []
        for row in table.rows:
            row_data = [cell.text.strip() for cell in row.cells]
            table_data.append(row_data)
        if hierarchy:
            # Add to last subsection of the last section
            if hierarchy[-1]["subsections"]:
                hierarchy[-1]["subsections"][-1]["content"].append({"type": "table", "data": table_data})
            else:
                hierarchy[-1]["subsections"].append({
                    "subheading": None,
                    "content": [{"type": "table", "data": table_data}]
                })
        else:
            hierarchy.append({
                "heading": None,
                "subsections": [{
                    "subheading": None,
                    "content": [{"type": "table", "data": table_data}]
                }]
            })

    return hierarchy

# Example usage
if __name__ == "__main__":
    docx_path = "your_file.docx"
    result = extract_docx_hierarchy(docx_path)

    # Save to JSON
    with open("docx_hierarchy.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # Optionally print
    import pprint
    pprint.pprint(result)
