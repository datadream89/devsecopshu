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
    # Paragraph considered bold if any run is bold
    for run in para.runs:
        if run.text.strip() and is_bold(run):
            return True
    return False

def is_underlined_para(para):
    # Paragraph considered underlined if any run is underlined
    for run in para.runs:
        if run.text.strip() and is_underline(run):
            return True
    return False

def extract_sections_and_tables(doc_path):
    doc = Document(doc_path)
    output = []

    # Iterate paragraphs and tables in document order
    # docx doesn't provide direct interleaved access to paragraphs/tables,
    # so we iterate over all block-level elements using _body._body property

    body = doc.element.body
    for child in body.iterchildren():
        tag = child.tag.split('}')[1]  # localname

        if tag == 'p':  # paragraph
            para = Document().paragraphs._parent._element._element_to_obj(child)
            # But the above is complicated, so easier is to map index:
            # We'll iterate paragraphs normally and map indices.

            # So, instead we'll iterate doc.paragraphs and keep a pointer
            # to track where we are. Let's do that outside this loop.

    # Since above is complicated, we'll do a combined approach:
    # We get counts of paragraphs and tables, then interleave by their order in XML.

    # Get list of paragraphs and tables with their _element objects
    paras = list(doc.paragraphs)
    tables = list(doc.tables)

    # Create list of (element, type, index) where index is original position in body
    elems = []
    for i, child in enumerate(body.iterchildren()):
        tag = child.tag.split('}')[1]
        if tag == 'p':
            # Find paragraph with this element
            for idx, para in enumerate(paras):
                if para._element == child:
                    elems.append((para, 'p', idx))
                    break
        elif tag == 'tbl':
            for idx, table in enumerate(tables):
                if table._element == child:
                    elems.append((table, 'tbl', idx))
                    break

    # Now iterate elems in order
    for elem, typ, idx in elems:
        if typ == 'p':
            para = elem
            text = para.text.strip()
            if not text:
                continue

            alignment = para.paragraph_format.alignment
            align_val = alignment.value if alignment else None

            bold = is_bold_para(para)
            underlined = is_underlined_para(para)

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
    docx_path = "your_file.docx"  # Replace with your actual docx file path
    result = extract_sections_and_tables(docx_path)

    with open("doc_sections_tables.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print("Extracted document structure saved to doc_sections_tables.json")
