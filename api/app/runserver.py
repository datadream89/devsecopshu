import json
import fitz
import re
from collections import Counter
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
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

# Initialize Sentence-BERT model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_pdf_pages(path):
    doc = fitz.open(path)
    return [{"pageNumber": i + 1, "text": doc.load_page(i).get_text()} for i in range(len(doc))]

def extract_sentences(text):
    return re.split(r'(?<=[.!?])\s+', text.strip())

def sentence_embeddings(texts):
    """ Get embeddings of sentences using Sentence-BERT """
    return model.encode(texts, show_progress_bar=False)

def deduplicate_statements(statements):
    """ Removes duplicate statements tied to the same questionRefId """
    seen = set()
    return [stmt for stmt in statements if stmt not in seen and not seen.add(stmt)]

def match_statements_with_pdf(statements, pages):
    """ Finds top matching sentences from the PDF using Sentence-BERT embeddings """
    all_sentences = []
    for page in pages:
        sentences = extract_sentences(page["text"])
        all_sentences.extend([(page["pageNumber"], s) for s in sentences])

    # Get embeddings of all the PDF sentences
    pdf_sentences = [s[1] for s in all_sentences]
    pdf_embeddings = sentence_embeddings(pdf_sentences)

    matched_results = []
    
    # For each statement, compare it to all PDF sentences
    for stmt in statements:
        stmt_embedding = sentence_embeddings([stmt])[0]  # Get embedding for the target statement
        similarities = cosine_similarity([stmt_embedding], pdf_embeddings).flatten()
        
        # Select the top 3 most similar sentences
        top_sentences_idx = similarities.argsort()[-3:][::-1]
        
        for idx in top_sentences_idx:
            page_num, sentence = all_sentences[idx]
            matched_results.append({
                "pageNumber": page_num,
                "excerpt": sentence,
                "statement": stmt
            })
    
    return matched_results

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

        # Step 1: Find matching sentences from PDF based on semantic similarity
        matched_results = match_statements_with_pdf(statements, pages)

        # Step 2: Use LLM to check if the sentences support or contradict the statement
        for result in matched_results:
            stmt = result["statement"]
            snippet = result["excerpt"]

            prompt = match_prompt.format_messages(
                statement=stmt,
                sentences=snippet
            )

            try:
                response = llm.invoke(prompt)
                parsed = json.loads(response.strip())

                if parsed.get("match"):
                    entry["results"].append({
                        "pageNumber": result["pageNumber"],
                        "excerpt": parsed.get("supportingSentence", ""),
                        "answer": parsed.get("answer", "Uncertain"),
                        "statement": stmt
                    })
                    break
            except Exception as e:
                print(f"Error: {e}")
                continue

        # Step 3: Aggregate majority answer (Yes/No/Uncertain)
        answers = [r["answer"] for r in entry["results"]]
        count = Counter(answers)
        if count:
            aggregate_answer = count.most_common(1)[0][0]
        else:
            aggregate_answer = "Uncertain"

        # Step 4: Calculate accuracy level
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
with open("outcome_with_sbert.json", "w") as f:
    json.dump({"results": outcome}, f, indent=2)

print("✅ outcome_with_sbert.json created with aggregateAnswer and accuracyLevel.")
