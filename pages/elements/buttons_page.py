"""
Page Object для страницы Buttons с различными типами кликов.
Содержит методы для двойного клика, правого клика и обычного клика.
"""

from playwright.sync_api import Page
from locators.elements.buttons_locators import ButtonsLocators
from pages.base_page import BasePage


class ButtonsPage(BasePage):
    """
    Страница тестирования различных типов кликов по кнопкам.
    Наследует от BasePage общие методы взаимодействия с элементами.
    """

    def __init__(self, page: Page):
        """
        Инициализация страницы кнопок.

        Args:
            page: Экземпляр страницы Playwright
        """
        super().__init__(page)

    def double_click_button(self) -> None:
        """
        Выполняет двойной клик по специальной кнопке.
        Postconditions: появляется сообщение о двойном клике.
        """
        self.log_step("Выполняем двойной клик по кнопке")
        self.page.dblclick(ButtonsLocators.DOUBLE_CLICK_BUTTON)

    def right_click_button(self) -> None:
        """
        Выполняет клик правой кнопкой мыши.
        Postconditions: появляется сообщение о правом клике.
        """
        self.log_step("Выполняем правый клик по кнопке")
        self.page.click(ButtonsLocators.RIGHT_CLICK_BUTTON, button="right")

    def click_me_button(self) -> None:
        """
        Выполняет обычный левый клик по динамической кнопке.
        Postconditions: появляется сообщение об обычном клике.
        """
        self.log_step("Выполняем обычный клик по кнопке Click Me")
        # Используем nth(2) так как это третья кнопка на странице
        button = self.page.locator("button.btn.btn-primary").nth(2)
        button.click()

    def get_double_click_message(self) -> str:
        """
        Получает сообщение, появившееся после двойного клика.

        Returns:
            str: Текст сообщения о двойном клике
        """
        return self.get_text_safe(ButtonsLocators.DOUBLE_CLICK_MESSAGE)

    def get_right_click_message(self) -> str:
        """
        Получает сообщение, появившееся после правого клика.

        Returns:
            str: Текст сообщения о правом клике
        """
        return self.get_text_safe(ButtonsLocators.RIGHT_CLICK_MESSAGE)

    def get_click_me_message(self) -> str:
        """
        Получает сообщение, появившееся после обычного клика.

        Returns:
            str: Текст сообщения об обычном клике
        """
        return self.get_text_safe(ButtonsLocators.CLICK_ME_MESSAGE)
