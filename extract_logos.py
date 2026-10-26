import asyncio
from playwright.async_api import async_playwright
from PIL import Image

viewer_html = """<!DOCTYPE html>
<html>
<head>
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
</head>
<body style="margin:0; background:white;">
<canvas id="pdf-canvas"></canvas>
<script>
  pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
  const loadingTask = pdfjsLib.getDocument('file:///D:/rishin/ecobite.pdf');
  loadingTask.promise.then(function(pdf) {
    pdf.getPage(1).then(function(page) {
      const scale = 2.5;
      const viewport = page.getViewport({scale: scale});
      const canvas = document.getElementById('pdf-canvas');
      const context = canvas.getContext('2d');
      canvas.height = viewport.height;
      canvas.width = viewport.width;
      const renderContext = {
        canvasContext: context,
        viewport: viewport
      };
      page.render(renderContext).promise.then(function() {
        window.renderDone = true;
      });
    });
  });
</script>
</body>
</html>"""

with open("d:/surplus-food/render_pdf.html", "w", encoding="utf-8") as f:
    f.write(viewer_html)

async def capture():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1600, "height": 2200})
        await page.goto("file:///d:/surplus-food/render_pdf.html")
        await page.wait_for_function("() => window.renderDone === true", timeout=25000)
        canvas = await page.query_selector("#pdf-canvas")
        await canvas.screenshot(path="d:/surplus-food/ecobite_page1_hires.png")
        print("Captured ecobite_page1_hires.png successfully!")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture())
    # Crop the exact emblems from ecobite_page1_hires.png
    im = Image.open("d:/surplus-food/ecobite_page1_hires.png")
    w, h = im.size
    print(f"Rendered image size: {w}x{h}")
    # KTU logo is located around center y: 0.35 to 0.48
    # MEA logo is located around center y: 0.58 to 0.72
    # Let's inspect coordinates dynamically or crop bounding boxes
