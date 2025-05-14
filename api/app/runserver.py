import json
import fitz
import re
from collections import Counter
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from rapidfuzz import fuzz

# Initialize PDF reader
pdf_path = "document.pdf"

# Load files
with open("pscrf.json") as f:
    pscrf_data = json.load(f)

with open("sentence.json") as f:
    sentence_data = json.load(f)

sentence_lookup = {q["questionRefId"]: q for q in sentence_data["questions"]}

# Deduplication
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

match_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an auditor. Identify if a statement is supported or contradicted by the page."),
    ("human", """
Target Statement:
{statement}

Page Sentences:
{sentences}

Instructions:
1. Pick the sentence that most directly relates to the target statement.
2. Decide if it supports or contradicts the target statement.
3. Respond as JSON:
{
  \"match\": true or false,
  \"answer\": \"Yes\" or \"No\" or \"Uncertain\",
  \"supportingSentence\": \"...\"
}
""")
])

# Load PDF
def get_pdf_pages(path):
    doc = fitz.open(path)
    return [{"pageNumber": i + 1, "text": doc.load_page(i).get_text()} for i in range(len(doc))]

# Extract sentences
def extract_sentences(text):
    return re.split(r'(?<=[.!?])\s+', text.strip())

# Match statements with PDF using fuzzy match
def match_statements_with_pdf(statements, pages):
    all_sentences = []
    for page in pages:
        sentences = extract_sentences(page["text"])
        for s in sentences:
            all_sentences.append({"pageNumber": page["pageNumber"], "sentence": s})

    matched_results = []
    for stmt in statements:
        ranked = sorted(all_sentences, key=lambda x: fuzz.token_set_ratio(x["sentence"], stmt), reverse=True)[:3]
        for match in ranked:
            matched_results.append({
                "pageNumber": match["pageNumber"],
                "excerpt": match["sentence"],
                "statement": stmt
            })
    return matched_results

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

        matched = match_statements_with_pdf(statements, pages)

        for result in matched:
            prompt = match_prompt.format_messages(
                statement=result["statement"],
                sentences=result["excerpt"]
            )
            try:
                response = llm.invoke(prompt)
                parsed = json.loads(response.strip())
                if parsed.get("match"):
                    entry["results"].append({
                        "pageNumber": result["pageNumber"],
                        "excerpt": parsed.get("supportingSentence", result["excerpt"]),
                        "answer": parsed.get("answer", "Uncertain"),
                        "statement": result["statement"]
                    })
            except Exception as e:
                print("LLM error:", e)
                continue

        answers = [r["answer"] for r in entry["results"]]
        count = Counter(answers)
        if count:
            agg = count.most_common(1)[0][0]
        else:
            agg = "Uncertain"

        entry["aggregateAnswer"] = agg
        entry["accuracyLevel"] = (
            "High" if count[agg] == len(answers) else
            "Medium" if count[agg] > 1 else "Low"
        )

        outcome.append(entry)

with open("outcome.json", "w") as f:
    json.dump({"results": outcome}, f, indent=2)

print("✅ outcome.json generated.")
