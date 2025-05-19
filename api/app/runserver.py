import json
from docx import Document

def is_bullet(para):
    return para.style.name and "List" in para.style.name

def extract_docx_with_tables(docx_path, output_json_path):
    doc = Document(docx_path)
    result = []
    para_iter = iter(doc.paragraphs)
    table_iter = iter(doc.tables)

    p_index = 0
    t_index = 0
    total_paras = len(doc.paragraphs)
    total_tables = len(doc.tables)

    while p_index < total_paras or t_index < total_tables:
        # Check the next element's position
        next_para = doc.paragraphs[p_index] if p_index < total_paras else None
        next_table = doc.tables[t_index] if t_index < total_tables else None

        para_pos = next_para._element.getparent().index(next_para._element) if next_para else float('inf')
        table_pos = next_table._element.getparent().index(next_table._element) if next_table else float('inf')

        if para_pos < table_pos:
            # Process paragraph
            text = next_para.text.strip()
            if text:
                entry = {
                    "type": "bullet" if is_bullet(next_para) else "paragraph",
                    "text": text
                }
                result.append(entry)
            p_index += 1
        else:
            # Process table
            table_data = []
            for row in next_table.rows:
                table_data.append([cell.text.strip() for cell in row.cells])
            result.append({
                "type": "table",
                "data": table_data
            })
            t_index += 1

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Intermediate JSON with tables saved to {output_json_path}")

# --- Example Usage ---
if __name__ == "__main__":
    extract_docx_with_tables("your_file.docx", "intermediate_output.json")
