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

# Load files
pdf_path = "document.pdf"
with open("pscrf.json") as f:
    pscrf_data = json.load(f)
with open("statements.json") as f:
    statement_data = json.load(f)
with open("references.json") as f:
    reference_data = json.load(f)

statement_lookup = {q["questionRefId"]: q for q in statement_data["questions"]}
ref_lookup = {ref["key"]: ref for ref in reference_data["references"]}

# LLM setup
llm = Ollama(model="llama3")
embedding_model = OllamaEmbeddings(model="llama3")

match_prompt = ChatPromptTemplate.from_messages([
    ("system", "You're an AI auditor. Determine if the statement is supported by the document page chunks."),
    ("human", """
Statement:
{statement}

Chunks:
{text}

Instructions:
- Identify if any chunk clearly supports or contradicts the statement.
- Respond in JSON: {\"match\": true/false, \"answer\": \"Yes\"/\"No\", \"supportingSentence\": \"...\", \"pageNumber\": number, \"section\": \"...\"}
""")
])

# Load and chunk PDF
def get_pdf_chunks(path):
    doc = fitz.open(path)
    pages = []
    for i in range(len(doc)):
        text = doc.load_page(i).get_text()
        pages.append(Document(page_content=text, metadata={"page": i+1}))
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=80)
    return text_splitter.split_documents(pages), doc

chunks, pdf_doc = get_pdf_chunks(pdf_path)
store = Chroma.from_documents(chunks, embedding_model)

outcome = []

for scenario in pscrf_data["scenarios"]:
    for q in scenario["questions"]:
        qref = q["questionRefId"]
        qmeta = statement_lookup.get(qref, {})
        qdesc = qmeta.get("questionDesc", "")
        refs = qmeta.get("references", [])
        answer_type = qmeta.get("answerDataType", "YN")

        entry = {
            "pscrfId": pscrf_data["pscrfId"],
            "scenarioId": scenario["scenarioId"],
            "questionId": q["questionId"],
            "questionRefId": qref,
            "questionDesc": qdesc,
            "pdfFileName": pdf_path,
            "answerDataType": answer_type,
            "results": []
        }

        # Case 1: use regular statements
        if not refs:
            statements = qmeta.get("statements", [])
            for stmt in statements:
                top_chunks = store.similarity_search(stmt, k=5)
                best_score = -1
                best_result = None

                for chunk in top_chunks:
                    prompt = match_prompt.format_messages(statement=stmt, text=chunk.page_content)
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
                                    "statement": stmt,
                                    "section": parsed.get("section", "")
                                }
                    except Exception as e:
                        print("LLM error:", e)

                if best_result:
                    entry["results"].append(best_result)

        # Case 2: use references
        else:
            for ref_key in refs:
                ref_entry = ref_lookup.get(ref_key, {})
                best_match_section = ""
                best_score = 0
                for page_num in range(len(pdf_doc)):
                    page_text = pdf_doc[page_num].get_text()
                    score = len(set(ref_key.lower().split()) & set(page_text.lower().split()))
                    if score > best_score:
                        best_score = score
                        best_match_section = page_text
                section_text = best_match_section if best_match_section else ref_key

                for src in ref_entry.get("source", []):
                    for val in src.get("values", []):
                        prompt = match_prompt.format_messages(statement=section_text, text=val)
                        try:
                            res = llm.invoke(prompt)
                            parsed = json.loads(res.strip())
                            if parsed.get("match") and len(parsed.get("supportingSentence", "").split()) >= 5:
                                entry["results"].append({
                                    "pageNumber": parsed.get("pageNumber", 0),
                                    "excerpt": parsed["supportingSentence"],
                                    "answer": parsed.get("answer", "No"),
                                    "statement": section_text,
                                    "referenceKey": ref_key,
                                    "sourceKey": src["key"],
                                    "section": parsed.get("section", "")
                                })
                        except Exception as e:
                            print("LLM error:", e)

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
