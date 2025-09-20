"""
Page Object для страницы Browser Windows.
Содержит методы для открытия новых вкладок и окон браузера.
"""

from playwright.sync_api import Page
from locators.alerts.browser_windows_locators import BrowserWindowsLocators
from pages.base_page import BasePage


class BrowserWindowsPage(BasePage):
    """
    Страница тестирования открытия новых вкладок и окон браузера.
    Поддерживает открытие обычных вкладок, окон и окон с сообщениями.
    """

    def __init__(self, page: Page):
        """
        Инициализация страницы Browser Windows.

        Args:
            page: Экземпляр страницы Playwright
        """
        super().__init__(page)

    def click_new_tab(self) -> None:
        """
        Кликает по кнопке для открытия новой вкладки.
        Postconditions: открывается новая вкладка в том же окне браузера.
        """
        self.log_step("Кликаем по кнопке New Tab")
        self.safe_click(BrowserWindowsLocators.NEW_TAB_BUTTON)

    def click_new_window(self) -> None:
        """
        Кликает по кнопке для открытия нового окна.
        Postconditions: открывается новое окно браузера.
        """
        self.log_step("Кликаем по кнопке New Window")
        self.safe_click(BrowserWindowsLocators.NEW_WINDOW_BUTTON)

    def click_new_window_message(self) -> None:
        """
        Кликает по кнопке для открытия нового окна с сообщением.
        Postconditions: открывается новое окно с предопределенным текстом.
        """
        self.log_step("Кликаем по кнопке New Window Message")
        self.safe_click(BrowserWindowsLocators.NEW_WINDOW_MESSAGE_BUTTON)

    def get_current_window_count(self) -> int:
        """
        Получает количество открытых окон/вкладок в контексте.

        Returns:
            int: Количество страниц в текущем контексте
        """
        return len(self.page.context.pages)

    def wait_for_new_page(self, timeout: int = 5000):
        """
        Ожидает открытия новой страницы и возвращает её.

        Args:
            timeout: Максимальное время ожидания в миллисекундах

        Returns:
            Page: Новая открытая страница
        """
        self.log_step("Ожидаем открытия новой страницы")
        with self.page.context.expect_page(timeout=timeout) as new_page_info:
            pass
        return new_page_info.value
