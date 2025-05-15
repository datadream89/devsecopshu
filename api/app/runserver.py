import fitz  # PyMuPDF
import json
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate

# Initialize LLM
llm = Ollama(model="llama3")

# Prompt to detect definitions
definition_prompt = ChatPromptTemplate.from_messages([
    ("system", "You're an AI that finds definitions of terms in legal or regulatory documents."),
    ("human", """
Given the term: **{term}**
And the following paragraph:

"{paragraph}"

If this paragraph defines or explains the term, respond with:
{{
  "match": true,
  "definition": "..."
}}

Otherwise respond with:
{{
  "match": false
}}
""")
])

# Extract paragraphs with page numbers from PDF
def extract_paragraphs_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    paragraphs_with_pages = []
    for i in range(len(doc)):
        text = doc[i].get_text()
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        for para in paragraphs:
            paragraphs_with_pages.append({"text": para, "page": i+1})
    return paragraphs_with_pages

# Identify the paragraph that defines the term
def find_definition(term, pdf_path):
    paragraphs = extract_paragraphs_from_pdf(pdf_path)
    for p in paragraphs:
        prompt = definition_prompt.format_messages(term=term, paragraph=p["text"])
        try:
            result = llm.invoke(prompt)
            parsed = json.loads(result.strip())
            if parsed.get("match"):
                return {
                    "term": term,
                    "definition": parsed["definition"],
                    "pageNumber": p["page"],
                    "paragraph": p["text"]
                }
        except Exception as e:
            print(f"Error: {e}")
    return {"term": term, "definition": "Not found"}

# Example usage
if __name__ == "__main__":
    pdf_path = "document.pdf"
    term = "M20 RAG"
    result = find_definition(term, pdf_path)
    print(json.dumps(result, indent=2))
