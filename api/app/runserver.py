from docx import Document
import json

def get_indent_level(left_indent, base_indent=36):
    if left_indent is None:
        return 0
    indent_pts = left_indent.pt if hasattr(left_indent, 'pt') else 0
    level = int(round(indent_pts / base_indent))
    return level

def is_bold(run):
    return run.bold is True

def is_underline(run):
    return run.underline is True

def is_bold_para(para):
    for run in para.runs:
        if run.text.strip() and is_bold(run):
            return True
    return False

def is_underline_para(para):
    for run in para.runs:
        if run.text.strip() and is_underline(run):
            return True
    return False

def extract_sections_and_tables(doc_path):
    doc = Document(doc_path)
    output = []

    # Collect all block-level elements (paras + tables) with their XML elements and indexes
    body = doc.element.body
    paras = list(doc.paragraphs)
    tables = list(doc.tables)

    elements = []
    p_idx = 0
    t_idx = 0

    for child in body.iterchildren():
        tag = child.tag.split('}')[1]
        if tag == 'p':
            para = paras[p_idx]
            p_idx += 1
            elements.append(('p', para))
        elif tag == 'tbl':
            table = tables[t_idx]
            t_idx += 1
            elements.append(('tbl', table))

    # Now process elements in order
    for typ, elem in elements:
        if typ == 'p':
            para = elem
            text = para.text.strip()
            if not text:
                continue

            alignment = para.paragraph_format.alignment
            align_val = alignment.value if alignment else None

            bold = is_bold_para(para)
            underlined = is_underline_para(para)

            indent_level = get_indent_level(para.paragraph_format.left_indent)

            if align_val == 1 and bold:  # center aligned and bold
                para_type = "topic"
            elif align_val == 3 and bold and underlined:  # justified and bold+underlined
                para_type = "heading"
            else:
                para_type = "paragraph"

            output.append({
                "type": para_type,
                "text": text,
                "indent_level": indent_level,
                "alignment": {0: "left",1: "center",2: "right",3: "justify"}.get(align_val, "none")
            })

        elif typ == 'tbl':
            table = elem
            table_data = []
            for row in table.rows:
                row_data = [cell.text.strip() for cell in row.cells]
                table_data.append(row_data)

            output.append({
                "type": "table",
                "data": table_data
            })

    return output


if __name__ == "__main__":
    docx_path = "your_file.docx"  # Replace with your actual file path
    result = extract_sections_and_tables(docx_path)

    with open("doc_sections_tables.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print("Done writing JSON output to doc_sections_tables.json")
