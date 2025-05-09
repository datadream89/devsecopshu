<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.4.120/pdf.min.js"></script>
  <style>
    body { margin: 0; }
    canvas { display: block; margin: 0 auto; }
    #highlight {
      position: absolute;
      background: yellow;
      opacity: 0.4;
      pointer-events: none;
    }
  </style>
</head>
<body>
  <canvas id="pdf-canvas"></canvas>
  <script>
    const urlParams = new URLSearchParams(window.location.search);
    const pdfUrl = urlParams.get('pdf');
    const pageNum = parseInt(urlParams.get('page')) || 1;

    const canvas = document.getElementById('pdf-canvas');
    const ctx = canvas.getContext('2d');

    pdfjsLib.getDocument(pdfUrl).promise.then(pdf => {
      pdf.getPage(pageNum).then(page => {
        const viewport = page.getViewport({ scale: 1.5 });
        canvas.height = viewport.height;
        canvas.width = viewport.width;

        const renderContext = {
          canvasContext: ctx,
          viewport: viewport
        };
        page.render(renderContext);
      });
    });
  </script>
</body>
</html>
