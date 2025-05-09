import os
import json
import streamlit as st
from ai_logic.ai_backend import generate_output

st.set_page_config(layout="wide")
st.title("Multi-File PDF QA with LLM")

uploaded_pdfs = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)
uploaded_refs = st.file_uploader("Upload reference JSONs", type="json", accept_multiple_files=True)
uploaded_prompts = st.file_uploader("Upload prompt JSONs", type="json", accept_multiple_files=True)

if st.button("Run Analysis"):
    os.makedirs("pdfs", exist_ok=True)
    os.makedirs("prompts", exist_ok=True)
    os.makedirs("references", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    for pdf_file, ref_file, prompt_file in zip(uploaded_pdfs, uploaded_refs, uploaded_prompts):
        pdf_path = os.path.join("pdfs", pdf_file.name)
        ref_path = os.path.join("references", ref_file.name)
        prompt_path = os.path.join("prompts", prompt_file.name)
        output_path = os.path.join("outputs", ref_file.name.replace(".json", "_outcome.json"))

        with open(pdf_path, "wb") as f:
            f.write(pdf_file.getbuffer())
        with open(ref_path, "wb") as f:
            f.write(ref_file.getbuffer())
        with open(prompt_path, "wb") as f:
            f.write(prompt_file.getbuffer())

        generate_output(pdf_path, ref_path, prompt_path, output_path)

    st.success("Outputs generated successfully!")

# Viewer section
output_files = [f for f in os.listdir("outputs") if f.endswith("_outcome.json")]
if output_files:
    selected_file = st.selectbox("Select PSCRF Output", output_files)
    with open(os.path.join("outputs", selected_file)) as f:
        results = json.load(f)

    index = st.session_state.get("index", 0)
    if st.button("Next"):
        st.session_state.index = (index + 1) % len(results)

    current_result = results[st.session_state.get("index", 0)]
    st.json(current_result)
