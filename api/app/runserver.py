# Install required packages before running:
# pip install transformers torchvision pytorch-lightning pdf2image
# Also install Poppler (https://blog.alivate.com.au/poppler-windows/) and add to system PATH

import json
from pdf2image import convert_from_path
from PIL import Image
import torch
from transformers import DonutProcessor, VisionEncoderDecoderModel

# Load Donut Processor and Model
processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base-finetuned-docvqa")
model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base-finetuned-docvqa")

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

def pdf_to_images(pdf_path, dpi=200):
    """Convert PDF to list of PIL images (one per page)."""
    return convert_from_path(pdf_path, dpi=dpi)

def run_donut_on_image(image: Image.Image) -> str:
    """Run Donut model on a single image and return output text."""
    task_prompt = "<s_docvqa><s_question>What is the document structure?</s_question><s_answer>"
    pixel_values = processor(image, return_tensors="pt").pixel_values.to(device)

    decoder_input_ids = processor.tokenizer(
        task_prompt, add_special_tokens=False, return_tensors="pt"
    ).input_ids.to(device)

    outputs = model.generate(
        pixel_values,
        decoder_input_ids=decoder_input_ids,
        max_length=512,
        early_stopping=True,
        pad_token_id=processor.tokenizer.pad_token_id,
        eos_token_id=processor.tokenizer.eos_token_id,
        use_cache=True
    )

    return processor.batch_decode(outputs, skip_special_tokens=True)[0]

def parse_pdf_to_structure(pdf_path: str):
    """Process all pages and return structured output."""
    images = pdf_to_images(pdf_path)
    document_structure = []

    for page_num, image in enumerate(images, start=1):
        try:
            result_text = run_donut_on_image(image)
            document_structure.append({
                "page": page_num,
                "structure": result_text
            })
        except Exception as e:
            document_structure.append({
                "page": page_num,
                "error": str(e)
            })

    return document_structure

if __name__ == "__main__":
    input_pdf = "input.pdf"  # Replace with your PDF filename
    output_json = "document_structure.json"

    structure = parse_pdf_to_structure(input_pdf)

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(structure, f, ensure_ascii=False, indent=2)

    print(f"Structure saved to: {output_json}")
