import streamlit as st
import json
import os
import fitz  # PyMuPDF to handle PDF rendering
from ai_logic.ai_backend import process_pdf_with_questions

# Set up page configurations
st.set_page_config(layout="wide")

# Step 1: PSCRF ID Selection Page
def step_1():
    st.title("PSCRF QA Explorer - Step 1")

    # Upload files for PDFs, prompt JSON, and reference JSON
    st.header("Upload Files")

    pdf_files = st.file_uploader("Upload PDF(s) with PSCRF ID", type="pdf", accept_multiple_files=True)
    prompt_json = st.file_uploader("Upload Prompt JSON", type="json")
    reference_files = st.file_uploader("Upload Reference JSON(s)", type="json", accept_multiple_files=True)

    # Step 2: Handle file uploads and saving to respective folders
    if st.button("Submit"):
        if pdf_files and prompt_json and reference_files:
            # Create necessary folders if not already created
            os.makedirs("pdfs", exist_ok=True)
            os.makedirs("prompts", exist_ok=True)
            os.makedirs("references", exist_ok=True)
            os.makedirs("outputs", exist_ok=True)

            # Save the uploaded files
            for pdf in pdf_files:
                with open(os.path.join("pdfs", pdf.name), "wb") as f:
                    f.write(pdf.getbuffer())

            prompt_data = json.load(prompt_json)
            for reference_file in reference_files:
                with open(os.path.join("references", reference_file.name), "wb") as f:
                    f.write(reference_file.getbuffer())

            # Load reference files into memory
            reference_data = {f.name: json.load(f) for f in reference_files}
            pscrf_options = list(reference_data.keys())
            selected_ref_file = st.selectbox("Select PSCRF ID (File)", pscrf_options)

            # After selection of PSCRF ID, go to the next page to render the PDF and questions
            if selected_ref_file:
                st.session_state.selected_ref_file = selected_ref_file
                st.session_state.reference_data = reference_data[selected_ref_file]
                st.session_state.pdf_files = pdf_files
                st.session_state.prompt_data = prompt_data

                # Redirect to step 2
                st.write("Processing the selected PSCRF ID... Moving to next page...")
                st.experimental_rerun()
        else:
            st.error("Please upload PDF, Prompt JSON, and Reference JSON files.")

# Step 2: PDF Rendering and Question Navigation Page
def step_2():
    st.title("PSCRF QA Explorer - Step 2")

    # Retrieve necessary data from session state
    selected_ref_file = st.session_state.get("selected_ref_file")
    reference_data = st.session_state.get("reference_data")
    pdf_files = st.session_state.get("pdf_files")
    prompt_data = st.session_state.get("prompt_data")

    # Get the PDF file that corresponds to the selected PSCRF ID
    pdf_file = next((f for f in pdf_files if selected_ref_file in f.name), None)

    if pdf_file:
        pdf_path = os.path.join("pdfs", pdf_file.name)

        # Run the backend function
        results = process_pdf_with_questions(pdf_path, prompt_data, reference_data, selected_ref_file)

        # Create an output directory and save the results to a file
        output_filename = os.path.join("outputs", f"{selected_ref_file}_output.json")
        with open(output_filename, "w") as output_file:
            json.dump({"results": results}, output_file, indent=4)

        # Display the results
        if results:
            st.write(f"Results for PSCRF ID: {selected_ref_file}")
            idx = st.session_state.get("idx", 0)
            if idx >= len(results):
                idx = 0

            # Display current result
            result = results[idx]
            st.write(f"**Question:** {result['question']}")
            st.write(f"**Answer:** {result['answer']}")
            st.write(f"**Page Number:** {result['pageNumber']}")
            st.write(f"**Accuracy:** {result['accuracyLevel']}%")
            st.write(f"**Valid:** {result['isValid']}")
            st.text_area("Matched Snippet:", result['matchedSnippet'], height=200)

            # PDF rendering
            st.write("Displaying PDF with highlighted snippet...")
            # Load the PDF and highlight the matched snippet
            doc = fitz.open(pdf_path)
            page = doc[result['pageNumber'] - 1]  # Get the correct page
            text = page.get_text("text")  # Extract text from the page
            highlighted_text = result['matchedSnippet']  # The snippet to highlight

            # Display PDF (you can use a custom method to highlight the text here)
            st.components.v1.html(f"""
                <embed src="{pdf_path}" width="100%" height="800px" type="application/pdf">
            """, height=800)

            # Navigation buttons for Next and Previous
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("Previous"):
                    st.session_state.idx -= 1
                    st.experimental_rerun()

            with col2:
                if st.button("Next"):
                    st.session_state.idx += 1
                    st.experimental_rerun()

    else:
        st.error("PDF not found. Please upload valid PDFs with the corresponding PSCRF ID.")

# Step 3: App flow control
if 'selected_ref_file' not in st.session_state:
    step_1()  # Show Step 1 (PSCRF ID selection)
else:
    step_2()  # Show Step 2 (PDF rendering and question navigation)
