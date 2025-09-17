# pages/links_page.py
from playwright.sync_api import Page, expect
from locators.elements.links_locators import LinksLocators


class LinksPage:
    def __init__(self, page: Page):
        self.page = page
        self.locators = LinksLocators()

    def open(self):
        self.page.goto("https://demoqa.com/links")

    def click_home_link(self):
        self.page.locator(self.locators.SIMPLE_LINK).click()

    def click_home79udw_link(self):
        self.page.locator(self.locators.DYNAMIC_LINK).click()

    def click_link_and_check_response(self, locator: str, expected_text: str):
        self.page.locator(locator).click()
        expect(self.page.locator(self.locators.LINK_RESPONSE_MESSAGE)).to_have_text(
            expected_text
        )
