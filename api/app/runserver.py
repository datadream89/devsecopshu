import pytesseract
from pdf2image import convert_from_path
import cv2
import json
import re
from pytesseract import Output

# Path to tesseract executable (adjust if needed)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_from_pdf(pdf_path):
    pages = convert_from_path(pdf_path)
    result = []

    for page_num, page in enumerate(pages):
        image = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)
        data = pytesseract.image_to_data(image, output_type=Output.DICT)
        blocks = []

        num_items = len(data['text'])
        current_block = {"type": None, "text": "", "indent": 0, "page": page_num + 1}
        prev_left = 0
        prev_line_num = -1

        for i in range(num_items):
            text = data['text'][i].strip()
            conf = int(data['conf'][i])
            if not text or conf < 50:
                continue

            left = data['left'][i]
            top = data['top'][i]
            width = data['width'][i]
            height = data['height'][i]
            line_num = data['line_num'][i]

            # Estimate indentation based on left offset
            indent = left // 40

            if line_num != prev_line_num:
                if current_block['text']:
                    blocks.append(current_block)
                current_block = {"type": "paragraph", "text": "", "indent": indent, "page": page_num + 1}
                prev_line_num = line_num

            # Classification
            if text.isupper() and abs(left - image.shape[1]//2) < 100:
                current_block['type'] = "topic"
            elif re.match(r'^\s*1(\.|)\s+', text) and current_block['type'] != "topic":
                current_block['type'] = "heading"

            current_block['text'] += text + " "

        if current_block['text']:
            blocks.append(current_block)

        # Detect tables using contours
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if w > 100 and h > 50:  # Table-like structure
                roi = image[y:y+h, x:x+w]
                table_text = pytesseract.image_to_string(roi, config='--psm 6')
                blocks.append({
                    "type": "table",
                    "text": table_text.strip(),
                    "indent": 0,
                    "page": page_num + 1
                })

        result.extend(blocks)

    return result

# Usage
if __name__ == "__main__":
    import numpy as np
    pdf_path = "your_document.pdf"  # Replace with actual path
    output = extract_from_pdf(pdf_path)

    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print("Extraction complete. Output written to output.json")
