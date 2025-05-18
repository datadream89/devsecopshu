import json
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

def extract_docx_structure(doc_path):
    doc = Document(doc_path)
    output = []

    def is_bold(run): return run.bold is True
    def is_underline(run): return run.underline is True
    def is_bold_and_underline(run): return is_bold(run) and is_underline(run)

    for block in doc.element.body:
        if block.tag.endswith('tbl'):
            # Table processing
            table = doc.tables[doc.element.body.index(block)]
            table_data = []
            for row in table.rows:
                table_data.append([cell.text.strip() for cell in row.cells])
            output.append({"type": "table", "data": table_data})
        elif block.tag.endswith('p'):
            para = Document().paragraphs._paragraph_from_xml(block, doc)
            text = para.text.strip()
            if not text:
                continue

            # Detect topic (centered + bold)
            alignment = para.paragraph_format.alignment
            is_centered = alignment == WD_PARAGRAPH_ALIGNMENT.CENTER
            # Check if entire paragraph is bold (all runs bold)
            all_bold = all(is_bold(run) for run in para.runs if run.text.strip())

            if is_centered and all_bold:
                output.append({"type": "topic", "text": text})
                continue

            # Check start runs for heading or subheading
            runs = para.runs
            # Find first non-empty run index
            first_non_empty_run_idx = next((i for i, r in enumerate(runs) if r.text.strip()), None)
            if first_non_empty_run_idx is None:
                output.append({"type": "paragraph", "text": text})
                continue

            # Identify if paragraph starts with bold+underline run(s) (heading)
            # or underline but not bold (subheading)
            # We look at runs from start to find consecutive runs matching that style
            i = first_non_empty_run_idx
            heading_runs = []
            subheading_runs = []
            while i < len(runs) and runs[i].text.strip():
                run = runs[i]
                if is_bold_and_underline(run):
                    heading_runs.append(run)
                elif is_underline(run) and not is_bold(run):
                    subheading_runs.append(run)
                else:
                    break
                i += 1

            if heading_runs:
                # Heading: full paragraph as heading text
                output.append({"type": "heading", "text": text})
                continue

            if subheading_runs:
                # Subheading is only the underlined part at start (concatenate their texts)
                subheading_text = "".join(run.text for run in subheading_runs).strip()
                # The rest of paragraph after those runs is paragraph content
                rest_text = "".join(run.text for run in runs[i:]).strip()
                entry = {"type": "subheading", "text": subheading_text}
                if rest_text:
                    entry["content"] = [{"type": "paragraph", "text": rest_text}]
                output.append(entry)
                continue

            # If none of above, bullet or paragraph — we treat lists as bullets, else paragraphs
            style_name = para.style.name if para.style else ""
            if "List" in style_name or "Bullet" in style_name:
                output.append({"type": "bullet", "text": text})
            else:
                output.append({"type": "paragraph", "text": text})

    return output

if __name__ == "__main__":
    docx_path = "your_file.docx"  # Replace with your DOCX file path
    result = extract_docx_structure(docx_path)

    with open("docx_output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    import pprint
    pprint.pprint(result)
