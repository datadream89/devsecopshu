import cv2
import pytesseract
from pdf2image import convert_from_path
import os
import json

# Optional: path to tesseract if not in PATH
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def detect_text_blocks(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)

    # Dilate to merge text into blocks
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 3))
    dilated = cv2.dilate(binary, kernel, iterations=2)

    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    blocks = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if h > 20 and w > 50:
            roi = image[y:y+h, x:x+w]
            text = pytesseract.image_to_string(roi, config="--psm 6").strip()
            if len(text) > 2:
                blocks.append({
                    "text": text,
                    "bbox": [int(x), int(y), int(w), int(h)]
                })
    return sorted(blocks, key=lambda b: b["bbox"][1])  # sort top-down

def process_pdf_with_opencv(pdf_path):
    pages = convert_from_path(pdf_path, dpi=300)
    result = []

    for i, page in enumerate(pages):
        image_path = f"page_{i}.png"
        page.save(image_path, 'PNG')
        image = cv2.imread(image_path)

        blocks = detect_text_blocks(image)
        result.append({
            "page": i + 1,
            "blocks": blocks
        })
        os.remove(image_path)

    return result

if __name__ == "__main__":
    pdf_path = "your_file.pdf"  # Replace with your PDF file
    output = process_pdf_with_opencv(pdf_path)

    with open("sections_extracted.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print("Sections extracted using OpenCV and saved to sections_extracted.json")
