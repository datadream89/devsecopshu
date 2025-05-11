import streamlit as st
import os
import json

# Setup folders
os.makedirs("pdfs", exist_ok=True)
os.makedirs("references", exist_ok=True)
os.makedirs("prompts", exist_ok=True)

# Page state
if "step" not in st.session_state:
    st.session_state.step = "upload"

# Button actions
def go_home():
    st.session_state.step = "upload"

def proceed_to_select():
    st.session_state.step = "select"

st.title("PSCRF QA Frontend")

# --- Step 1: Upload Section ---
if st.session_state.step == "upload":
    st.header("Step 1: Upload Files")

    uploaded_pdfs = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    uploaded_references = st.file_uploader("Upload Reference JSONs", type="json", accept_multiple_files=True)
    uploaded_prompt = st.file_uploader("Upload Prompt JSON", type="json")

    if st.button("Submit"):
        pscrf_ids = set()

        # Save PDFs
        for pdf in uploaded_pdfs:
            path = os.path.join("pdfs", pdf.name)
            with open(path, "wb") as f:
                f.write(pdf.read())
            id_part = os.path.splitext(pdf.name)[0].split("_")[-1]
            if id_part.isdigit():
                pscrf_ids.add(id_part)

        # Save References
        for ref in uploaded_references:
            path = os.path.join("references", ref.name)
            with open(path, "wb") as f:
                f.write(ref.read())
            id_part = os.path.splitext(ref.name)[0].split("_")[-1]
            if id_part.isdigit():
                pscrf_ids.add(id_part)

        # Save Prompt
        if uploaded_prompt:
            prompt_path = os.path.join("prompts", uploaded_prompt.name)
            with open(prompt_path, "wb") as f:
                f.write(uploaded_prompt.read())
            st.session_state["prompt_filename"] = uploaded_prompt.name

        st.session_state["pscrf_ids"] = sorted(list(pscrf_ids))
        proceed_to_select()
        st.experimental_rerun()

# --- Step 2: Select PSCRF ID ---
if st.session_state.step == "select":
    st.header("Step 2: Select PSCRF ID")

    selected_id = st.selectbox("PSCRF ID", st.session_state.get("pscrf_ids", []), key="selected_pscrf_id")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Home"):
            go_home()
            st.experimental_rerun()

    with col2:
        if st.button("Submit"):
            st.session_state.step = "process"
            st.experimental_rerun()
