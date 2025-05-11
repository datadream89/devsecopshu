import streamlit as st
import os
import json
import uuid
from ai_logic.ai_backend import process_pdf_with_questions

# Create folders if not exists
for folder in ["pdfs", "prompts", "references", "outputs"]:
    os.makedirs(folder, exist_ok=True)

st.set_page_config(layout="wide")
st.title("PSCRF QA Explorer")

# Session control
if "page" not in st.session_state:
    st.session_state.page = "upload"

def go_home():
    st.session_state.page = "upload"

def go_to_select():
    st.session_state.page = "select"

def go_to_output():
    st.session_state.page = "output"
    st.session_state.idx = 0

# Step 1: Upload files
if st.session_state.page == "upload":
    st.subheader("Step 1: Upload Files")

    pdfs = st.file_uploader("Upload PDF(s)", type="pdf", accept_multiple_files=True)
    prompts = st.file_uploader("Upload Prompt JSON", type="json")
    references = st.file_uploader("Upload Reference JSON(s)", type="json", accept_multiple_files=True)

    if st.button("Submit Uploads"):
        if prompts:
            with open(os.path.join("prompts", prompts.name), "wb") as f:
                f.write(prompts.read())

        for pdf in pdfs or []:
            with open(os.path.join("pdfs", pdf.name), "wb") as f:
                f.write(pdf.read())

        for ref in references or []:
            with open(os.path.join("references", ref.name), "wb") as f:
                f.write(ref.read())

        go_to_select()

# Step 2: Choose PSCRF ID
elif st.session_state.page == "select":
    st.subheader("Step 2: Select PSCRF ID")

    reference_files = [f for f in os.listdir("references") if f.endswith(".json")]
    pscrf_ids = [os.path.splitext(f)[0] for f in reference_files]

    selected_id = st.selectbox("PSCRF ID", pscrf_ids)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Home"):
            go_home()
    with col2:
        if st.button("Submit"):
            prompt_path = next((os.path.join("prompts", f) for f in os.listdir("prompts") if f.endswith(".json")), None)
            reference_path = os.path.join("references", f"{selected_id}.json")
            pdf_path = next((os.path.join("pdfs", f) for f in os.listdir("pdfs") if selected_id in f), None)

            if prompt_path and os.path.exists(reference_path) and os.path.exists(pdf_path):
                with open(prompt_path) as f:
                    prompt_data = json.load(f)
                with open(reference_path) as f:
                    reference_data = json.load(f)

                results = process_pdf_with_questions(pdf_path, prompt_data, reference_data, selected_id)
                output_file = os.path.join("outputs", f"{selected_id}_outcome.json")
                with open(output_file, "w") as f:
                    json.dump({"results": results}, f, indent=2)

                st.session_state.selected_id = selected_id
                st.session_state.output_data = results
                st.session_state.pdf_path = pdf_path
                go_to_output()

# Step 3: Display Results
elif st.session_state.page == "output":
    st.subheader(f"Results for PSCRF ID: {st.session_state.selected_id}")

    output = st.session_state.output_data
    idx = st.session_state.idx
    if idx >= len(output):
        idx = 0
    q = output[idx]

    # Highlighted PDF
    import fitz
    doc = fitz.open(st.session_state.pdf_path)
    snippet_parts = q["matchedSnippet"].split(". ")
    for page in doc:
        for part in snippet_parts:
            part = part.strip()
            if len(part) > 10 and part in page.get_text():
                for area in page.search_for(part):
                    highlight = page.add_highlight_annot(area)
                    highlight.update()
    unique_name = f"highlighted_{uuid.uuid4().hex[:8]}.pdf"
    highlighted_path = os.path.join("pdfs", unique_name)
    doc.save(highlighted_path)

    st.markdown(f'<iframe src="pdfs/{unique_name}" width="100%" height="600px"></iframe>', unsafe_allow_html=True)

    st.markdown(f"**Scenario ID:** {q['scenarioId']}")
    st.markdown(f"**QuestionRef ID:** {q['questionRefId']}")
    st.markdown(f"**Question:** {q['question']}")
    st.markdown(f"**Answer:** {q['answer']}")
    st.markdown(f"**Page Number:** {q['pageNumber']}")
    st.markdown(f"**Accuracy:** {q['accuracyLevel']}%")
    st.markdown(f"**Valid:** {q['isValid']}")
    st.text_area("Snippet:", q["matchedSnippet"], height=200)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("Previous") and idx > 0:
            st.session_state.idx -= 1
    with col2:
        if st.button("Home"):
            go_home()
    with col3:
        if st.button("Next") and idx < len(output) - 1:
            st.session_state.idx += 1
