"""
Page Object для страницы авторизации BookStore.
Содержит методы для входа, регистрации и управления учетными записями.
"""

import logging
from typing import Optional
from playwright.sync_api import Page

from pages.base_page import BasePage
from locators.bookstore.login_locators import LoginLocators

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """
    Страница авторизации и регистрации пользователей BookStore.
    Наследует от BasePage общие методы взаимодействия с элементами.
    """

    def __init__(self, page: Page):
        """
        Инициализация страницы логина.

        Args:
            page: Экземпляр страницы Playwright
        """
        super().__init__(page)

    def login(self, username: str, password: str) -> None:
        """
        Выполняет вход в систему с указанными учетными данными.

        Args:
            username: Имя пользователя
            password: Пароль
        """
        self.log_step(f"Выполняем вход пользователя: {username}")
        self.safe_fill(LoginLocators.USERNAME_INPUT, username)
        self.safe_fill(LoginLocators.PASSWORD_INPUT, password)
        self.safe_click(LoginLocators.LOGIN_BUTTON)

    def fill_login_form(self, username: str, password: str) -> None:
        """
        Заполняет форму логина без отправки.

        Args:
            username: Имя пользователя
            password: Пароль
        """
        self.log_step(f"Заполняем форму логина для пользователя: {username}")
        self.safe_fill(LoginLocators.USER_NAME_LOGIN, username)
        self.safe_fill(LoginLocators.PASSWORD_LOGIN, password)

    def click_new_user(self) -> None:
        """
        Переходит на страницу регистрации нового пользователя.
        """
        self.log_step("Переходим к регистрации нового пользователя")
        self.safe_click(LoginLocators.NEW_USER_BUTTON)

    def fill_registration_form(
        self, first_name: str, last_name: str, username: str, password: str
    ) -> None:
        """
        Заполняет форму регистрации нового пользователя.

        Args:
            first_name: Имя
            last_name: Фамилия
            username: Имя пользователя
            password: Пароль
        """
        self.log_step(f"Заполняем форму регистрации для: {username}")
        self.safe_fill(LoginLocators.FIRST_NAME, first_name)
        self.safe_fill(LoginLocators.LAST_NAME, last_name)
        self.safe_fill(LoginLocators.USER_NAME_REG, username)
        self.safe_fill(LoginLocators.PASSWORD_REG, password)

    def click_register_button(self) -> None:
        """
        Нажимает кнопку регистрации пользователя.
        """
        self.log_step("Нажимаем кнопку регистрации")
        self.safe_click(LoginLocators.REGISTER_BUTTON)

    def click_back_to_login(self) -> None:
        """
        Возвращается на страницу входа из формы регистрации.
        """
        self.log_step("Возвращаемся на страницу входа")
        self.safe_click(LoginLocators.BACK_TO_LOGIN_BUTTON)

    def get_header_text(self) -> Optional[str]:
        """
        Получает текст заголовка текущей страницы.

        Returns:
            str или None: Текст заголовка или None если не найден
        """
        return self.get_text_safe(LoginLocators.PAGE_HEADER)

    def get_error_message(self) -> Optional[str]:
        """
        Получает сообщение об ошибке при неудачной авторизации.

        Returns:
            str или None: Текст ошибки или None если ошибки нет
        """
        try:
            error_elem = self.page.locator(LoginLocators.ERROR_MESSAGE)
            error_elem.wait_for(state="visible", timeout=5000)
            return error_elem.text_content()
        except:
            return None

    def get_captcha_error(self) -> Optional[str]:
        """
        Получает сообщение об ошибке reCAPTCHA при регистрации.

        Returns:
            str или None: Текст ошибки reCAPTCHA или None если ошибки нет
        """
        try:
            error_elem = self.page.locator(LoginLocators.CAPTCHA_ERROR)
            error_elem.wait_for(state="visible", timeout=7000)
            return error_elem.text_content()
        except:
            return None

    def get_logged_in_username(self) -> Optional[str]:
        """
        Получает отображаемое имя авторизованного пользователя.

        Returns:
            str или None: Имя пользователя или None если не авторизован
        """
        if self.page.is_visible(LoginLocators.USER_DISPLAY):
            return self.page.text_content(LoginLocators.USER_DISPLAY)
        return None

    def is_field_invalid(self, field_locator: str) -> bool:
        """
        Проверяет, имеет ли поле класс валидационной ошибки.

        Args:
            field_locator: CSS селектор поля с классом ошибки

        Returns:
            bool: True если поле имеет ошибку валидации
        """
        return self.page.is_visible(field_locator)
