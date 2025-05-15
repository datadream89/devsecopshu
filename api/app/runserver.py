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

# Create lookup dictionaries
statement_lookup = {q["questionRefId"]: q for q in statement_data["questions"]}
ref_lookup = {ref["key"]: ref for ref in reference_data["references"]}

# LLM and embedding model setup
llm = Ollama(model="llama3")
embedding_model = OllamaEmbeddings(model="llama3")

# Prompt to check if chunk supports statement
match_prompt = ChatPromptTemplate.from_messages([
    ("system", "You're an AI auditor. Determine if the statement is supported by the document page chunks."),
    ("human", """
Statement:
{statement}

Chunks:
{text}

Instructions:
- Identify if any chunk clearly supports or contradicts the statement.
- Respond in JSON: {{"match": true/false, "answer": "Yes"/"No", "supportingSentence": "..."}}
""")
])

# Prompt to identify if paragraph defines a term
definition_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert assistant helping identify definitions in a document."),
    ("human", """
TERM: {term}

PARAGRAPH:
"{paragraph}"

INSTRUCTION:
If the paragraph defines or explains the term, respond in JSON as:
{{"match": true, "definition": "..."}}
Else respond: {{"match": false}}
""")
])

# Load and chunk PDF for vector search
def get_pdf_chunks(path):
    doc = fitz.open(path)
    pages = []
    for i in range(len(doc)):
        text = doc.load_page(i).get_text()
        pages.append(Document(page_content=text, metadata={"page": i + 1}))
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

        # Case 1: references empty → use normal statements with similarity search
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
                                    "pageNumber": chunk.metadata.get("page", 0),
                                    "excerpt": parsed["supportingSentence"],
                                    "answer": parsed.get("answer", "No"),
                                    "statement": stmt
                                }
                    except Exception as e:
                        print("LLM error:", e)

                if best_result:
                    entry["results"].append(best_result)

        # Case 2: references populated → find definition paragraph using LLM, then match each source value
        else:
            for ref_key in refs:
                ref_entry = ref_lookup.get(ref_key, {})

                # Collect all paragraphs with page info
                paragraphs = []
                for i in range(len(pdf_doc)):
                    text = pdf_doc[i].get_text()
                    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
                    for para in paras:
                        paragraphs.append({"text": para, "page": i + 1})

                best_definition = None
                best_page = None

                # Use LLM to find paragraph that defines ref_key term
                for para in paragraphs:
                    prompt = definition_prompt.format_messages(term=ref_key, paragraph=para["text"])
                    try:
                        res = llm.invoke(prompt)
                        parsed = json.loads(res.strip())
                        if parsed.get("match"):
                            best_definition = parsed["definition"]
                            best_page = para["page"]
                            break
                    except Exception as e:
                        print(f"LLM error finding definition for {ref_key}: {e}")

                # Fallback if no definition found
                section_text = best_definition if best_definition else ref_key

                # For each value under sources, match with statement (definition paragraph)
                for src in ref_entry.get("source", []):
                    for val in src.get("values", []):
                        prompt = match_prompt.format_messages(statement=section_text, text=val)
                        try:
                            res = llm.invoke(prompt)
                            parsed = json.loads(res.strip())
                            if parsed.get("match") and len(parsed.get("supportingSentence", "").split()) >= 5:
                                entry["results"].append({
                                    "pageNumber": best_page if best_page else 0,
                                    "excerpt": parsed["supportingSentence"],
                                    "answer": parsed.get("answer", "No"),
                                    "statement": section_text
                                })
                        except Exception as e:
                            print("LLM error:", e)

        # Aggregate answers for this question
        answers = [r["answer"] for r in entry["results"]]
        count = Counter(answers)
        agg = count.most_common(1)[0][0] if count else "No"
        entry["aggregateAnswer"] = agg
        entry["accuracyLevel"] = (
            "High" if count[agg] == len(answers) else
            "Medium" if count[agg] > 1 else "Low"
        )

        outcome.append(entry)

# Write outcome file and print
with open("outcome.json", "w") as f:
    json.dump({"results": outcome}, f, indent=2)

print(json.dumps({"results": outcome}, indent=2))
