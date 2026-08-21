import asyncio
from playwright.async_api import async_playwright

html = """<!DOCTYPE html>
<html>
<head>
<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
<script>mermaid.initialize({startOnLoad:true});</script>
</head>
<body>
<div class="mermaid">
graph TD
    A[Customer] --> B[System]
</div>
</body>
</html>"""

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_content(html)
        await page.wait_for_selector('.mermaid svg', timeout=10000)
        print('Mermaid rendered SVG successfully!')
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test())
