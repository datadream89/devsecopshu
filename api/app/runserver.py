<!DOCTYPE html>
<html>
  <head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.4.120/pdf.min.js"></script>
    <style>
      body { margin: 0; overflow: auto; }
      #pdf-viewer canvas { margin: auto; display: block; }
    </style>
  </head>
  <body>
    <div id="pdf-viewer"></div>
    <script>
      const pdfViewer = document.getElementById("pdf-viewer");
      const url = new URLSearchParams(window.location.search).get("pdf_url");

      const renderPDF = async (url) => {
        const pdf = await pdfjsLib.getDocument(url).promise;
        for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
          const page = await pdf.getPage(pageNum);
          const canvas = document.createElement("canvas");
          const context = canvas.getContext("2d");
          const viewport = page.getViewport({ scale: 1.5 });
          canvas.height = viewport.height;
          canvas.width = viewport.width;

          await page.render({ canvasContext: context, viewport }).promise;
          pdfViewer.appendChild(canvas);
        }
      };

      renderPDF(url);
    </script>
  </body>
</html>
