import fitz  # PyMuPDF
import uuid
import os

def highlight_pdf(pdf_path, snippets):
    """
    Highlight the snippets in the PDF and create a new PDF with only the highlighted pages.

    :param pdf_path: Path to the input PDF file
    :param snippets: List of dictionaries containing matched snippets with page numbers and highlighted text
    :return: Path to the newly saved PDF with highlighted pages
    """
    doc = fitz.open(pdf_path)
    highlighted_pages = []

    for snippet in snippets:
        page_num = snippet["pageNumber"] - 1  # Page numbers in PyMuPDF are 0-based
        matched_snippet = snippet["matchedSnippet"]
        
        if len(matched_snippet) > 10:  # Ensure we have a valid snippet to highlight
            page = doc.load_page(page_num)
            for part in matched_snippet.split(". "):
                part = part.strip()
                if part in page.get_text():
                    for area in page.search_for(part):
                        highlight = page.add_highlight_annot(area)
                        highlight.update()
            
            if page_num not in highlighted_pages:
                highlighted_pages.append(page_num)

    # Save the newly created highlighted PDF with only the pages containing highlights
    unique_name = f"highlighted_{uuid.uuid4().hex[:8]}.pdf"
    highlighted_path = os.path.join("pdfs", unique_name)
    
    # Create a new document with only highlighted pages
    highlighted_doc = fitz.open()
    for page_num in highlighted_pages:
        highlighted_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)

    highlighted_doc.save(highlighted_path)
    return highlighted_path
