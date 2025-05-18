from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import json

# Load PDF file
pdf = DocumentFile.from_pdf("your_file.pdf")  # Multi-page PDF

# Load OCR model (you can choose from pre-trained models)
model = ocr_predictor(pretrained=True)

# Perform OCR
result = model(pdf)

# Export to structured JSON
json_output = result.export()

# Save the output
with open("ocr_output.json", "w", encoding="utf-8") as f:
    json.dump(json_output, f, ensure_ascii=False, indent=2)

print("OCR extraction complete!")
