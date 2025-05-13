import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate

# Embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# LLM wrapper (LangChain + Ollama)
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
You are a helpful assistant that finds which page a sentence appears on.

Sentence:
"{sentence}"

Page {page_num} content:
\"\"\"
{text}
\"\"\"

Does this page contain the sentence (exactly or semantically)? 
If yes, respond with: Page {page_num}
If no, respond with: Not this page.
""")
    prompt = template.format(sentence=sentence, page_num=page['page'], text=page['text'])
    result = llm.invoke(prompt)
    return result.strip().lower()

def find_page(sentence, pdf_path):
    pages = extract_pages(pdf_path)
    top_pages = rank_pages_by_similarity(sentence, pages, top_k=3)

    for page in top_pages:
        result = run_llm_check(sentence, page)
        if f"page {page['page']}" in result:
            return page['page']
    return None

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python hybrid_langchain_ollama.py <pdf_path> <sentence>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    sentence = sys.argv[2]

    found_page = find_page(sentence, pdf_path)
    if found_page:
        print(f"Sentence found on page {found_page}")
    else:
        print("Sentence not found in the document.")
