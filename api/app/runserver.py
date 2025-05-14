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
rank_prompt = ChatPromptTemplate.from_messages([
    ("system", "You're a smart auditor. Given a statement and page snippets, rank pages most likely to contain the statement."),
    ("human", """
Statement:
{statement}

Page Snippets:
{pages}

Respond with JSON array of ranked page numbers in decreasing order of relevance.
Output:
[<int>, <int>, ...]
""")
])

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

# Rank top N pages with LLM
def rank_pages_with_llm(statement, pages, top_n=3):
    page_snippets = "\n\n".join([f"Page {p['pageNumber']}: {p['text'][:300].replace('\\n', ' ')}..." for p in pages])
    prompt = rank_prompt.format_messages(statement=statement, pages=page_snippets)
    try:
        response = llm.invoke(prompt)
        ranked = json.loads(response.strip())
        return ranked[:top_n] if isinstance(ranked, list) else []
    except Exception as e:
        print("Ranking LLM error:", e)
        return list(range(1, top_n + 1))

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
            top_page_nums = rank_pages_with_llm(stmt, pages)
            relevant_pages = [p for p in pages if p["pageNumber"] in top_page_nums]

            for page in relevant_pages:
                sentences = extract_sentences(page["text"])
                context = "\n".join(sentences[:15])
                prompt = match_prompt.format_messages(statement=stmt, sentences=context)
                try:
                    response = llm.invoke(prompt)
                    parsed = json.loads(response.strip())
                    if parsed.get("match"):
                        ans = parsed.get("answer", "No")
                        if ans not in ["Yes", "No"]:
                            ans = "No"
                        entry["results"].append({
                            "pageNumber": page["pageNumber"],
                            "excerpt": parsed.get("supportingSentence", ""),
                            "answer": ans,
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
