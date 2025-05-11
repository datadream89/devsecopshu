import streamlit as st
import json
import os
import re
import base64

# Utility to extract digits from filename
def extract_id(filename):
    match = re.search(r'(\d+)', filename)
    return match.group(1) if match else None

# Load available outputs
output_dir = "outputs"
output_files = [f for f in os.listdir(output_dir) if f.endswith("_outcome.json")]
pscrf_ids = [extract_id(f) for f in output_files]

st.title("PSCRF Review Panel")

if "step" not in st.session_state:
    st.session_state.step = 1
if "selected_pscrf" not in st.session_state:
    st.session_state.selected_pscrf = None
if "current_index" not in st.session_state:
    st.session_state.current_index = 0

if st.session_state.step == 1:
    st.subheader("Step 1: Choose PSCRF ID")
    selected = st.selectbox("Select PSCRF ID", pscrf_ids)
    col1, col2 = st.columns(2)
    if col1.button("Submit"):
        st.session_state.selected_pscrf = selected
        st.session_state.step = 2
        st.session_state.current_index = 0
        st.rerun()
    if col2.button("Home"):
        st.session_state.step = 1
        st.rerun()

elif st.session_state.step == 2:
    st.subheader(f"Results for PSCRF ID: {st.session_state.selected_pscrf}")

    # Load output
    filename = f"prompt_dict_{st.session_state.selected_pscrf}_outcome.json"
    with open(os.path.join("outputs", filename), "r") as f:
        data = json.load(f)["results"]

    idx = st.session_state.current_index
    entry = data[idx]

    st.write(f"**Scenario ID**: {entry['scenarioId']}")
    st.write(f"**Question ID**: {entry['questionId']}")
    st.write(f"**Question**: {entry['question']}")
    st.write(f"**Answer**: {entry['answer']}")
    st.write(f"**Accuracy**: {entry['accuracyLevel']}%")
    st.write(f"**Valid**: {entry['isValid']}")

    st.text_area("Matched Snippet", entry["matchedSnippet"], height=200)

    # PDF rendering with highlight
    def render_pdf_with_highlight(pdf_path, text):
        import fitz  # PyMuPDF
        doc = fitz.open(pdf_path)
        highlight_pages = []
        for page_num, page in enumerate(doc):
            if text in page.get_text():
                highlight_pages.append(page_num)
                areas = page.search_for(text)
                for area in areas:
                    highlight = page.add_highlight_annot(area)
                    highlight.update()
        output_path = os.path.join("pdfs", "highlighted_temp.pdf")
        doc.save(output_path)
        return output_path

    input_pdf_path = os.path.join("pdfs", entry["filename"])
    highlighted_pdf = render_pdf_with_highlight(input_pdf_path, entry["matchedSnippet"])

    with open(highlighted_pdf, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600px" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    if col1.button("Previous") and idx > 0:
        st.session_state.current_index -= 1
        st.rerun()
    if col2.button("Next") and idx < len(data) - 1:
        st.session_state.current_index += 1
        st.rerun()
