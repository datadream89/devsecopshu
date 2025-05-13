import fitz  # PyMuPDF
import requests
import sys
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load sentence embedding model
model_embed = SentenceTransformer("all-MiniLM-L6-v2")

def extract_pages(pdf_path):
    doc = fitz.open(pdf_path)
    return [{'page': i + 1, 'text': doc[i].get_text().strip()} for i in range(len(doc))]

def rank_pages_by_similarity(sentence, pages, top_k=3):
    sentence_vec = model_embed.encode([sentence])
    page_vecs = model_embed.encode([page['text'] for page in pages])

    similarities = cosine_similarity(sentence_vec, page_vecs)[0]
    ranked_pages = sorted(zip(pages, similarities), key=lambda x: x[1], reverse=True)
    return [item[0] for item in ranked_pages[:top_k]]

def ask_ollama_for_page(sentence, pages, model='llama3'):
    for page in pages:
        prompt = f"""
You are given a page from a PDF.

Your task is to determine if the following sentence appears on this page, either exactly or with similar meaning.

Sentence:
"{sentence}"

Page {page['page']} content:
\"\"\"
{page['text']}
\"\"\"

If this page contains the sentence, respond with: Page {page['page']}
If not, respond with: Not this page.
"""
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            }
        )
        reply = response.json()['response'].strip().lower()
        if f"page {page['page']}" in reply:
            return page['page']
    return None

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python hybrid_llm_with_embeddings.py <pdf_path> <sentence>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    sentence = sys.argv[2]

    pages = extract_pages(pdf_path)
    top_pages = rank_pages_by_similarity(sentence, pages, top_k=3)
    result = ask_ollama_for_page(sentence, top_pages)

    if result:
        print(f"Sentence found on page {result}")
    else:
        print("Sentence not found in the document.")
