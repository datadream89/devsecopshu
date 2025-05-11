<!DOCTYPE html>
<html>
<head>
  <style>
    .highlight {
      background-color: yellow;
    }
  </style>
</head>
<body>
  <div id="pdf-container"></div>

  <script src="https://mozilla.github.io/pdf.js/build/pdf.js"></script>
  <script>
    const url = "{{ pdf_url }}";
    const highlights = {{ highlights_json | safe }};

    const container = document.getElementById("pdf-container");
    const loadingTask = pdfjsLib.getDocument(url);

    loadingTask.promise.then(pdf => {
      for (let i = 1; i <= pdf.numPages; i++) {
        pdf.getPage(i).then(page => {
          const scale = 1.5;
          const viewport = page.getViewport({ scale });

          const canvas = document.createElement("canvas");
          canvas.height = viewport.height;
          canvas.width = viewport.width;
          container.appendChild(canvas);

          const context = canvas.getContext("2d");
          const renderContext = {
            canvasContext: context,
            viewport: viewport
          };
          page.render(renderContext).promise.then(() => {
            page.getTextContent().then(textContent => {
              const snippet = highlights.find(h => h.pageNumber === page.pageNumber);
              if (snippet && snippet.text) {
                const ctx = canvas.getContext("2d");
                textContent.items.forEach(item => {
                  if (item.str && snippet.text.includes(item.str)) {
                    const tx = pdfjsLib.Util.transform(
                      viewport.transform,
                      item.transform
                    );
                    const x = tx[4];
                    const y = tx[5];
                    ctx.fillStyle = "yellow";
                    ctx.globalAlpha = 0.5;
                    ctx.fillRect(x, y - item.height, item.width, item.height);
                    ctx.globalAlpha = 1.0;
                  }
                });
              }
            });
          });
        });
      }
    });
  </script>
</body>
</html>
