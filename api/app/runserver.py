import fitz  # PyMuPDF

def find_sentence_pages(pdf_path, sentence):
    doc = fitz.open(pdf_path)
    pages = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        
        # Normalize whitespace and lowercase for better matching
        page_text = ' '.join(text.lower().split())
        target_sentence = ' '.join(sentence.lower().split())

        if target_sentence in page_text:
            pages.append(page_num + 1)  # Page numbers are 1-indexed

    doc.close()
    return pages

# Example usage
pdf_file = "your_file.pdf"
search_sentence = "This is the full sentence you're searching for."
matched_pages = find_sentence_pages(pdf_file, search_sentence)

print(f"Sentence found on pages: {matched_pages}")
