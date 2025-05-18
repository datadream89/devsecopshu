import pytesseract
from pdf2image import convert_from_path
import cv2
import os
import json

# Set tesseract path if not in PATH
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_headings_from_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    d = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)

    headings = []
    for i in range(len(d['text'])):
        text = d['text'][i].strip()
        font_size = int(d['height'][i])
        conf = int(d['conf'][i])
        
        # Skip low-confidence or short text
        if len(text) < 3 or conf < 60:
            continue

        # Heuristics: larger font or "Table" / numeric prefixes => heading
        if font_size > 15 or text.lower().startswith(("table", "chapter", "section", "1", "2", "3")):
            headings.append({
                "text": text,
                "left": d['left'][i],
                "top": d['top'][i],
                "font_size": font_size,
                "confidence": conf
            })

    return headings

def process_pdf(pdf_path):
    pages = convert_from_path(pdf_path, dpi=300)
    all_headings = []

    for idx, page in enumerate(pages):
        image_path = f"page_{idx}.png"
        page.save(image_path, 'PNG')
        image = cv2.imread(image_path)
        headings = extract_headings_from_image(image)
        all_headings.append({
            "page": idx + 1,
            "headings": headings
        })
        os.remove(image_path)  # cleanup

    return all_headings

if __name__ == "__main__":
    pdf_file = "your_file.pdf"  # Replace with your file
    result = process_pdf(pdf_file)

    # Write to JSON
    with open("document_toc.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print("Extracted headings written to document_toc.json")
