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

    def click_new_user(self):
        self.page.click(LoginLocators.NEW_USER_BUTTON)

    def get_header_text(self):
        return self.page.text_content(LoginLocators.PAGE_HEADER)

    def click_register_button(self):
        self.page.click(LoginLocators.REGISTER_BUTTON)

    def is_field_invalid(self, field_locator: str):
        return self.page.is_visible(field_locator)

    def get_captcha_error(self):
        try:
            error_elem = self.page.locator(LoginLocators.CAPTCHA_ERROR)
            error_elem.wait_for(state="visible", timeout=7000)  # ждем до 7 сек
            return error_elem.text_content()
        except:
            return None

    def click_back_to_login(self):
        self.page.click(LoginLocators.BACK_TO_LOGIN_BUTTON)

    def fill_login_form(self, username, password):
        self.page.fill(LoginLocators.USER_NAME_LOGIN, username)
        self.page.fill(LoginLocators.PASSWORD_LOGIN, password)

    def click_login(self):
        self.page.click(LoginLocators.LOGIN_BUTTON)

    def get_logged_in_username(self):
        if self.page.is_visible(LoginLocators.USER_DISPLAY):
            return self.page.text_content(LoginLocators.USER_DISPLAY)
        return None

    def fill_registration_form(self, first_name, last_name, username, password):
        self.page.fill(LoginLocators.FIRST_NAME, first_name)
        self.page.fill(LoginLocators.LAST_NAME, last_name)
        self.page.fill(LoginLocators.USER_NAME_REG, username)
        self.page.fill(LoginLocators.PASSWORD_REG, password)