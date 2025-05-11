import streamlit as st
import os
import re

# Set up directories
os.makedirs("pdfs", exist_ok=True)
os.makedirs("prompts", exist_ok=True)
os.makedirs("references", exist_ok=True)

st.title("PSCRF File Upload")

# File upload inside a form
with st.form(key="upload_form"):
    uploaded_pdfs = st.file_uploader("Upload PDF(s)", type="pdf", accept_multiple_files=True)
    uploaded_prompt = st.file_uploader("Upload Prompt JSON", type="json")
    uploaded_references = st.file_uploader("Upload Reference JSON(s)", type="json", accept_multiple_files=True)
    
    submit_button = st.form_submit_button(label="Submit Files")

# File saving logic after submission
if submit_button:
    if uploaded_pdfs:
        for pdf in uploaded_pdfs:
            with open(os.path.join("pdfs", pdf.name), "wb") as f:
                f.write(pdf.read())
        st.success(f"Saved {len(uploaded_pdfs)} PDF(s)")

    if uploaded_prompt:
        with open(os.path.join("prompts", uploaded_prompt.name), "wb") as f:
            f.write(uploaded_prompt.read())
        st.success("Saved Prompt JSON")

    if uploaded_references:
        for ref in uploaded_references:
            with open(os.path.join("references", ref.name), "wb") as f:
                f.write(ref.read())
        st.success(f"Saved {len(uploaded_references)} Reference JSON(s)")

    st.session_state["uploaded"] = True

# Step 2: Show dropdown for PSCRF ID after submit
if st.session_state.get("uploaded", False):
    reference_files = os.listdir("references")

    # Extract PSCRF IDs from filenames like 'prompt_dict_101.json' -> '101'
    pscrf_ids = []
    for filename in reference_files:
        match = re.search(r"(\d+)", filename)
        if match:
            pscrf_ids.append(match.group(1))

    pscrf_ids = sorted(set(pscrf_ids))  # remove duplicates

    selected_id = st.selectbox("PSCRF ID", pscrf_ids)
    st.session_state["selected_pscrf_id"] = selected_id
