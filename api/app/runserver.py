import streamlit as st
import uuid
import os

# Sample path to the generated highlighted PDF
highlighted_pdf_path = "pdfs/highlighted_example.pdf"

# PDF.js code to display the PDF with highlights
pdf_js_code = f"""
    <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.10.377/pdf.min.js"></script>
    <div style="width: 100%; height: 600px;">
        <canvas id="pdf-canvas" style="width: 100%; height: 100%;"></canvas>
    </div>
    <script>
        var url = '{highlighted_pdf_path}';
        var pdfjsLib = window['pdfjs-dist/build/pdf'];
        
        // Specify the workerSrc
        pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.10.377/pdf.worker.min.js';

        var pdfDoc = null,
            pageNum = 1,
            pageRendering = false,
            pageNumPending = null,
            scale = 1.5,
            canvas = document.getElementById('pdf-canvas'),
            ctx = canvas.getContext('2d');

        // Render the page
        function renderPage(num) {
            pageRendering = true;
            pdfDoc.getPage(num).then(function(page) {
                var viewport = page.getViewport({ scale: scale });
                canvas.height = viewport.height;
                canvas.width = viewport.width;

                var renderContext = {
                    canvasContext: ctx,
                    viewport: viewport
                };
                page.render(renderContext).promise.then(function() {
                    pageRendering = false;
                    if (pageNumPending !== null) {
                        renderPage(pageNumPending);
                        pageNumPending = null;
                    }
                });
            });
        }

        // Get document
        pdfjsLib.getDocument(url).promise.then(function(pdfDoc_) {
            pdfDoc = pdfDoc_;
            renderPage(pageNum);
        });
    </script>
"""

# Inject the custom HTML and JavaScript into the Streamlit app
st.markdown(pdf_js_code, unsafe_allow_html=True)

# Optional: Provide a download button
with open(highlighted_pdf_path, "rb") as pdf_file:
    st.download_button(
        label="Download Highlighted PDF",
        data=pdf_file,
        file_name="highlighted_output.pdf",
        mime="application/pdf"
    )
