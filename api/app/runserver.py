import subprocess
from pathlib import Path

def convert_docx_to_pdf(input_path):
    input_path = Path(input_path)
    output_dir = input_path.parent
    subprocess.run([
        "libreoffice", "--headless", "--convert-to", "pdf", str(input_path),
        "--outdir", str(output_dir)
    ], check=True)
    return str(output_dir / input_path.with_suffix(".pdf").name)

pdf_path = convert_docx_to_pdf("your_file.docx")              
