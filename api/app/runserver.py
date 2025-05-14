import json
import fitz
import re
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate

# Load data
with open("sentence.json") as f:
    sentence_data = json.load(f)

with open("pscrf.json") as f:
    pscrf_data = json.load(f)

pdf_path = "document.pdf"
llm = Ollama(model="llama3")

# Step 1: Extract PDF pages
def get_pdf_pages(path):
    doc = fitz.open(path)
    return [{"pageNumber": i + 1, "text": doc.load_page(i).get_text()} for i in range(len(doc))]

# Step 2: Extract sentences from a block of text
def extract_sentences(text):
    text = re.sub(r"\s+", " ", text.strip())
    return re.split(r'(?<=[.!?]) +', text)

# Prompts
page_score_prompt = ChatPromptTemplate.from_messages([
    ("system", "Rate each page's relevance to the statement."),
    ("human", """
Statement: {statement}
Rate the relevance of this PDF page on a scale of 1 (irrelevant) to 5 (very relevant).

Page {pageNumber}:
{pageContent}

Respond as JSON:
{{ "pageNumber": {pageNumber}, "score": 1–5 }}
""")
])

sentence_match_prompt = ChatPromptTemplate.from_messages([
    ("system", "You identify if any sentence in a list supports the statement."),
    ("human", """
Statement:
{statement}

Sentences from Page {pageNumber}:
{sentences}

Does any sentence clearly support the statement? Respond as JSON:
{{
  "match": true or false,
  "answer": "Yes" or "No" or "Uncertain",
  "supportingSentence": "Best matching sentence or empty if none"
}}
""")
])

# Step 3: Hybrid Evaluation
pages = get_pdf_pages(pdf_path)
outcome_list = []

for scenario in pscrf_data["scenarios"]:
    for question in scenario["questions"]:
        qref = question["questionRefId"]
        qdesc = question["question"]
        sentence_entry = next((q for q in sentence_data["questions"] if q["questionRefId"] == qref), None)
        if not sentence_entry:
            continue

        outcome_entry = {
            "pscrfId": pscrf_data["pscrfId"],
            "scenarioId": scenario["scenarioId"],
            "questionId": question["questionId"],
            "questionRefId": qref,
            "questionDesc": qdesc,
            "pdfFileName": pdf_path,
            "results": []
        }

        for statement in sentence_entry["statements"]:
            scores = []
            for page in pages:
                score_prompt = page_score_prompt.format_messages(
                    statement=statement,
                    pageNumber=page["pageNumber"],
                    pageContent=page["text"][:1000]
                )
                try:
                    resp = llm.invoke(score_prompt)
                    score = json.loads(resp.strip()).get("score", 0)
                    scores.append((score, page))
                except:
                    continue

            # Top 3 pages
            top_pages = sorted(scores, key=lambda x: x[0], reverse=True)[:3]

            # Step 4: Sentence-level match in top pages
            for _, page in top_pages:
                sentences = extract_sentences(page["text"])
                if not sentences:
                    continue

                prompt = sentence_match_prompt.format_messages(
                    statement=statement,
                    pageNumber=page["pageNumber"],
                    sentences="\n".join(f"- {s}" for s in sentences[:10])  # limit to 10 for token control
                )
                try:
                    result = llm.invoke(prompt)
                    parsed = json.loads(result.strip())
                    if parsed.get("match"):
                        outcome_entry["results"].append({
                            "pageNumber": page["pageNumber"],
                            "excerpt": parsed.get("supportingSentence", ""),
                            "answer": parsed.get("answer", ""),
                            "statement": statement
                        })
                        break
                except Exception as e:
                    continue

        outcome_list.append(outcome_entry)

# Save final output
with open("outcome.json", "w") as f:
    json.dump({"results": outcome_list}, f, indent=2)

print("Hybrid outcome.json generated.")
