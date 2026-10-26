import asyncio
from playwright.async_api import async_playwright
import os

os.makedirs('d:/surplus-food/screenshots', exist_ok=True)

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # 1. Customer
        ctx = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await ctx.new_page()
        await page.goto('http://localhost:5173/auth')
        await page.fill('input[type="email"]', 'customer@surplus.com')
        await page.fill('input[type="password"]', 'customer123')
        await page.click('button[type="submit"]')
        await page.wait_for_url('**/customer/dashboard', timeout=15000)
        await page.wait_for_timeout(2000)
        await page.screenshot(path='d:/surplus-food/screenshots/03_customer_dashboard.png')
        print('Captured 03_customer_dashboard.png')
        
        await page.goto('http://localhost:5173/customer/orders')
        await page.wait_for_timeout(2000)
        await page.screenshot(path='d:/surplus-food/screenshots/04_customer_orders.png')
        print('Captured 04_customer_orders.png')
        await ctx.close()
        
        # 2. Restaurant
        ctx2 = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page2 = await ctx2.new_page()
        await page2.goto('http://localhost:5173/auth')
        await page2.fill('input[type="email"]', 'restaurant@surplus.com')
        await page2.fill('input[type="password"]', 'restaurant123')
        await page2.click('button[type="submit"]')
        await page2.wait_for_url('**/restaurant/dashboard', timeout=15000)
        await page2.wait_for_timeout(2000)
        await page2.screenshot(path='d:/surplus-food/screenshots/06_restaurant_dashboard.png')
        print('Captured 06_restaurant_dashboard.png')
        
        await page2.goto('http://localhost:5173/restaurant/reservations')
        await page2.wait_for_timeout(2000)
        await page2.screenshot(path='d:/surplus-food/screenshots/07_restaurant_reservations.png')
        print('Captured 07_restaurant_reservations.png')
        await ctx2.close()
        
        # 3. Admin
        ctx3 = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page3 = await ctx3.new_page()
        await page3.goto('http://localhost:5173/auth')
        await page3.fill('input[type="email"]', 'admin@surplus.com')
        await page3.fill('input[type="password"]', 'admin123')
        await page3.click('button[type="submit"]')
        await page3.wait_for_url('**/admin/dashboard', timeout=15000)
        await page3.wait_for_timeout(2000)
        await page3.screenshot(path='d:/surplus-food/screenshots/08_admin_dashboard.png')
        print('Captured 08_admin_dashboard.png')
        
        await page3.goto('http://localhost:5173/admin/restaurants')
        await page3.wait_for_timeout(2000)
        await page3.screenshot(path='d:/surplus-food/screenshots/09_admin_verification.png')
        print('Captured 09_admin_verification.png')
        
        await page3.goto('http://localhost:5173/admin/listings')
        await page3.wait_for_timeout(2000)
        await page3.screenshot(path='d:/surplus-food/screenshots/10_admin_listings.png')
        print('Captured 10_admin_listings.png')
        await ctx3.close()
        
        await browser.close()
        print('All screenshots captured with active data!')

if __name__ == '__main__':
    asyncio.run(run())
