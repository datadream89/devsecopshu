from docx import Document
import json

def alignment_to_str(alignment):
    if alignment is None:
        return "None"
    mapping = {
        0: "Left",
        1: "Center",
        2: "Right",
        3: "Justify"
    }
    return mapping.get(alignment.value, "Unknown")

def get_font_info(run):
    font = run.font
    return {
        "text": run.text,
        "name": font.name,
        "size": font.size.pt if font.size else None,
        "bold": font.bold,
        "italic": font.italic,
        "underline": font.underline,
        "color": font.color.rgb.hex if font.color and font.color.rgb else None
    }

docx_path = 'your_file.docx'  # Replace with your file

doc = Document(docx_path)

paragraphs_data = []

for para in doc.paragraphs:
    para_text = para.text
    para_style = para.style.name if para.style else None
    para_alignment = alignment_to_str(para.paragraph_format.alignment)

    runs_info = [get_font_info(run) for run in para.runs]

    paragraphs_data.append({
        "text": para_text,
        "style": para_style,
        "alignment": para_alignment,
        "runs": runs_info
    })

# Save to JSON file
with open('paragraphs_output.json', 'w', encoding='utf-8') as f:
    json.dump(paragraphs_data, f, ensure_ascii=False, indent=2)

print("Paragraph data with font info saved to paragraphs_output.json")
