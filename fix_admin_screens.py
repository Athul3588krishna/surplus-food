import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await ctx.new_page()
        
        # Login as Admin
        await page.goto('http://localhost:5173/auth')
        await page.fill('input[type="email"]', 'admin@surplus.com')
        await page.fill('input[type="password"]', 'admin123')
        await page.click('button[type="submit"]')
        await page.wait_for_url('**/admin/dashboard', timeout=15000)
        
        # Capture Verification page
        await page.goto('http://localhost:5173/admin/verifications')
        await page.wait_for_timeout(2000)
        await page.screenshot(path='d:/surplus-food/screenshots/09_admin_verification.png')
        print('Captured 09_admin_verification.png')
        
        # Capture System Listings page
        await page.goto('http://localhost:5173/admin/listings')
        await page.wait_for_timeout(2000)
        await page.screenshot(path='d:/surplus-food/screenshots/10_admin_listings.png')
        print('Captured 10_admin_listings.png')
        
        await browser.close()
        print('Admin screens captured successfully!')

if __name__ == '__main__':
    asyncio.run(run())
