# ai_logic/ai_backend.py

import re
import random
from collections import Counter
import tempfile
import fitz  # PyMuPDF
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import Ollama
from langchain.chains import RetrievalQA


def load_and_split_pdf(pdf_path):
    raw_docs = PyMuPDFLoader(str(pdf_path)).load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    all_chunks = []
    for doc in raw_docs:
        page = doc.metadata["page"]
        stamped = f"[Page {page}] {doc.page_content}"
        chunks = splitter.create_documents([stamped])
        all_chunks.extend(chunks)
    return all_chunks


def run_majority_voting_qa(all_chunks, questions_with_ids):
    results = []
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    for meta_id, question in questions_with_ids.items():
        page_votes = []
        sentence_votes = []

        max_attempts = 5
        attempts = 0
        found_valid = False

        while attempts < max_attempts and not found_valid:
            attempts += 1

            shuffled_chunks = random.sample(all_chunks, len(all_chunks))
            vectorstore = Chroma.from_documents(shuffled_chunks, embedding=embeddings)
            retriever = vectorstore.as_retriever()
            qa_chain = RetrievalQA.from_chain_type(llm=Ollama(model="mistral"), retriever=retriever)

            answer = qa_chain.run(question).strip()

            if answer.lower() in ["yes", "no"]:
                found_valid = True
                results.append({
                    "meta_id": meta_id,
                    "question": question,
                    "answer": answer.capitalize(),
                    "page": None,
                    "sentence": None
                })
                break

            match = re.search(r"\[Page (\d+)\](.*)", answer)
            if match:
                page_num = int(match.group(1))
                sentence = match.group(2).strip().split(".")[0]

                match_found = any(sentence in doc.page_content for doc in all_chunks)

                if match_found:
                    page_votes.append(page_num)
                    sentence_votes.append(sentence)
                    found_valid = True
                    results.append({
                        "meta_id": meta_id,
                        "question": question,
                        "answer": f"[Page {page_num}] {sentence}",
                        "page": page_num,
                        "sentence": sentence
                    })

        if not found_valid:
            results.append({
                "meta_id": meta_id,
                "question": question,
                "answer": "Answer not found with reliable confidence.",
                "page": None,
                "sentence": None
            })

    return results


def highlight_pdf_sentence(pdf_path, sentence, page_number):
    doc = fitz.open(pdf_path)
    page = doc[page_number - 1]
    areas = page.search_for(sentence, quads=True)
    for area in areas:
        page.add_highlight_annot(area.rects)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc.save(temp_file.name)
    doc.close()
    return temp_file.name
