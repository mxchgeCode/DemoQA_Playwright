from playwright.sync_api import Page
from locators.elements.text_box_locators import TextBoxLocators
from data import URLs


class TextBoxPage:
    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto(URLs.TEXT_BOX)

    def fill_user_name(self, name: str):
        self.page.fill(TextBoxLocators.USER_NAME, name)

    def fill_user_email(self, email: str):
        self.page.fill(TextBoxLocators.USER_EMAIL, email)

    def fill_current_address(self, address: str):
        self.page.fill(TextBoxLocators.CURRENT_ADDRESS, address)

    def fill_permanent_address(self, address: str):
        self.page.fill(TextBoxLocators.PERMANENT_ADDRESS, address)

    def submit(self):
        self.page.click(TextBoxLocators.SUBMIT_BUTTON)

    def get_output_name(self):
        return self.page.locator(TextBoxLocators.OUTPUT_NAME).inner_text()

    def get_output_email(self):
        return self.page.locator(TextBoxLocators.OUTPUT_EMAIL).inner_text()

    def get_output_current_address(self):
        return self.page.locator(TextBoxLocators.OUTPUT_CURRENT_ADDRESS).inner_text()

    def get_output_permanent_address(self):
        return self.page.locator(TextBoxLocators.OUTPUT_PERMANENT_ADDRESS).inner_text()
