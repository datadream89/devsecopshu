# webapp/pdf_viewer/__init__.py

import streamlit.components.v1 as components
import os
import tempfile
import shutil

def view_pdf(pdf_file_path):
    component_dir = os.path.dirname(__file__)
    index_path = os.path.join(component_dir, "pdf_component.html")

    tmp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    shutil.copy(pdf_file_path, tmp_pdf.name)
    pdf_url = f"file://{tmp_pdf.name}"

    with open(index_path) as f:
        html_content = f.read().replace("pdf_url", f"{pdf_url}")

    components.html(html_content, height=800, scrolling=True)
