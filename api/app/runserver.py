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
    seen = set()
    deduped = []
    for s in statements:
        if s not in seen:
            seen.add(s)
            deduped.append(s)
    return deduped

# LLM setup
llm = Ollama(model="llama3")

# Prompts
match_prompt = ChatPromptTemplate.from_messages([
    ("system", "You're an AI auditor. Identify if the statement is supported by the page."),
    ("human", """
Statement:
{statement}

Page Sentences:
{sentences}

Instructions:
- Find the most related sentence.
- State if it supports or contradicts the statement.
- Respond in JSON with fields: match (bool), answer (Yes/No), supportingSentence (str)
""")
])

# Load PDF pages
def get_pdf_pages(path):
    doc = fitz.open(path)
    return [{"pageNumber": i + 1, "text": doc.load_page(i).get_text()} for i in range(len(doc))]

# Extract sentences
def extract_sentences(text):
    return re.split(r'(?<=[.!?])\s+', text.strip())

# Heuristic ranking: keyword overlap
def keyword_overlap_rank(statement, pages, top_n=5):
    keywords = set(re.findall(r'\w+', statement.lower()))
    page_scores = []

    for page in pages:
        page_words = set(re.findall(r'\w+', page["text"].lower()))
        score = len(keywords & page_words)
        page_scores.append((page["pageNumber"], score))

    ranked = sorted(page_scores, key=lambda x: x[1], reverse=True)
    return [page_num for page_num, _ in ranked[:top_n]]

# Main pipeline
pages = get_pdf_pages(pdf_path)
outcome = []

for scenario in pscrf_data["scenarios"]:
    for q in scenario["questions"]:
        qref = q["questionRefId"]
        qdesc = sentence_lookup[qref]["questionDesc"]
        statements = deduplicate_statements(sentence_lookup[qref]["statements"])

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
            top_page_nums = keyword_overlap_rank(stmt, pages, top_n=5)
            relevant_pages = [p for p in pages if p["pageNumber"] in top_page_nums]

            for page in relevant_pages:
                sentences = extract_sentences(page["text"])
                context = "\n".join(sentences[:15])
                prompt = match_prompt.format_messages(statement=stmt, sentences=context)
                try:
                    response = llm.invoke(prompt)
                    parsed = json.loads(response.strip())
                    if parsed.get("match"):
                        entry["results"].append({
                            "pageNumber": page["pageNumber"],
                            "excerpt": parsed.get("supportingSentence", ""),
                            "answer": parsed.get("answer", "No"),
                            "statement": stmt
                        })
                except Exception as e:
                    print("LLM match error:", e)

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

print("✅ outcome.json generated.")
