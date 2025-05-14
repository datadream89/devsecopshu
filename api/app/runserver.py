import json
import fitz
import re
from collections import Counter
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate

# Load files
pdf_path = "document.pdf"
with open("pscrf.json") as f:
    pscrf_data = json.load(f)
with open("sentence.json") as f:
    sentence_data = json.load(f)

sentence_lookup = {q["questionRefId"]: q for q in sentence_data["questions"]}

# Deduplicate statements
def deduplicate_statements(statements):
    return list(dict.fromkeys(statements))

# LLM setup
llm = Ollama(model="llama3")

# Prompts
match_prompt = ChatPromptTemplate.from_messages([
    ("system", "You're an AI auditor. Determine if the statement is supported by the page."),
    ("human", """
Statement:
{statement}

Page Sentences:
{sentences}

Instructions:
- Identify the most relevant supporting or contradicting sentence.
- Respond in JSON: {{"match": true/false, "answer": "Yes"/"No", "supportingSentence": "..."}}
""")
])

# Load PDF and extract text per page
def get_pdf_pages(path):
    doc = fitz.open(path)
    return [{"pageNumber": i + 1, "text": doc.load_page(i).get_text()} for i in range(len(doc))]

def extract_sentences(text):
    return re.split(r'(?<=[.!?])\s+', text.strip())

# Smarter ranking using frequency + term weighting
def rank_pages_by_overlap(statement, pages, top_n=5):
    statement_words = set(re.findall(r'\w+', statement.lower()))
    scores = []
    for page in pages:
        page_words = re.findall(r'\w+', page["text"].lower())
        match_count = sum(1 for word in page_words if word in statement_words)
        density = match_count / (len(page_words) + 1)
        scores.append((page["pageNumber"], density))
    ranked = sorted(scores, key=lambda x: x[1], reverse=True)
    return [p for p, _ in ranked[:top_n]]

# Main pipeline
pages = get_pdf_pages(pdf_path)
outcome = []

for scenario in pscrf_data["scenarios"]:
    for q in scenario["questions"]:
        qref = q["questionRefId"]
        question_meta = sentence_lookup.get(qref, {})
        qdesc = question_meta.get("questionDesc", "")
        statements = deduplicate_statements(question_meta.get("statements", []))

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
            top_pages = [p for p in pages if p["pageNumber"] in rank_pages_by_overlap(stmt, pages, top_n=4)]

            best_result = None
            for page in top_pages:
                context = "\n".join(extract_sentences(page["text"]))
                prompt = match_prompt.format_messages(statement=stmt, sentences=context)
                try:
                    response = llm.invoke(prompt)
                    parsed = json.loads(response.strip())
                    sent = parsed.get("supportingSentence", "")
                    if parsed.get("match") and len(sent.split()) >= 5:
                        best_result = {
                            "pageNumber": page["pageNumber"],
                            "excerpt": sent,
                            "answer": parsed.get("answer", "No"),
                            "statement": stmt
                        }
                        break  # take best early match
                except Exception as e:
                    print("LLM error:", e)

            if best_result:
                entry["results"].append(best_result)

        answers = [r["answer"] for r in entry["results"]]
        count = Counter(answers)
        agg = count.most_common(1)[0][0] if count else "No"
        entry["aggregateAnswer"] = agg
        entry["accuracyLevel"] = (
            "High" if count[agg] == len(answers) else
            "Medium" if count[agg] > 1 else "Low"
        )

        outcome.append(entry)

with open("outcome.json", "w") as f:
    json.dump({"results": outcome}, f, indent=2)

print(json.dumps({"results": outcome}, indent=2))
