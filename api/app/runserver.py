# ai_logic/ai_backend.py
import os
import json
import fitz  # PyMuPDF
from typing import List, Dict
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama


def extract_text_by_page(file_path: str) -> Dict[int, str]:
    doc = fitz.open(file_path)
    return {i + 1: page.get_text() for i, page in enumerate(doc)}


def create_vector_store(file_path: str):
    loader = PyMuPDFLoader(file_path)
    pages = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(pages)

    vector_store = Chroma.from_documents(
        docs, embedding=OllamaEmbeddings(model="nomic-embed-text"), persist_directory=".chroma-store"
    )
    return vector_store


def get_answer(llm, retriever, question: str) -> dict:
    prompt = (
        f"Answer the following question based on the document.
        Include only 'Yes' or 'No' as answer.
"
        f"Also provide the page number and the sentence or snippet supporting it.
"
        f"Question: {question}"
    )
    result = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    ).run(prompt)

    return result  # Post-processed in below step


def generate_output(pdf_path: str, prompt_dict_path: str, input_json_path: str, output_json_path: str):
    pscrf_id = os.path.basename(pdf_path).split(".")[0].split("_")[-1]
    text_by_page = extract_text_by_page(pdf_path)
    vector_store = create_vector_store(pdf_path)
    retriever = vector_store.as_retriever()
    llm = Ollama(model="llama3")

    with open(prompt_dict_path) as f:
        prompt_dict = json.load(f)

    with open(input_json_path) as f:
        input_json = json.load(f)

    question_map = {}
    for scenario in prompt_dict["scenarios"]:
        for q in scenario["questions"]:
            question_map[q["questionRefId"]] = {
                "questionText": q["answerText"],
                "questionId": q["questionId"],
                "scenarioId": scenario["scenarioId"],
                "pscrfId": prompt_dict["pscrfId"]
            }

    output = []
    for item in input_json["prompts"]:
        question_ref_id = item["questionRefId"]
        prompt = item["prompt"]
        qa_result = get_answer(llm, retriever, prompt)

        # Heuristic parsing (for demo purpose)
        answer = "Yes" if "yes" in qa_result.lower() else "No"
        page_number = next((p for p, text in text_by_page.items() if answer.lower() in text.lower()), -1)
        snippet = qa_result.split("Answer:")[-1].strip()[:300]

        is_valid = "Yes" if page_number != -1 else "No"

        result = {
            "pscrfId": question_map[question_ref_id]["pscrfId"],
            "scenarioId": question_map[question_ref_id]["scenarioId"],
            "questionId": question_map[question_ref_id]["questionId"],
            "questionRefId": question_ref_id,
            "fileName": os.path.basename(pdf_path),
            "pageNumber": page_number,
            "snippet": snippet,
            "accuracy": "High" if is_valid == "Yes" else "Low",
            "isValid": is_valid,
            "question": prompt.split("?")[0] + "?",
            "answer": answer
        }
        output.append(result)

    with open(output_json_path, "w") as f:
        json.dump(output, f, indent=2)

    return output
