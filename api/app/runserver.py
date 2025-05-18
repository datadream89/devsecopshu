import fitz  # PyMuPDF

def extract_toc(pdf_path):
    doc = fitz.open(pdf_path)
    toc = doc.get_toc(simple=False)  # or simple=True for flat TOC
    # toc = [(level, title, page), ...]
    doc.close()
    return toc

pdf_path = "your_file.pdf"
toc = extract_toc(pdf_path)

for level, title, page in toc:
    print(f"Level: {level}, Title: {title}, Page: {page}")
