import json
import fitz  # PyMuPDF
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate

# Load input data
with open("sentence.json") as f:
    sentence_data = json.load(f)

with open("pscrf.json") as f:
    pscrf_data = json.load(f)

pdf_path = "document.pdf"

# Load PDF with fitz
def extract_pdf_text(pdf_path):
    doc = fitz.open(pdf_path)
    return [{"pageNumber": i + 1, "text": doc.load_page(i).get_text()} for i in range(doc.page_count)]

pages = extract_pdf_text(pdf_path)

# Load LLaMA model
llm = Ollama(model="llama3")

# Prompt to select top N relevant pages for a statement
selector_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are helping match a statement to the most relevant pages of a PDF."),
    ("human", """
Given the following statement and PDF pages, identify the top 3 most relevant page numbers.

Statement: {statement}

PDF Pages:
{page_list}

Respond only with a list of the 3 most relevant page numbers in JSON format, like this:
{{ "top_pages": [3, 5, 9] }}
""")
])

# Prompt to verify if a specific page supports the statement
verify_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a compliance analyst evaluating if a statement is supported by a PDF page."),
    ("human", """
Given the following statement and page content, determine if the page supports the statement.

Statement:
{statement}

Page {pageNumber} Content:
{pageContent}

Respond in JSON:
{{
  "match": true or false,
  "answer": "Yes" or "No" or "Uncertain",
  "excerpt": "Relevant excerpt if match is true"
}}
""")
])

outcome_list = []

# Create string of pages for LLM
def format_pages_for_llm(pages, max_chars=10000):
    chunks = []
    chunk = ""
    for page in pages:
        entry = f"Page {page['pageNumber']}: {page['text'].strip()[:800]}"
        if len(chunk) + len(entry) > max_chars:
            chunks.append(chunk)
            chunk = ""
        chunk += entry + "\n\n"
    chunks.append(chunk)
    return chunks

formatted_chunks = format_pages_for_llm(pages)

# Main loop
for scenario in pscrf_data["scenarios"]:
    for question in scenario["questions"]:
        qref = question["questionRefId"]
        sentence_entry = next((q for q in sentence_data["questions"] if q["questionRefId"] == qref), None)
        if not sentence_entry:
            continue

        outcome_entry = {
            "pscrfId": pscrf_data["pscrfId"],
            "scenarioId": scenario["scenarioId"],
            "questionId": question["questionId"],
            "questionRefId": qref,
            "questionDesc": sentence_entry["questionDesc"],
            "pdfFileName": pdf_path,
            "results": []
        }

        for statement in sentence_entry["statements"]:
            # Ask LLM to pick top N pages
            response = llm.invoke(selector_prompt.format_messages(statement=statement, page_list=formatted_chunks[0]))
            try:
                page_numbers = json.loads(response.strip())["top_pages"]
            except:
                continue

            # Evaluate selected pages
            for pnum in page_numbers:
                page = next((p for p in pages if p["pageNumber"] == pnum), None)
                if not page:
                    continue

                msg = verify_prompt.format_messages(
                    statement=statement,
                    pageNumber=page["pageNumber"],
                    pageContent=page["text"][:4000]
                )

                try:
                    resp = llm.invoke(msg)
                    parsed = json.loads(resp.strip())
                    if parsed.get("match"):
                        outcome_entry["results"].append({
                            "pageNumber": page["pageNumber"],
                            "excerpt": parsed.get("excerpt", ""),
                            "answer": parsed.get("answer", ""),
                            "statement": statement
                        })
                        break
                except Exception as e:
                    print(f"Failed on statement: {statement}\nResponse: {resp}\nError: {e}")
                    continue

        outcome_list.append(outcome_entry)

# Write outcome.json
with open("outcome.json", "w") as f:
    json.dump({"results": outcome_list}, f, indent=2)

print("Generated outcome.json using LLaMA 3.2 and fitz without embeddings.")
