"""
Page Object для страницы Alerts.
Содержит методы для работы с различными типами JavaScript alert диалогов.
"""

from playwright.sync_api import Page
from locators.alerts.alerts_locators import AlertsLocators
from pages.base_page import BasePage


class AlertsPage(BasePage):
    """
    Страница тестирования различных типов alert диалогов.
    Поддерживает простые alert, confirm и prompt диалоги.
    """

    def __init__(self, page: Page):
        """
        Инициализация страницы Alerts.

        Args:
            page: Экземпляр страницы Playwright
        """
        super().__init__(page)

    def click_alert_button(self) -> None:
        """
        Кликает кнопку для вызова простого alert диалога.
        Postconditions: появляется alert с сообщением для подтверждения.
        """
        self.log_step("Кликаем кнопку для вызова Alert")
        self.safe_click(AlertsLocators.ALERT_BUTTON)

    def click_timer_alert_button(self) -> None:
        """
        Кликает кнопку для вызова alert с задержкой в 5 секунд.
        Postconditions: через 5 секунд появляется alert диалог.
        """
        self.log_step("Кликаем кнопку для вызова Timer Alert")
        self.safe_click(AlertsLocators.TIMER_ALERT_BUTTON)

    def click_confirm_button(self) -> None:
        """
        Кликает кнопку для вызова confirm диалога.
        Postconditions: появляется confirm диалог с кнопками OK/Cancel.
        """
        self.log_step("Кликаем кнопку для вызова Confirm")
        self.safe_click(AlertsLocators.CONFIRM_BUTTON)

    def click_prompt_button(self) -> None:
        """
        Кликает кнопку для вызова prompt диалога.
        Postconditions: появляется prompt диалог с полем для ввода текста.
        """
        self.log_step("Кликаем кнопку для вызова Prompt")
        self.safe_click(AlertsLocators.PROMPT_BUTTON)

    def handle_alert(self, accept: bool = True) -> None:
        """
        Обрабатывает простой alert диалог.

        Args:
            accept: True для подтверждения (OK), False не применимо для alert

        Postconditions: alert диалог закрыт
        """
        self.log_step(f"Обрабатываем alert: accept={accept}")

        def alert_handler(dialog):
            if accept:
                dialog.accept()
            else:
                dialog.accept()  # Alert можно только подтвердить

        self.page.on("dialog", alert_handler)

    def handle_confirm(self, accept: bool = True) -> None:
        """
        Обрабатывает confirm диалог.

        Args:
            accept: True для OK, False для Cancel

        Postconditions: confirm диалог закрыт, результат отображен на странице
        """
        self.log_step(f"Обрабатываем confirm: accept={accept}")

        def confirm_handler(dialog):
            if accept:
                dialog.accept()
            else:
                dialog.dismiss()

        self.page.on("dialog", confirm_handler)

    def handle_prompt(self, text: str = "", accept: bool = True) -> None:
        """
        Обрабатывает prompt диалог.

        Args:
            text: Текст для ввода в prompt (по умолчанию пустой)
            accept: True для OK, False для Cancel

        Postconditions: prompt диалог закрыт, результат отображен на странице
        """
        self.log_step(f"Обрабатываем prompt с текстом: '{text}', accept={accept}")

        def prompt_handler(dialog):
            if accept:
                dialog.accept(text)
            else:
                dialog.dismiss()

        self.page.on("dialog", prompt_handler)

    def get_confirm_result(self) -> str:
        """
        Получает результат обработки confirm диалога.

        Returns:
            str: Сообщение о результате (OK или Cancel)
        """
        return self.get_text_safe(AlertsLocators.CONFIRM_RESULT) or ""

    def get_prompt_result(self) -> str:
        """
        Получает результат обработки prompt диалога.

        Returns:
            str: Сообщение с введенным текстом или результатом отмены
        """
        return self.get_text_safe(AlertsLocators.PROMPT_RESULT) or ""

    def wait_for_timer_alert(self, timeout: int = 6000) -> bool:
        """
        Ожидает появления timer alert диалога.

        Args:
            timeout: Максимальное время ожидания в миллисекундах

        Returns:
            bool: True если alert появился в указанное время
        """
        self.log_step("Ожидаем появления timer alert")
        try:
            with self.page.expect_event("dialog", timeout=timeout):
                pass
            return True
        except Exception:
            return False
