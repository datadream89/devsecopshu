import re
from collections import deque
from doctr.documents import DocumentFile
from doctr.models import ocr_predictor

def get_level(text):
    numeric_pattern = re.compile(r'^(\d+(\.\d+)*)[.\s]')
    alpha_pattern = re.compile(r'^([a-zA-Z])[.\s]')
    roman_pattern = re.compile(r'^\(?([ivxlcdm]+)\)?[.\s]', re.IGNORECASE)

    if numeric_pattern.match(text):
        prefix = numeric_pattern.match(text).group(1)
        return prefix.count('.') + 1
    elif alpha_pattern.match(text):
        return 3
    elif roman_pattern.match(text):
        return 4
    else:
        return None

def parse_lines_to_hierarchy(lines):
    hierarchy = []
    stack = deque()

    for line in lines:
        text = line["text"].strip()
        level = get_level(text)

        node = {
            "text": text,
            "children": [],
            "page": line["page"],
            "bbox": line["bbox"],
        }

        if level is None:
            # Paragraph or continuation text - add under last section if any
            if stack:
                stack[-1]["children"].append(node)
            else:
                hierarchy.append(node)
            continue

        # Pop from stack until top has lower level than current
        while stack and get_level(stack[-1]["text"]) >= level:
            stack.pop()

        if stack:
            stack[-1]["children"].append(node)
        else:
            hierarchy.append(node)

        stack.append(node)

    return hierarchy

def ocr_and_extract_hierarchy(pdf_path):
    # Load pretrained doctr OCR model
    model = ocr_predictor(pretrained=True)

    # Load and OCR the document
    doc = DocumentFile.from_pdf(pdf_path)
    result = model(doc)

    lines = []
    for page_idx, page in enumerate(result.pages):
        for block in page.blocks:
            for line in block.lines:
                text = line.value
                bbox = line.geometry.to_list()  # [x1,y1,x2,y2]
                lines.append({
                    "text": text,
                    "bbox": bbox,
                    "page": page_idx
                })

    hierarchy = parse_lines_to_hierarchy(lines)
    return hierarchy

if __name__ == "__main__":
    pdf_path = "your_document.pdf"  # replace with your PDF path
    hierarchy = ocr_and_extract_hierarchy(pdf_path)

    import json
    with open("hierarchy_output.json", "w", encoding="utf-8") as f:
        json.dump(hierarchy, f, ensure_ascii=False, indent=2)

    print(json.dumps(hierarchy, indent=2, ensure_ascii=False))
