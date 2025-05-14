import json
import fitz  # PyMuPDF
from langchain_core.messages import HumanMessage
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate

# Load JSON files
with open("sentence.json") as f:
    sentence_data = json.load(f)

with open("pscrf.json") as f:
    pscrf_data = json.load(f)

pdf_path = "document.pdf"

# Extract text from each page of the PDF using Fitz
def extract_pdf_text(pdf_path):
    doc = fitz.open(pdf_path)
    pages = [{"pageNumber": i + 1, "text": doc.load_page(i).get_text()} for i in range(doc.page_count)]
    return pages

# LangChain LLaMA LLM setup
llm = Ollama(model="llama3")

# LangChain prompt template
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a compliance analyst reviewing whether a statement is supported by content from a PDF page."),
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

# Process each question in pscrf.json
for scenario in pscrf_data["scenarios"]:
    for question in scenario["questions"]:
        qref = question["questionRefId"]

        # Match with sentence in sentence.json
        sentence_entry = next((q for q in sentence_data["questions"] if q["questionRefId"] == qref), None)
        if not sentence_entry:
            continue

        # Prepare outcome entry for this question
        outcome_entry = {
            "pscrfId": pscrf_data["pscrfId"],
            "scenarioId": scenario["scenarioId"],
            "questionId": question["questionId"],
            "questionRefId": qref,
            "questionDesc": sentence_entry["questionDesc"],
            "pdfFileName": pdf_path,
            "results": []
        }

        # Extract text from PDF pages
        pages = extract_pdf_text(pdf_path)

        # Evaluate each statement against each page
        for statement in sentence_entry["statements"]:
            for page in pages:
                # Prepare the prompt for LLaMA
                message = prompt_template.format_messages(
                    statement=statement,
                    pageNumber=page["pageNumber"],
                    pageContent=page["text"][:4000] if page["text"] else ""  # limit text size to prevent overflow
                )
                
                # Get response from LLaMA
                response = llm.invoke(message)

                try:
                    parsed = json.loads(response.strip())
                    if parsed.get("match"):
                        # Add the result if match is found
                        outcome_entry["results"].append({
                            "pageNumber": page["pageNumber"],
                            "excerpt": parsed.get("excerpt", ""),
                            "answer": parsed.get("answer", ""),
                            "statement": statement
                        })
                        break  # only keep the first matching page for this statement
                except Exception as e:
                    print(f"Parse error: {e}\nResponse: {response}")
                    continue

        outcome_list.append(outcome_entry)

# Write the final outcome.json file
with open("outcome.json", "w") as f:
    json.dump({"results": outcome_list}, f, indent=2)

print("outcome.json successfully created using LangChain + LLaMA 3.2 + Fitz.")
