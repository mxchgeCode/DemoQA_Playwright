from playwright.sync_api import Page
from locators.elements.buttons_locators import ButtonsLocators
from data import URLs


class ButtonsPage:
    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto(URLs.PAGE_BTN)

    def double_click_button(self):
        self.page.dblclick(ButtonsLocators.DOUBLE_CLICK_BUTTON)

    def right_click_button(self):
        self.page.click(ButtonsLocators.RIGHT_CLICK_BUTTON, button="right")

    def click_me_button(self):
        button = self.page.locator("button.btn.btn-primary").nth(2)
        button.click()

    def get_double_click_message(self) -> str:
        return self.page.locator(ButtonsLocators.DOUBLE_CLICK_MESSAGE).inner_text()

    def get_right_click_message(self) -> str:
        return self.page.locator(ButtonsLocators.RIGHT_CLICK_MESSAGE).inner_text()

    def get_click_me_message(self) -> str:
        return self.page.locator(ButtonsLocators.CLICK_ME_MESSAGE).inner_text()
