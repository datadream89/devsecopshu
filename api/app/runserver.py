import fitz  # PyMuPDF
from rapidfuzz import process, fuzz
import re

def extract_sentences(text):
    # Simple sentence splitter (can be improved with NLP if needed)
    return re.split(r'(?<=[.!?]) +', text)

def search_fuzzy_sentence(pdf_path, search_query):
    doc = fitz.open(pdf_path)
    results = []

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()
        sentences = extract_sentences(text)
        if not sentences:
            continue
        
        # Get the closest match
        match, score, _ = process.extractOne(search_query, sentences, scorer=fuzz.token_set_ratio)
        results.append({
            "page": page_num,
            "match": match,
            "score": score
        })

    # Return the best overall match
    best_match = max(results, key=lambda x: x["score"], default=None)
    return best_match

# Example usage
pdf_path = "your_document.pdf"
query = "How can I reset my password?"

result = search_fuzzy_sentence(pdf_path, query)
print(result)
