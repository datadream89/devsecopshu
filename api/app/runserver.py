# Folder structure with file contents:

# project_root/ai_logic/ai_backend.py

import os
import json
import fitz  # PyMuPDF
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from collections import Counter

def extract_text_with_page_numbers(pdf_path):
    doc = fitz.open(pdf_path)
    pages = []
    for page_number in range(len(doc)):
        page = doc.load_page(page_number)
        text = page.get_text()
        pages.append({"page": page_number + 1, "text": text})
    return pages

def majority_vote(answers):
    return Counter(answers).most_common(1)[0][0]

def process_pdf_with_questions(pdf_path, prompt_json, reference_json, reference_name):
    pages = extract_text_with_page_numbers(pdf_path)
    all_text = "\n".join(p["text"] for p in pages)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = text_splitter.split_text(all_text)

    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vectordb = FAISS.from_texts(chunks, embedding=embeddings)

    llm = Ollama(model="llama3")
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
        Answer the question as accurately as possible based on the context.

        Context: {context}
        Question: {question}
        Answer with a clear Yes or No.
        """
    )
    chain = LLMChain(llm=llm, prompt=prompt)

    results = []
    pscrf_id = reference_json["pscrfId"]
    for scenario in reference_json["scenarios"]:
        scenario_id = scenario["scenarioId"]
        for q in scenario["questions"]:
            question_id = q["questionId"]
            question_ref_id = q["questionRefId"]

            prompt_text = next((p["promptText"] for p in prompt_json["prompts"] if p["questionRefId"] == question_ref_id), "")
            if not prompt_text:
                continue

            docs = vectordb.similarity_search(prompt_text, k=4)
            context = "\n".join([doc.page_content for doc in docs])

            answers = [chain.run(context=context, question=prompt_text).strip() for _ in range(3)]
            answer = majority_vote(answers)

            matched_snippet = next((doc.page_content for doc in docs if answer.lower() in doc.page_content.lower()), "")
            page_number = next((p["page"] for p in pages if matched_snippet and matched_snippet[:30] in p["text"]), -1)
            accuracy = round((answers.count(answer) / len(answers)) * 100)

            results.append({
                "pscrfId": pscrf_id,
                "scenarioId": scenario_id,
                "questionId": question_id,
                "questionRefId": question_ref_id,
                "filename": os.path.basename(pdf_path),
                "pageNumber": page_number,
                "matchedSnippet": matched_snippet,
                "answer": answer,
                "accuracyLevel": accuracy,
                "isValid": "Yes" if answer.lower() in matched_snippet.lower() else "No",
                "question": prompt_text.split("?")[0] + "?"
            })

    return results


# project_root/webapp/app.py

import streamlit as st
import json
import os
from ai_logic.ai_backend import process_pdf_with_questions

st.set_page_config(layout="wide")
st.title("PSCRF QA Explorer")

pdf_files = st.file_uploader("Upload PDF(s)", type="pdf", accept_multiple_files=True)
prompt_json = st.file_uploader("Upload Prompt JSON", type="json")
reference_files = st.file_uploader("Upload Reference JSON(s)", type="json", accept_multiple_files=True)

if pdf_files and prompt_json and reference_files:
    prompt_data = json.load(prompt_json)
    reference_data = {f.name: json.load(f) for f in reference_files}

    pscrf_options = list(reference_data.keys())
    selected_ref_file = st.selectbox("Select PSCRF ID (File)", pscrf_options)

    reference = reference_data[selected_ref_file]
    pdf_file = next((f for f in pdf_files if selected_ref_file.startswith(os.path.splitext(f.name)[0])), None)

    if pdf_file:
        pdf_path = os.path.join("/mnt", "wsl", "pdfs", pdf_file.name)
        with open(pdf_path, "wb") as f:
            f.write(pdf_file.read())

        output = process_pdf_with_questions(pdf_path, prompt_data, reference, selected_ref_file)

        idx = st.session_state.get("idx", 0)
        if idx >= len(output):
            idx = 0

        st.session_state["idx"] = idx

        if output:
            q = output[idx]
            st.write(f"**Question:** {q['question']}")
            st.write(f"**Answer:** {q['answer']}")
            st.write(f"**Page Number:** {q['pageNumber']}")
            st.write(f"**Accuracy:** {q['accuracyLevel']}%")
            st.write(f"**Valid:** {q['isValid']}")
            st.text_area("Snippet:", q['matchedSnippet'], height=200)

            if st.button("Next"):
                st.session_state["idx"] += 1
                st.experimental_rerun()


# project_root/webapp/pdf_viewer/__init__.py

# Empty file for module initialization


# project_root/webapp/pdf_viewer/pdf_component.html

<!-- Example component placeholder -->
<div id="pdf-container">
  <embed src="{{ pdf_url }}" width="100%" height="800px" type="application/pdf">
</div>


# project_root/pdfs/  # <- Place your PDFs here

# project_root/prompts/  # <- Place pscrf_101.json, etc.

# project_root/references/  # <- Place prompt_dict.json, etc.

# project_root/outputs/  # <- Outputs written by app
