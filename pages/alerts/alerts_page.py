"""
Page Object для страницы Alerts с JavaScript диалогами.
Переписан для корректной работы с Playwright dialog handling.
"""

import allure
from playwright.sync_api import Page
from locators.alerts.alerts_locators import AlertsLocators
from pages.base_page import BasePage


class AlertsPage(BasePage):
    """
    Страница тестирования JavaScript alert диалогов.
    Использует корректную обработку диалогов через Playwright.
    """

    def __init__(self, page: Page):
        """
        Инициализация страницы Alerts.

        Args:
            page: Экземпляр страницы Playwright
        """
        super().__init__(page)

    @allure.step("Обрабатываем простой alert и получаем его текст")
    def handle_simple_alert(self) -> str:
        """
        Обрабатывает простой alert диалог.

        Returns:
            str: Текст alert диалога
        """
        dialog_text = ""

        def handle_dialog(dialog):
            nonlocal dialog_text
            dialog_text = dialog.message
            dialog.accept()

        # Устанавливаем обработчик перед кликом
        self.page.on("dialog", handle_dialog)

        try:
            self.safe_click(AlertsLocators.ALERT_BUTTON)
            self.page.wait_for_timeout(1000)  # Ждем обработки
        finally:
            # Удаляем обработчик
            self.page.remove_listener("dialog", handle_dialog)

        return dialog_text

    @allure.step("Обрабатываем timer alert и получаем его текст")
    def handle_timer_alert(self, timeout: int = 7000) -> str:
        """
        Обрабатывает alert с задержкой.

        Args:
            timeout: Максимальное время ожидания alert (мс)

        Returns:
            str: Текст alert диалога
        """
        dialog_text = ""
        dialog_handled = False

        def handle_dialog(dialog):
            nonlocal dialog_text, dialog_handled
            dialog_text = dialog.message
            dialog_handled = True
            dialog.accept()

        # Устанавливаем обработчик перед кликом
        self.page.on("dialog", handle_dialog)

        try:
            self.safe_click(AlertsLocators.TIMER_ALERT_BUTTON)
            self.page.wait_for_timeout(timeout)  # Ждем появления alert
        finally:
            # Удаляем обработчик
            self.page.remove_listener("dialog", handle_dialog)

        return dialog_text if dialog_handled else ""

    @allure.step("Принимаем confirm dialog")
    def accept_confirm_dialog(self) -> str:
        """
        Принимает confirm диалог (нажимает OK).

        Returns:
            str: Текст результата или пустая строка
        """
        def handle_dialog(dialog):
            dialog.accept()

        # Устанавливаем обработчик перед кликом
        self.page.on("dialog", handle_dialog)

        try:
            self.safe_click(AlertsLocators.CONFIRM_BUTTON)
            self.page.wait_for_timeout(1000)
        finally:
            # Удаляем обработчик
            self.page.remove_listener("dialog", handle_dialog)

        # Пытаемся получить результат
        return self.get_text_safe(AlertsLocators.CONFIRM_RESULT) or ""

    @allure.step("Отклоняем confirm dialog")
    def dismiss_confirm_dialog(self) -> str:
        """
        Отклоняет confirm диалог (нажимает Cancel).

        Returns:
            str: Текст результата или пустая строка
        """
        def handle_dialog(dialog):
            dialog.dismiss()

        # Устанавливаем обработчик перед кликом
        self.page.on("dialog", handle_dialog)

        try:
            self.safe_click(AlertsLocators.CONFIRM_BUTTON)
            self.page.wait_for_timeout(1000)
        finally:
            # Удаляем обработчик
            self.page.remove_listener("dialog", handle_dialog)

        # Пытаемся получить результат
        return self.get_text_safe(AlertsLocators.CONFIRM_RESULT) or ""

    @allure.step("Вводим текст в prompt dialog")
    def handle_prompt_with_text(self, text: str) -> str:
        """
        Обрабатывает prompt диалог с вводом текста.

        Args:
            text: Текст для ввода

        Returns:
            str: Результат prompt диалога или пустая строка
        """
        def handle_dialog(dialog):
            dialog.accept(text)

        # Устанавливаем обработчик перед кликом
        self.page.on("dialog", handle_dialog)

        try:
            self.safe_click(AlertsLocators.PROMPT_BUTTON)
            self.page.wait_for_timeout(1000)
        finally:
            # Удаляем обработчик
            self.page.remove_listener("dialog", handle_dialog)

        # Пытаемся получить результат
        return self.get_text_safe(AlertsLocators.PROMPT_RESULT) or ""

    @allure.step("Отклоняем prompt dialog")
    def dismiss_prompt_dialog(self) -> str:
        """
        Отклоняет prompt диалог.

        Returns:
            str: Результат prompt диалога или пустая строка
        """
        def handle_dialog(dialog):
            dialog.dismiss()

        # Устанавливаем обработчик перед кликом
        self.page.on("dialog", handle_dialog)

        try:
            self.safe_click(AlertsLocators.PROMPT_BUTTON)
            self.page.wait_for_timeout(1000)
        finally:
            # Удаляем обработчик
            self.page.remove_listener("dialog", handle_dialog)

        # Пытаемся получить результат
        return self.get_text_safe(AlertsLocators.PROMPT_RESULT) or ""

    def check_all_buttons_visible(self) -> bool:
        """
        Проверяет видимость всех кнопок alert на странице.

        Returns:
            bool: True если все кнопки видны
        """
        buttons = [
            AlertsLocators.ALERT_BUTTON,
            AlertsLocators.TIMER_ALERT_BUTTON,
            AlertsLocators.CONFIRM_BUTTON,
            AlertsLocators.PROMPT_BUTTON
        ]

        try:
            for button in buttons:
                if not self.page.locator(button).is_visible():
                    return False
            return True
        except Exception:
            return False

    def check_element_exists(self, selector: str) -> bool:
        """
        Проверяет существование элемента в DOM.

        Args:
            selector: CSS селектор элемента

        Returns:
            bool: True если элемент существует
        """
        try:
            return self.page.locator(selector).count() > 0
        except Exception:
            return False

    def get_confirm_result_safe(self) -> str:
        """Безопасно получает результат confirm."""
        try:
            element = self.page.locator(AlertsLocators.CONFIRM_RESULT)
            element.wait_for(state="visible", timeout=2000)
            return element.inner_text()
        except Exception:
            return ""

    def get_prompt_result_safe(self) -> str:
        """Безопасно получает результат prompt."""
        try:
            element = self.page.locator(AlertsLocators.PROMPT_RESULT)
            element.wait_for(state="visible", timeout=2000)
            return element.inner_text()
        except Exception:
            return ""
