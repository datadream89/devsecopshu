import json
from docx import Document

def is_bullet(para):
    return para.style.name and "List" in para.style.name

def extract_intermediate_json(docx_path, output_json_path):
    doc = Document(docx_path)
    result = []

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        entry = {
            "type": "bullet" if is_bullet(para) else "paragraph",
            "text": text
        }
        result.append(entry)

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Intermediate JSON saved to {output_json_path}")

# Example usage
if __name__ == "__main__":
    extract_intermediate_json("your_file.docx", "intermediate_output.json")
