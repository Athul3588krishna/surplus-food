import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await ctx.new_page()
        
        await page.goto('http://localhost:5173/auth')
        await page.fill('input[type="email"]', 'restaurant@surplus.com')
        await page.fill('input[type="password"]', 'restaurant123')
        await page.click('button[type="submit"]')
        await page.wait_for_url('**/restaurant/dashboard', timeout=15000)
        await page.wait_for_timeout(3500)
        await page.screenshot(path='d:/surplus-food/screenshots/06_restaurant_dashboard.png')
        print('Captured 06_restaurant_dashboard.png!')
        
        await page.goto('http://localhost:5173/restaurant/reservations')
        await page.wait_for_timeout(3500)
        await page.screenshot(path='d:/surplus-food/screenshots/07_restaurant_reservations.png')
        print('Captured 07_restaurant_reservations.png!')
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(run())
