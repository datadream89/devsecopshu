# webapp/app.py - Step 1: Upload and save files

import streamlit as st
import os

# Create folders if they don't exist
os.makedirs("pdfs", exist_ok=True)
os.makedirs("prompts", exist_ok=True)
os.makedirs("references", exist_ok=True)

st.title("Step 1: Upload Files")

with st.form("file_upload_form"):
    uploaded_pdfs = st.file_uploader("Upload PDF(s)", type="pdf", accept_multiple_files=True)
    uploaded_prompt = st.file_uploader("Upload Prompt JSON", type="json", accept_multiple_files=False)
    uploaded_references = st.file_uploader("Upload Reference JSON(s)", type="json", accept_multiple_files=True)

    submitted = st.form_submit_button("Submit Files")

if submitted:
    # Save PDFs
    if uploaded_pdfs:
        for pdf in uploaded_pdfs:
            with open(os.path.join("pdfs", pdf.name), "wb") as f:
                f.write(pdf.read())
        st.success(f"{len(uploaded_pdfs)} PDF(s) saved to /pdfs")

    # Save Prompt JSON
    if uploaded_prompt:
        with open(os.path.join("prompts", uploaded_prompt.name), "wb") as f:
            f.write(uploaded_prompt.read())
        st.success(f"Prompt JSON saved to /prompts")

    # Save Reference JSONs
    if uploaded_references:
        for ref in uploaded_references:
            with open(os.path.join("references", ref.name), "wb") as f:
                f.write(ref.read())
        st.success(f"{len(uploaded_references)} Reference JSON(s) saved to /references")

    st.session_state["uploaded"] = True
