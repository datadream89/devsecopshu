import json
import fitz
import re
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate

# Load JSON files
with open("pscrf.json") as f:
    pscrf_data = json.load(f)

with open("sentence.json") as f:
    sentence_data = json.load(f)

pdf_path = "document.pdf"
llm = Ollama(model="llama3")

# Prompt: First find most related sentence, then judge support vs contradiction
match_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an auditor. Find the most relevant sentence from the page for the given statement. Then decide if it supports or contradicts the statement."),
    ("human", """
Target Statement:
{statement}

Page Sentences:
{sentences}

Steps:
1. Identify the sentence that most directly relates to the target statement.
2. Check whether it supports or contradicts the target statement.
3. Return:
- match: true or false (is a relevant sentence found?)
- answer: "Yes" (if it supports), "No" (if it contradicts), or "Uncertain"
- supportingSentence: the most related sentence

Respond in JSON:
{{
  "match": true or false,
  "answer": "Yes" or "No" or "Uncertain",
  "supportingSentence": "..."
}}
""")
])

# PDF tools
def get_pdf_pages(path):
    doc = fitz.open(path)
    return [{"pageNumber": i + 1, "text": doc.load_page(i).get_text()} for i in range(len(doc))]

def extract_sentences(text):
    return re.split(r'(?<=[.!?])\s+', text.strip())

def score_page(statement, text):
    words = re.findall(r'\w+', statement.lower())
    text = text.lower()
    return sum(1 for w in words if w in text)

# Load PDF
pages = get_pdf_pages(pdf_path)

# Sentence lookup by questionRefId
sentence_lookup = {q["questionRefId"]: q for q in sentence_data["questions"]}
outcome = []

# Process each question
for scenario in pscrf_data["scenarios"]:
    for q in scenario["questions"]:
        qref = q["questionRefId"]
        qdesc = sentence_lookup[qref]["questionDesc"]
        statements = sentence_lookup[qref]["statements"]

        entry = {
            "pscrfId": pscrf_data["pscrfId"],
            "scenarioId": scenario["scenarioId"],
            "questionId": q["questionId"],
            "questionRefId": qref,
            "questionDesc": qdesc,
            "pdfFileName": pdf_path,
            "results": []
        }

        for stmt in statements:
            # Get top 2 likely pages by word match
            scored_pages = sorted(
                [(score_page(stmt, p["text"]), p) for p in pages],
                key=lambda x: x[0],
                reverse=True
            )[:2]

            for _, page in scored_pages:
                sentences = extract_sentences(page["text"])[:10]
                snippet = "\n".join(f"- {s}" for s in sentences if s.strip())

                prompt = match_prompt.format_messages(
                    statement=stmt,
                    sentences=snippet
                )

                try:
                    response = llm.invoke(prompt)
                    parsed = json.loads(response.strip())

                    if parsed.get("match"):
                        entry["results"].append({
                            "pageNumber": page["pageNumber"],
                            "excerpt": parsed["supportingSentence"],
                            "answer": parsed["answer"],
                            "statement": stmt
                        })
                        break  # stop after first match
                except Exception as e:
                    print(f"Error parsing LLM response: {e}")
                    continue

        outcome.append(entry)

# Save output
with open("outcome.json", "w") as f:
    json.dump({"results": outcome}, f, indent=2)

print("✅ outcome.json created.")
