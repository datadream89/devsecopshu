# webapp/app.py

import streamlit as st
import json
import base64
import tempfile
import os
import sys
from pathlib import Path

# Add ai_logic to sys.path
ai_logic_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ai_logic"))
sys.path.append(ai_logic_path)

from ai_backend import load_and_split_pdf, run_majority_voting_qa, highlight_pdf_sentence
from pdf_viewer import view_pdf


def show_pdf(file_path):
    view_pdf(file_path)


st.title("Document QA & Highlight Viewer")

pdf_file = st.file_uploader("Upload PDF file", type="pdf")
input_json = st.file_uploader("Upload Input JSON", type="json")
ref_json = st.file_uploader("Upload Reference JSON", type="json")

if pdf_file and input_json and ref_json:
    # Save PDF to temp file
    pdf_path = Path(tempfile.gettempdir()) / pdf_file.name
    with open(pdf_path, "wb") as f:
        f.write(pdf_file.read())

    input_entries = json.load(input_json)
    reference_entries = json.load(ref_json)

    questions_dict = {}
    meta_map = {}

    for entry in input_entries:
        cid = entry["client_id"]
        sid = entry["scenario_id"]
        qid = entry["question_id"]
        meta_id = f"{cid}_{sid}_{qid}"
        try:
            question_text = reference_entries[cid][sid][qid]["question"]
            questions_dict[meta_id] = question_text
            meta_map[meta_id] = {"client_id": cid, "scenario_id": sid, "question_id": qid}
        except KeyError:
            st.warning(f"Missing question for {cid} > {sid} > {qid}")

    if "qa_results" not in st.session_state:
        with st.spinner("Running QA..."):
            chunks = load_and_split_pdf(pdf_path)
            st.session_state.qa_results = run_majority_voting_qa(chunks, questions_dict)
            st.session_state.index = 0

    results = st.session_state.qa_results
    index = st.session_state.index
    item = results[index]

    meta = meta_map.get(item["meta_id"], {})
    st.subheader(f"Question {index + 1} of {len(results)}")
    st.markdown(f"**Client ID:** {meta.get('client_id')}")
    st.markdown(f"**Scenario ID:** {meta.get('scenario_id')}")
    st.markdown(f"**Question ID:** {meta.get('question_id')}")
    st.markdown(f"**Q:** {item['question']}")
    st.markdown(f"**A:** {item['answer']}")

    if item["page"] and item["sentence"]:
        highlighted_pdf = highlight_pdf_sentence(str(pdf_path), item["sentence"], item["page"])
        show_pdf(highlighted_pdf)
    elif item["answer"].lower() in ["yes", "no"]:
        st.info(f"Answer is a clear '{item['answer']}' response.")
    else:
        st.warning("Could not highlight answer in PDF.")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Previous", disabled=index == 0):
            st.session_state.index -= 1
    with col2:
        if st.button("Next", disabled=index == len(results) - 1):
            st.session_state.index += 1
