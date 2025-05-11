
import streamlit as st
import streamlit.components.v1 as components
import base64
import os

def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    
    pdf_display = f"""
        <iframe 
            src="data:application/pdf;base64,{base64_pdf}" 
            width="100%" height="800px" type="application/pdf">
        </iframe>
    """
    components.html(pdf_display, height=800, width=1000)

# Usage
pdf_path = "pdfs/pscrf_101.pdf"  # adjust to your filename
if os.path.exists(pdf_path):
    show_pdf(pdf_path)
else:
    st.error("PDF not found.")
