import json
import os
from PyPDF2 import PdfReader
import fitz  # PyMuPDF for PDF parsing

def extract_text_from_pdf(pdf_path, page_number):
    """Extract text from a specific page of the PDF."""
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        page = reader.pages[page_number - 1]
        return page.extract_text()

def highlight_text_in_pdf(pdf_path, snippet, page_number):
    """Highlight a snippet of text in the PDF."""
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_number - 1)
    
    text_instances = page.search_for(snippet)
    
    for inst in text_instances:
        page.add_highlight_annot(inst)
    
    highlighted_pdf_path = f"uploads/highlighted_{os.path.basename(pdf_path)}"
    doc.save(highlighted_pdf_path)
    return highlighted_pdf_path

def process_multiple_references(reference_files):
    """Process multiple reference JSON files and generate output."""
    all_outputs = []
    for ref_file in reference_files:
        with open(ref_file, 'r') as f:
            data = json.load(f)
            for scenario in data['scenarios']:
                for question in scenario['questions']:
                    output = {
                        'pscrfId': data['pscrfId'],
                        'scenarioId': scenario['scenarioId'],
                        'questionId': question['questionId'],
                        'questionRefId': question['questionRefId'],
                        'fileName': data['fileName'],
                        'pageNumber': question['pageNumber'],
                        'snippet': question['answerText'],  # Assume this is the matched snippet
                        'accuracy': 95,  # Placeholder accuracy
                        'isValid': "yes"  # Placeholder validity
                    }
                    all_outputs.append(output)
    return all_outputs
