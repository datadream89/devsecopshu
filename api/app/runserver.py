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

# Extract all pages
def get_pdf_pages(path):
    doc = fitz.open(path)
    return [{"pageNumber": i + 1, "text": doc.load_page(i).get_text()} for i in range(len(doc))]

# Extract clean sentences
def extract_sentences(text):
    text = re.sub(r"\s+", " ", text.strip())
    return re.split(r'(?<=[.!?]) +', text)

# LLM prompts
page_score_prompt = ChatPromptTemplate.from_messages([
    ("system", "You rate how relevant a PDF page is to a statement."),
    ("human", """
Statement: {statement}

Rate the relevance of this PDF page on a scale of 1 (irrelevant) to 5 (very relevant).

Page {pageNumber}:
{pageContent}

Respond in JSON:
{{ "pageNumber": {pageNumber}, "score": 1–5 }}
""")
])

sentence_match_prompt = ChatPromptTemplate.from_messages([
    ("system", "You evaluate if any sentence supports the statement."),
    ("human", """
Statement:
{statement}

Sentences from Page {pageNumber}:
{sentences}

Respond in JSON:
{{
  "match": true or false,
  "answer": "Yes" or "No" or "Uncertain",
  "supportingSentence": "Matching sentence or empty if none"
}}
""")
])

# Build outcomes
pages = get_pdf_pages(pdf_path)
outcomes = []

# Build lookup from sentence.json
sentence_lookup = {q["questionRefId"]: q for q in sentence_data["questions"]}

for scenario in pscrf_data["scenarios"]:
    for question in scenario["questions"]:
        qref = question["questionRefId"]
        qdesc = sentence_lookup.get(qref, {}).get("questionDesc", "")
        statements = sentence_lookup.get(qref, {}).get("statements", [])
        answer_type = question.get("answerDataType", "")
        answer_text = question.get("answerText", "")

        entry = {
            "pscrfId": pscrf_data["pscrfId"],
            "scenarioId": scenario["scenarioId"],
            "questionId": question["questionId"],
            "questionRefId": qref,
            "questionDesc": qdesc,
            "pdfFileName": pdf_path,
            "results": []
        }

        for stmt in statements:
            scores = []
            for page in pages:
                prompt = page_score_prompt.format_messages(
                    statement=stmt,
                    pageNumber=page["pageNumber"],
                    pageContent=page["text"][:1000]
                )
                try:
                    resp = llm.invoke(prompt)
                    score = json.loads(resp.strip()).get("score", 0)
                    scores.append((score, page))
                except:
                    continue

            top_pages = sorted(scores, key=lambda x: x[0], reverse=True)[:3]

            for _, page in top_pages:
                sents = extract_sentences(page["text"])
                prompt = sentence_match_prompt.format_messages(
                    statement=stmt,
                    pageNumber=page["pageNumber"],
                    sentences="\n".join(f"- {s}" for s in sents[:10])  # first 10 sentences
                )
                try:
                    resp = llm.invoke(prompt)
                    parsed = json.loads(resp.strip())
                    if parsed.get("match"):
                        entry["results"].append({
                            "pageNumber": page["pageNumber"],
                            "excerpt": parsed.get("supportingSentence", ""),
                            "answer": parsed.get("answer", ""),
                            "statement": stmt
                        })
                        break
                except:
                    continue

        outcomes.append(entry)

# Write output
with open("outcome.json", "w") as f:
    json.dump({"results": outcomes}, f, indent=2)

print("outcome.json created.")
