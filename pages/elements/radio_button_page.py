from playwright.sync_api import Page
from locators.elements.radio_button_locators import RadioButtonLocators
from data import URLs

class RadioButtonPage:
    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto(URLs.RADIO_BTN)

    def select_yes(self):
        self.page.click(RadioButtonLocators.YES_RADIO)

    def select_impressive(self):
        self.page.click(RadioButtonLocators.IMPRESSIVE_RADIO)

    def select_no(self):
        # No radio is disabled, but click anyway for test
        self.page.click(RadioButtonLocators.NO_RADIO, timeout=500)

    def get_result_text(self) -> str:
        return self.page.locator(RadioButtonLocators.RESULT_TEXT).inner_text()
