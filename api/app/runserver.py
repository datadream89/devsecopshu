# webapp/app.py
import streamlit as st
import json
import os
from pathlib import Path
from pdf_viewer import show_pdf

st.set_page_config(layout="wide")

# Load outputs
OUTPUT_DIR = "outputs"
REFERENCE_FILES = [f for f in os.listdir(OUTPUT_DIR) if f.endswith("_outcome.json")]

if not REFERENCE_FILES:
    st.warning("No output files found in 'outputs/' directory.")
    st.stop()

pscrf_ids = [f.replace("_outcome.json", "") for f in REFERENCE_FILES]
selected_id = st.selectbox("Select PSCRF ID", pscrf_ids)

with open(f"outputs/{selected_id}_outcome.json") as f:
    data = json.load(f)

# Pagination
index = st.session_state.get("question_index", 0)

if index >= len(data):
    st.success("End of questions.")
    index = 0

current = data[index]

st.subheader(f"Q{index + 1}. {current['question']}")
st.markdown(f"**Answer**: {current['answer']}")
st.markdown(f"**Page**: {current['pageNumber']}")
st.markdown(f"**Valid**: {current['isValid']}  ")
st.markdown(f"**Snippet**: _{current['snippet']}_")

pdf_path = f"pdfs/{current['fileName']}"
if Path(pdf_path).exists():
    show_pdf(pdf_path, page=current['pageNumber'])
else:
    st.error(f"PDF {current['fileName']} not found.")

if st.button("Next"):
    st.session_state["question_index"] = index + 1
    st.experimental_rerun()
