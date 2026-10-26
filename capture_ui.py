import asyncio
from playwright.async_api import async_playwright
import os

os.makedirs('d:/surplus-food/screenshots', exist_ok=True)

async def take_screenshots():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # 1. Landing Page
        print("Capturing Landing Page...")
        context1 = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page1 = await context1.new_page()
        await page1.goto('http://localhost:5173/')
        await page1.wait_for_timeout(2000)
        await page1.screenshot(path='d:/surplus-food/screenshots/01_landing.png')
        await context1.close()
        
        # 2. Login Page
        print("Capturing Login Page...")
        context2 = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page2 = await context2.new_page()
        await page2.goto('http://localhost:5173/auth')
        await page2.wait_for_timeout(2000)
        await page2.screenshot(path='d:/surplus-food/screenshots/02_login.png')
        await context2.close()
        
        # 3. Customer Session
        print("Capturing Customer Views...")
        context_cust = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page_cust = await context_cust.new_page()
        await page_cust.goto('http://localhost:5173/auth')
        await page_cust.wait_for_timeout(1000)
        await page_cust.fill('input[type="email"]', 'customer@surplus.com')
        await page_cust.fill('input[type="password"]', 'customer123')
        await page_cust.click('button[type="submit"]')
        await page_cust.wait_for_timeout(3000)
        await page_cust.screenshot(path='d:/surplus-food/screenshots/03_customer_dashboard.png')
        print("Captured 03_customer_dashboard.png")
        
        # 4. Customer Orders
        await page_cust.goto('http://localhost:5173/customer/orders')
        await page_cust.wait_for_timeout(2000)
        await page_cust.screenshot(path='d:/surplus-food/screenshots/04_customer_orders.png')
        print("Captured 04_customer_orders.png")
        
        # 5. Customer Profile
        await page_cust.goto('http://localhost:5173/customer/profile')
        await page_cust.wait_for_timeout(2000)
        await page_cust.screenshot(path='d:/surplus-food/screenshots/05_customer_profile.png')
        print("Captured 05_customer_profile.png")
        await context_cust.close()
        
        # 6. Restaurant Session
        print("Capturing Restaurant Views...")
        context_rest = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page_rest = await context_rest.new_page()
        await page_rest.goto('http://localhost:5173/auth')
        await page_rest.wait_for_timeout(1000)
        await page_rest.fill('input[type="email"]', 'restaurant@surplus.com')
        await page_rest.fill('input[type="password"]', 'restaurant123')
        await page_rest.click('button[type="submit"]')
        await page_rest.wait_for_timeout(3000)
        await page_rest.screenshot(path='d:/surplus-food/screenshots/06_restaurant_dashboard.png')
        print("Captured 06_restaurant_dashboard.png")
        
        # 7. Restaurant Reservations
        await page_rest.goto('http://localhost:5173/restaurant/reservations')
        await page_rest.wait_for_timeout(2000)
        await page_rest.screenshot(path='d:/surplus-food/screenshots/07_restaurant_reservations.png')
        print("Captured 07_restaurant_reservations.png")
        await context_rest.close()
        
        # 8. Admin Session
        print("Capturing Admin Views...")
        context_admin = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page_admin = await context_admin.new_page()
        await page_admin.goto('http://localhost:5173/auth#admin')
        await page_admin.wait_for_timeout(1500)
        await page_admin.click('button[type="submit"]')
        await page_admin.wait_for_timeout(3000)
        await page_admin.screenshot(path='d:/surplus-food/screenshots/08_admin_dashboard.png')
        print("Captured 08_admin_dashboard.png")
        
        # 9. Admin Restaurant Verification
        await page_admin.goto('http://localhost:5173/admin/restaurants')
        await page_admin.wait_for_timeout(2000)
        await page_admin.screenshot(path='d:/surplus-food/screenshots/09_admin_verification.png')
        print("Captured 09_admin_verification.png")
        
        # 10. Admin System Listings
        await page_admin.goto('http://localhost:5173/admin/listings')
        await page_admin.wait_for_timeout(2000)
        await page_admin.screenshot(path='d:/surplus-food/screenshots/10_admin_listings.png')
        print("Captured 10_admin_listings.png")
        await context_admin.close()
        
        await browser.close()
        print('All 10 screenshots captured successfully!')

if __name__ == "__main__":
    asyncio.run(take_screenshots())
