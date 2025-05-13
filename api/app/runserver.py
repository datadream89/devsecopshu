import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
import difflib
import sys

# Load embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Load LLM from Ollama via LangChain
llm = Ollama(model="llama3")

def extract_pages(pdf_path):
    doc = fitz.open(pdf_path)
    return [{'page': i + 1, 'text': doc[i].get_text().strip()} for i in range(len(doc))]

def rank_pages_by_similarity(sentence, pages, top_k=3):
    sentence_vec = embedder.encode([sentence])
    page_vecs = embedder.encode([page['text'] for page in pages])
    similarities = cosine_similarity(sentence_vec, page_vecs)[0]
    ranked = sorted(zip(pages, similarities), key=lambda x: x[1], reverse=True)
    return [item[0] for item in ranked[:top_k]]

def run_llm_check(sentence, page):
    template = PromptTemplate.from_template("""
You are an assistant that determines whether a specific sentence appears on a given page of text, and retrieves the closest matching sentence if found.

Sentence to find:
"{sentence}"

Page {page_num} content:
\"\"\"
{text}
\"\"\"

Instructions:
1. Does the sentence appear on this page (either exact or semantically)? Reply "yes" or "no".
2. If "yes", provide the most similar sentence as-is from the page content.

Format your response like this:
Found: yes
Match: <most similar sentence>

Or, if not found:
Found: no
Match: none
""")
    prompt = template.format(sentence=sentence, page_num=page['page'], text=page['text'])
    response = llm.invoke(prompt).strip()
    return response

def parse_llm_response(response):
    lines = response.lower().splitlines()
    found = 'no'
    match = None

    for line in lines:
        if line.startswith('found:'):
            found = line.split(':', 1)[1].strip()
        elif line.startswith('match:'):
            match_text = line.split(':', 1)[1].strip()
            match = match_text if match_text != "none" else None
    return found == 'yes', match

def find_page(sentence, pdf_path):
    pages = extract_pages(pdf_path)
    top_pages = rank_pages_by_similarity(sentence, pages, top_k=3)

    for page in top_pages:
        response = run_llm_check(sentence, page)
        found, match = parse_llm_response(response)
        if found:
            return {
                "found": True,
                "page": page['page'],
                "matched_sentence": match
            }

    return {
        "found": False,
        "page": None,
        "matched_sentence": None
    }

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python hybrid_langchain_ollama.py <pdf_path> <sentence>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    sentence = sys.argv[2]

    result = find_page(sentence, pdf_path)
    print(result)
