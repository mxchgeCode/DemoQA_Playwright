import time

from locators.bookstore.login_locators import LoginLocators
from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    def login(self, username: str, password: str):
        self.page.fill(LoginLocators.USERNAME_INPUT, username)
        self.page.fill(LoginLocators.PASSWORD_INPUT, password)
        self.page.click(LoginLocators.LOGIN_BUTTON)
        time.sleep(5)

    def get_error_message(self):
        try:
            # Ожидаем появления элемента ошибки до 5 секунд
            error_elem = self.page.locator(LoginLocators.ERROR_MESSAGE)
            error_elem.wait_for(state="visible", timeout=5000)
            return error_elem.text_content()
        except:
            return None
