from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.firefox.launch(headless=False)
    page = browser.new_page()
    page.goto("https://demoqa.com/alerts", wait_until="domcontentloaded", timeout=0)
    print("Page DOM is loaded")
    # можно добавить sleep или wait_for_selector для имплицитного ожидания элементов
    browser.close()
