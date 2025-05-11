import streamlit as st
import json
import os
from ai_logic.ai_backend import process_pdf_with_questions

# Setting page config for the Streamlit app
st.set_page_config(layout="wide")
st.title("PSCRF QA Explorer")

# Upload PDF files, Prompt JSON, and Reference JSON files
pdf_files = st.file_uploader("Upload PDF(s)", type="pdf", accept_multiple_files=True)
prompt_json = st.file_uploader("Upload Prompt JSON", type="json")
reference_files = st.file_uploader("Upload Reference JSON(s)", type="json", accept_multiple_files=True)

# After files are uploaded, proceed with the next step
if pdf_files and prompt_json and reference_files:
    # Load the uploaded JSON files
    prompt_data = json.load(prompt_json)
    reference_data = {f.name: json.load(f) for f in reference_files}

    # Dropdown to select the reference file (PSCRF ID)
    pscrf_options = list(reference_data.keys())
    selected_ref_file = st.selectbox("Select PSCRF ID (File)", pscrf_options)

    # Get the corresponding reference data for the selected PSCRF ID
    reference = reference_data[selected_ref_file]

    # Match the selected reference file with the uploaded PDFs
    pdf_file = next((f for f in pdf_files if selected_ref_file.startswith(os.path.splitext(f.name)[0])), None)

    if pdf_file:
        # Save PDF to a temporary path
        pdf_path = os.path.join("/mnt", "wsl", "pdfs", pdf_file.name)
        with open(pdf_path, "wb") as f:
            f.write(pdf_file.read())

        # Process the PDF and generate answers for the questions in the reference JSON
        output = process_pdf_with_questions(pdf_path, prompt_data, reference, selected_ref_file)

        # Initialize session state to track question index for navigation
        idx = st.session_state.get("idx", 0)
        if idx >= len(output):
            idx = 0

        st.session_state["idx"] = idx

        # Display output (question, answer, page number, accuracy, validity)
        if output:
            q = output[idx]
            st.write(f"**Question:** {q['question']}")
            st.write(f"**Answer:** {q['answer']}")
            st.write(f"**Page Number:** {q['pageNumber']}")
            st.write(f"**Accuracy:** {q['accuracyLevel']}%")
            st.write(f"**Valid:** {q['isValid']}")
            st.text_area("Snippet:", q['matchedSnippet'], height=200)

            # Display the PDF with the highlighted snippet for the question's page
            st.write(f"**Displaying Page {q['pageNumber']}**:")
            # PDF file path
            pdf_display_path = f"/mnt/c/{pdf_path.replace('/mnt/wsl', '')}"
            st.markdown(f'<embed src="file:///{pdf_display_path}" width="100%" height="800px" type="application/pdf">', unsafe_allow_html=True)

            # Next button to move to the next question
            if st.button("Next"):
                st.session_state["idx"] += 1
                st.experimental_rerun()

            # Back button to upload more files
            if st.button("Back to Upload"):
                st.session_state.clear()
                st.experimental_rerun()

