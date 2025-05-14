import json
import fitz
import re
from collections import Counter
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# Load input files
with open("pscrf.json") as f:
    pscrf_data = json.load(f)

with open("sentence.json") as f:
    sentence_data = json.load(f)

pdf_path = "document.pdf"
llm = Ollama(model="llama3")

# LLM prompt to detect relevance and contradiction
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

{{
  "match": true or false,
  "answer": "Yes" or "No" or "Uncertain",
  "supportingSentence": "..."
}}
""")
])

def get_pdf_pages(path):
    doc = fitz.open(path)
    return [{"pageNumber": i + 1, "text": doc.load_page(i).get_text()} for i in range(len(doc))]

def extract_sentences(text):
    return re.split(r'(?<=[.!?])\s+', text.strip())

def score_page(statement, text):
    words = re.findall(r'\w+', statement.lower())
    text = text.lower()
    return sum(1 for w in words if w in text)

def deduplicate_statements(statements):
    """ Removes duplicate statements tied to the same questionRefId """
    seen = set()
    return [stmt for stmt in statements if stmt not in seen and not seen.add(stmt)]

def tfidf_page_filter(statement, pages):
    """ Filters top pages based on TF-IDF score against a given statement """
    vectorizer = TfidfVectorizer()
    doc_texts = [p["text"] for p in pages]
    statement_vector = vectorizer.fit_transform([statement] + doc_texts)
    
    # Calculate cosine similarity between the statement and each page's text
    cosine_similarities = np.array(statement_vector[0].dot(statement_vector[1:].T).todense()).flatten()
    scored_pages = sorted(zip(cosine_similarities, pages), key=lambda x: x[0], reverse=True)
    
    return scored_pages[:3]  # Return top 3 pages based on TF-IDF

pages = get_pdf_pages(pdf_path)
sentence_lookup = {q["questionRefId"]: q for q in sentence_data["questions"]}
outcome = []

# Main loop
for scenario in pscrf_data["scenarios"]:
    for q in scenario["questions"]:
        qref = q["questionRefId"]
        qdesc = sentence_lookup[qref]["questionDesc"]
        statements = sentence_lookup[qref]["statements"]

        # Remove duplicate statements for the same questionRefId
        statements = deduplicate_statements(statements)

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
            # Step 1: Filter pages based on TF-IDF similarity
            scored_pages = tfidf_page_filter(stmt, pages)

            # Step 2: Extract sentences from top pages
            for _, page in scored_pages:
                sentences = extract_sentences(page["text"])[:5]
                snippet = "\n".join(f"- {s}" for s in sentences if s.strip())

                # Step 3: Use LLM to detect support or contradiction
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
                            "excerpt": parsed.get("supportingSentence", ""),
                            "answer": parsed.get("answer", "Uncertain"),
                            "statement": stmt
                        })
                        break
                except Exception as e:
                    print(f"Error: {e}")
                    continue

        # Step 4: Aggregate majority answer (Yes/No/Uncertain)
        answers = [r["answer"] for r in entry["results"]]
        count = Counter(answers)
        if count:
            aggregate_answer = count.most_common(1)[0][0]
        else:
            aggregate_answer = "Uncertain"

        # Step 5: Calculate accuracy level
        if aggregate_answer == "Uncertain":
            accuracy = "Low"
        elif count[aggregate_answer] == len(answers):
            accuracy = "High"
        else:
            accuracy = "Medium"

        entry["aggregateAnswer"] = aggregate_answer
        entry["accuracyLevel"] = accuracy
        outcome.append(entry)

# Save output
with open("outcome_optimized.json", "w") as f:
    json.dump({"results": outcome}, f, indent=2)

print("✅ outcome_optimized.json created with aggregateAnswer and accuracyLevel.")
