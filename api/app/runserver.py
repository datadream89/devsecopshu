import streamlit as st
import json
import os
from ai_logic.ai_backend import process_pdf_with_questions

# Define directory paths
prompts_dir = os.path.join(os.getcwd(), 'prompts')
references_dir = os.path.join(os.getcwd(), 'references')
pdf_dir = os.path.join(os.getcwd(), 'pdfs')

# Ensure the directories exist
os.makedirs(prompts_dir, exist_ok=True)
os.makedirs(references_dir, exist_ok=True)
os.makedirs(pdf_dir, exist_ok=True)

st.set_page_config(layout="wide")
st.title("PSCRF QA Explorer")

# File uploaders for PDFs, Prompt JSON, and Reference JSON
pdf_files = st.file_uploader("Upload PDF(s)", type="pdf", accept_multiple_files=True)
prompt_json = st.file_uploader("Upload Prompt JSON", type="json")
reference_files = st.file_uploader("Upload Reference JSON(s)", type="json", accept_multiple_files=True)

if pdf_files and prompt_json and reference_files:
    # Save Prompt JSON to prompts folder
    prompt_json_path = os.path.join(prompts_dir, prompt_json.name)
    with open(prompt_json_path, "wb") as f:
        f.write(prompt_json.read())
    
    # Save Reference JSON files to references folder
    reference_data = {}
    for ref_file in reference_files:
        ref_file_path = os.path.join(references_dir, ref_file.name)
        with open(ref_file_path, "wb") as f:
            f.write(ref_file.read())
        reference_data[ref_file.name] = json.load(open(ref_file_path))

    # Load prompt data
    prompt_data = json.load(open(prompt_json_path))

    # Get PSCRF ID options for dropdown based on uploaded reference files
    pscrf_options = list(reference_data.keys())
    selected_ref_file = st.selectbox("Select PSCRF ID (File)", pscrf_options)

    reference = reference_data[selected_ref_file]
    pdf_file = next((f for f in pdf_files if selected_ref_file.startswith(os.path.splitext(f.name)[0])), None)

    if pdf_file:
        # Adjust path for WSL-compatible location
        pdf_path = os.path.join("/mnt/c/users/G84100/OneDrive - Ni/Documents/GitHub/pscrf-Gena/pdfs", pdf_file.name)
        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
        with open(pdf_path, "wb") as f:
            f.write(pdf_file.read())

        # Process the PDF with the corresponding questions from the reference JSON
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
