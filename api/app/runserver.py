import re
from docx import Document
import json

def bullet_is_subheading(para):
    import unicodedata

    raw_text = para.text
    # Normalize and replace non-breaking spaces with normal spaces
    text = para.text.replace('\u00A0', ' ').lstrip()
    text = unicodedata.normalize("NFKC", text)
    print(f"Checking paragraph text (repr): {repr(text)}")

    # Match number prefix like "1" or "1." optionally followed by whitespace
    prefix_match = re.match(r"^\s*(\d+\.?)\s*", text)
    if not prefix_match:
        print("No number prefix found.")
        return False

    prefix_len = len(prefix_match.group(0))
    print(f"Number prefix found: '{prefix_match.group(0)}' with length {prefix_len}")

    pos = 0
    for i, run in enumerate(para.runs):
        run_text = run.text or ""
        run_len = len(run_text)
        run_start = pos
        run_end = pos + run_len
        pos = run_end

        print(f"Run {i}: '{run_text}' from {run_start} to {run_end}, bold={run.bold}, underline={run.underline}")

        # Skip runs fully inside prefix (the number and whitespace)
        if run_end <= prefix_len:
            print(f"Run {i} is within prefix, skipping.")
            continue

        # For runs that start after prefix, check if any is bold and underlined
        if run_start >= prefix_len:
            if run_text.strip() and run.bold and run.underline:
                print("Found bold and underlined run after prefix - returning True")
                return True

    print("No bold and underlined run found after prefix - returning False")
    return False

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

    def is_subsection(para):
        # This function can stay as is or be adjusted if needed
        # For now, we just reuse bullet_is_subheading logic for bullets
        return bullet_is_subheading(para)

    def is_bold_underlined(para):
        for run in para.runs:
            if run.text.strip() and run.bold and run.underline:
                return True
        return False

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        alignment = para.paragraph_format.alignment  # 1 = center alignment
        is_bold = any(run.bold for run in para.runs if run.text.strip())

        # Detect Section (center aligned + bold)
        if alignment == 1 and is_bold:
            append_section()
            current_section["heading"] = text
            current_subsection = {"subheading": None, "content": []}
            continue

        # Detect Subsection based on bullet_is_subheading (bold & underlined after number prefix)
        if is_subsection(para):
            append_subsection()
            current_subsection = {"subheading": text, "content": []}
            continue

        # Determine Content Type
        if para.style.name and "List" in para.style.name:
            if is_bold_underlined(para):
                text_type = "heading"
            else:
                text_type = "bullet"
        else:
            text_type = "paragraph"

        current_subsection["content"].append({"type": text_type, "text": text})

    append_section()

    # Extract Tables and append them to the last subsection content if possible
    for table in doc.tables:
        table_data = []
        for row in table.rows:
            row_data = [cell.text.strip() for cell in row.cells]
            table_data.append(row_data)

        if hierarchy:
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

# --- Usage example ---
if __name__ == "__main__":
    docx_path = "your_file.docx"  # Replace with your docx file path
    result = extract_docx_hierarchy(docx_path)

    with open("docx_hierarchy.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    import pprint
    pprint.pprint(result)
