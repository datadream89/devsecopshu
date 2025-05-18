import fitz  # PyMuPDF

def extract_toc(pdf_path):
    doc = fitz.open(pdf_path)
    toc = doc.get_toc()  # Returns a list of [level, title, page number]
    doc.close()
    return toc

if __name__ == "__main__":
    pdf_path = "your_file.pdf"  # Replace with your PDF file path
    toc = extract_toc(pdf_path)
    
    if not toc:
        print("No TOC found in this PDF.")
    else:
        for level, title, page in toc:
            print(f"Level {level}, Page {page}: {title}")
