import json
import fitz
import re
from collections import Counter
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain.vectorstores import Chroma

# Load JSON files
with open("pscrf.json") as f:
    pscrf_data = json.load(f)

with open("statements.json") as f:
    statements_data = json.load(f)

with open("references.json") as f:
    references_data = json.load(f)

# Map questions by questionRefId for quick lookup
statements_lookup = {q["questionRefId"]: q for q in statements_data["questions"]}

# LLM & Embeddings setup
llm = Ollama(model="llama3")
embedding_model = OllamaEmbeddings(model="llama3")

match_prompt = ChatPromptTemplate.from_messages([
    ("system", "You're an AI auditor. Determine if the statement is supported by the document page chunks."),
    ("human", """
Statement:
{statement}

Chunk:
{text}

Chunk metadata:
{metadata}

Instructions:
- Identify if any chunk clearly supports or contradicts the statement.
- Respond in JSON: {{"match": true/false, "answer": "Yes"/"No", "supportingSentence": "...", "pageNumber": number}}
""")
])

# Load and chunk PDF pages
def get_pdf_chunks(pdf_path):
    doc = fitz.open(pdf_path)
    pages = []
    for i in range(len(doc)):
        text = doc.load_page(i).get_text()
        pages.append(Document(page_content=text, metadata={"page": i+1}))
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=80)
    chunks = text_splitter.split_documents(pages)
    return chunks

# Deduplicate statements helper
def deduplicate_statements(stmts):
    seen = set()
    return [s for s in stmts if not (s in seen or seen.add(s))]

# Find reference object by key in references.json
def get_reference_by_key(key):
    for ref in references_data["references"]:
        if ref["key"] == key:
            return ref
    return None

# Main processing function
def process(pscrf_data, statements_lookup, references_data, pdf_path):
    chunks = get_pdf_chunks(pdf_path)
    # Build vector store over all chunks
    store = Chroma.from_documents(chunks, embedding_model)

    outcome = []

    for scenario in pscrf_data["scenarios"]:
        for q in scenario["questions"]:
            qref = q["questionRefId"]
            qmeta = statements_lookup.get(qref, {})
            qdesc = qmeta.get("questionDesc", "")
            references = qmeta.get("references", [])

            entry = {
                "pscrfId": pscrf_data["pscrfId"],
                "scenarioId": scenario["scenarioId"],
                "questionId": q["questionId"],
                "questionRefId": qref,
                "questionDesc": qdesc,
                "pdfFileName": pdf_path,
                "results": []
            }

            # CASE 1: references empty - use statements as queries, chunks from PDF
            if not references:
                stmts = deduplicate_statements(qmeta.get("statements", []))
                for stmt in stmts:
                    top_chunks = store.similarity_search(stmt, k=5)
                    best_score = -1
                    best_result = None

                    for chunk in top_chunks:
                        prompt = match_prompt.format_messages(
                            statement=stmt,
                            text=chunk.page_content,
                            metadata=json.dumps(chunk.metadata)
                        )
                        try:
                            res = llm.invoke(prompt)
                            parsed = json.loads(res.strip())
                            if parsed.get("match") and len(parsed.get("supportingSentence", "").split()) >= 5:
                                overlap = len(set(re.findall(r'\w+', stmt.lower())) & set(re.findall(r'\w+', parsed["supportingSentence"].lower())))
                                if overlap > best_score:
                                    best_score = overlap
                                    best_result = {
                                        "pageNumber": parsed.get("pageNumber", chunk.metadata.get("page", 0)),
                                        "excerpt": parsed["supportingSentence"],
                                        "answer": parsed.get("answer", "No"),
                                        "statement": stmt
                                    }
                        except Exception as e:
                            print("LLM error:", e)

                    if best_result:
                        entry["results"].append(best_result)

            # CASE 2: references populated - for each reference key, find related values in references.json and match with PDF sections
            else:
                for ref_key in references:
                    reference = get_reference_by_key(ref_key)
                    if not reference:
                        continue

                    # Use reference key as the statement/query to find relevant PDF chunk (page section)
                    # We'll find pages containing ref_key (or similar) for statement context
                    # For simplicity, use vector search with ref_key first to find statement context chunks
                    statement_chunks = store.similarity_search(ref_key, k=3)
                    statement_text = " ".join(c.page_content for c in statement_chunks)

                    # For each source in reference, treat each 'values' entry as a chunk to check for support
                    for source in reference.get("source", []):
                        for val in source.get("values", []):
                            # For each value, find top chunks in vector store to score against
                            top_chunks = store.similarity_search(val, k=3)

                            best_score = -1
                            best_result = None

                            for chunk in top_chunks:
                                prompt = match_prompt.format_messages(
                                    statement=statement_text,
                                    text=chunk.page_content,
                                    metadata=json.dumps(chunk.metadata)
                                )
                                try:
                                    res = llm.invoke(prompt)
                                    parsed = json.loads(res.strip())
                                    if parsed.get("match") and len(parsed.get("supportingSentence", "").split()) >= 5:
                                        overlap = len(set(re.findall(r'\w+', statement_text.lower())) & set(re.findall(r'\w+', parsed["supportingSentence"].lower())))
                                        if overlap > best_score:
                                            best_score = overlap
                                            best_result = {
                                                "pageNumber": parsed.get("pageNumber", chunk.metadata.get("page", 0)),
                                                "excerpt": parsed["supportingSentence"],
                                                "answer": parsed.get("answer", "No"),
                                                "statement": val
                                            }
                                except Exception as e:
                                    print("LLM error:", e)

                            if best_result:
                                entry["results"].append(best_result)

            # Aggregate answers and set accuracy level
            answers = [r["answer"] for r in entry["results"]]
            count = Counter(answers)
            agg = count.most_common(1)[0][0] if count else "No"
            entry["aggregateAnswer"] = agg
            entry["accuracyLevel"] = (
                "High" if count[agg] == len(answers) else
                "Medium" if count[agg] > 1 else "Low"
            )

            outcome.append(entry)

    return outcome


if __name__ == "__main__":
    pdf_path = "document.pdf"
    results = process(pscrf_data, statements_lookup, references_data, pdf_path)

    with open("outcome.json", "w") as f:
        json.dump({"results": results}, f, indent=2)

    print(json.dumps({"results": results}, indent=2))
