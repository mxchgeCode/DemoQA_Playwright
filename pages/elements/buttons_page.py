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
        # Предпочитаем стабильный селектор по тексту, с резервом
        btn = self.page.locator(ButtonsLocators.CLICK_ME_BUTTON_ALT)
        if btn.count() == 0 or not btn.first.is_visible():
            btn = self.page.locator(ButtonsLocators.CLICK_ME_BUTTON)
        btn.first.click()

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

    # ===== Доп. API, ожидаемое тестами =====

    # Сообщение для обычного клика с именем, ожидаемым тестом
    def get_click_message(self) -> str:
        return self.get_click_me_message()

    # Видимость кнопок
    def is_double_click_button_visible(self) -> bool:
        return self.page.locator(ButtonsLocators.DOUBLE_CLICK_BUTTON).is_visible()

    def is_right_click_button_visible(self) -> bool:
        return self.page.locator(ButtonsLocators.RIGHT_CLICK_BUTTON).is_visible()

    def is_click_me_button_visible(self) -> bool:
        # Считаем видимой, если хотя бы один из селекторов доступен
        return (
            self.page.locator(ButtonsLocators.CLICK_ME_BUTTON_ALT).is_visible()
            or self.page.locator(ButtonsLocators.CLICK_ME_BUTTON).is_visible()
        )

    # Доступность (enabled) кнопок
    def is_double_click_button_enabled(self) -> bool:
        return self.page.locator(ButtonsLocators.DOUBLE_CLICK_BUTTON).is_enabled()

    def is_right_click_button_enabled(self) -> bool:
        return self.page.locator(ButtonsLocators.RIGHT_CLICK_BUTTON).is_enabled()

    def is_click_me_button_enabled(self, timeout: int = 5000) -> bool:
        try:
            # Пробуем альтернативные селекторы
            selectors = [
                ButtonsLocators.CLICK_ME_BUTTON_ALT,
                ButtonsLocators.CLICK_ME_BUTTON,
                ButtonsLocators.ALL_BUTTONS + ":nth-child(3)"
            ]

            for selector in selectors:
                try:
                    locator = self.page.locator(selector)
                    if locator.count() > 0:
                        return locator.is_enabled(timeout=timeout)
                except:
                    continue

            return False
        except Exception:
            return False

    # Тексты на кнопках
    def get_double_click_button_text(self) -> str:
        return self.page.locator(ButtonsLocators.DOUBLE_CLICK_BUTTON).inner_text()

    def get_right_click_button_text(self) -> str:
        return self.page.locator(ButtonsLocators.RIGHT_CLICK_BUTTON).inner_text()

    def get_click_me_button_text(self) -> str:
        locator = self.page.locator(ButtonsLocators.CLICK_ME_BUTTON_ALT)
        if not locator.is_visible():
            locator = self.page.locator(ButtonsLocators.CLICK_ME_BUTTON)
        return locator.inner_text()
