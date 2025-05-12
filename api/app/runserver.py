import fitz  # PyMuPDF
import spacy
from rapidfuzz import process, fuzz

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

def extract_sentences_with_page(pdf_path):
    doc = fitz.open(pdf_path)
    sentence_data = []

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()
        if not text.strip():
            continue

        spacy_doc = nlp(text)
        for sent in spacy_doc.sents:
            clean_sent = sent.text.strip()
            if clean_sent:
                sentence_data.append({
                    "page": page_num,
                    "text": clean_sent
                })

    return sentence_data

def search_best_match(pdf_path, search_query, max_words=None):
    sentences = extract_sentences_with_page(pdf_path)

    if not sentences:
        return None

    # Prepare list for matching
    search_list = [s["text"] for s in sentences]
    best_text, score, idx = process.extractOne(search_query, search_list, scorer=fuzz.token_set_ratio)

    match = sentences[idx]
    truncated_text = ' '.join(match["text"].split()[:max_words]) + ('...' if max_words and len(match["text"].split()) > max_words else '') if max_words else match["text"]

    return {
        "page": match["page"],
        "match": truncated_text,
        "score": score
    }

# Example usage
pdf_path = "your_document.pdf"
query = "How do I reset my password?"
result = search_best_match(pdf_path, query, max_words=25)
print(result)
