import json
from PyPDF2 import PdfReader
from langchain_core.messages import HumanMessage
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate

# Load JSON data
with open("sentence.json") as f:
    sentence_data = json.load(f)

with open("pscrf.json") as f:
    pscrf_data = json.load(f)

pdf_path = "document.pdf"
reader = PdfReader(pdf_path)

# Extract all PDF pages
pages = [{"pageNumber": i + 1, "text": page.extract_text()} for i, page in enumerate(reader.pages)]

# LangChain LLaMA LLM
llm = Ollama(model="llama3")

# LangChain prompt template
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a compliance analyst evaluating whether a statement is supported by a PDF page."),
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
  "excerpt": "A relevant excerpt if match is true, otherwise empty"
}}
""")
])

outcome_list = []

# Process each question
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
            for page in pages:
                message = prompt_template.format_messages(
                    statement=statement,
                    pageNumber=page["pageNumber"],
                    pageContent=page["text"][:4000] if page["text"] else ""
                )
                response = llm.invoke(message)

                try:
                    parsed = json.loads(response.strip())
                    if parsed.get("match"):
                        outcome_entry["results"].append({
                            "pageNumber": page["pageNumber"],
                            "excerpt": parsed.get("excerpt", ""),
                            "answer": parsed.get("answer", ""),
                            "statement": statement
                        })
                        break  # Use first match
                except Exception as e:
                    print(f"Parse error: {e}\nResponse: {response}")

        outcome_list.append(outcome_entry)

# Write final outcome.json
with open("outcome.json", "w") as f:
    json.dump({"results": outcome_list}, f, indent=2)

print("outcome.json successfully created using LangChain + LLaMA 3.2.")
