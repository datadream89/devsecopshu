from docx import Document
import json

def is_bold_para(para):
    return any(run.bold for run in para.runs if run.text.strip())

def is_underline_para(para):
    return any(run.underline for run in para.runs if run.text.strip())

def get_left_indent_pts(para):
    if para.paragraph_format.left_indent:
        return para.paragraph_format.left_indent.pt
    return 0

def extract_sections_and_tables(doc_path):
    doc = Document(doc_path)
    output = []

    # Step 1: Collect all elements (paragraphs and tables) in document order
    body = doc.element.body
    p_idx, t_idx = 0, 0
    elements = []

    for child in body.iterchildren():
        tag = child.tag.split('}')[-1]
        if tag == 'p':
            elements.append(('p', doc.paragraphs[p_idx]))
            p_idx += 1
        elif tag == 'tbl':
            elements.append(('tbl', doc.tables[t_idx]))
            t_idx += 1

    # Step 2: Track indent level relatively
    indent_levels = []
    prev_indent = None
    current_level = 0

    for typ, elem in elements:
        if typ == 'p':
            para = elem
            text = para.text.strip()
            if not text:
                continue

            left_indent = get_left_indent_pts(para)
            align = para.paragraph_format.alignment
            align_val = align.value if align else None

            bold = is_bold_para(para)
            underline = is_underline_para(para)

            # Detect type
            if align_val == 1 and bold:
                para_type = "topic"
            elif align_val == 3 and bold and underline:
                para_type = "heading"
            else:
                para_type = "paragraph"

            # Relative indentation level
            if prev_indent is None:
                indent_level = 0
            else:
                if abs(left_indent - prev_indent) < 1:
                    indent_level = current_level
                elif left_indent > prev_indent:
                    current_level += 1
                    indent_level = current_level
                else:
                    current_level = max(0, current_level - 1)
                    indent_level = current_level

            prev_indent = left_indent

            output.append({
                "type": para_type,
                "text": text,
                "indent_level": indent_level,
                "alignment": {0: "left", 1: "center", 2: "right", 3: "justify"}.get(align_val, "none")
            })

        elif typ == 'tbl':
            # Table — just append without affecting indentation
            table_data = []
            for row in elem.rows:
                row_data = [cell.text.strip() for cell in row.cells]
                table_data.append(row_data)

            output.append({
                "type": "table",
                "data": table_data
            })

    return output

# --- Run ---
if __name__ == "__main__":
    docx_path = "your_file.docx"  # Replace with your .docx path
    result = extract_sections_and_tables(docx_path)

    with open("structured_doc.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print("Written to structured_doc.json")
