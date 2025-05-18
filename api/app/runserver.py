from docx import Document
from docx.shared import Pt
import json

def get_indent_level(left_indent, base_indent=36):
    if left_indent is None:
        return 0
    indent_pts = left_indent.pt if hasattr(left_indent, 'pt') else 0
    level = int(round(indent_pts / base_indent))
    return level

def is_bold_and_underlined(para):
    for run in para.runs:
        if run.text.strip() and run.bold and run.underline:
            return True
    return False

def get_alignment_str(alignment):
    if alignment is None:
        return "None"
    mapping = {
        0: "left",
        1: "center",
        2: "right",
        3: "justify"
    }
    return mapping.get(alignment.value, "unknown")

def extract_sections(doc_path):
    doc = Document(doc_path)
    sections = []

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        alignment = para.paragraph_format.alignment
        align_str = get_alignment_str(alignment)
        indent_level = get_indent_level(para.paragraph_format.left_indent)

        if is_bold_and_underlined(para):
            if align_str == "center":
                para_type = "topic"
            elif align_str == "justify":
                para_type = "heading"
            else:
                para_type = "paragraph"
        else:
            para_type = "paragraph"

        sections.append({
            "text": text,
            "type": para_type,
            "indent_level": indent_level,
            "alignment": align_str
        })

    return sections

if __name__ == "__main__":
    docx_path = "your_file.docx"  # Replace with your file path
    result = extract_sections(docx_path)

    with open("sections_output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("Extracted paragraphs with types and indent levels saved in sections_output.json")
