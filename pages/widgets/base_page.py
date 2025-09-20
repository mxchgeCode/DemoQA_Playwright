"""
Базовый Page Object для виджетов с общими утилитами.
Расширяет функциональность основного BasePage специфичными для виджетов методами.
"""

import time
import logging
from playwright.sync_api import Page
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class WidgetBasePage(BasePage):
    """
    Базовый класс для всех Page Object виджетов.
    Содержит общие методы для работы с интерактивными элементами виджетов.
    """

    def __init__(self, page: Page):
        """
        Инициализация базовой страницы виджетов.

        Args:
            page: Экземпляр страницы Playwright
        """
        super().__init__(page)

    def wait_for_animation_complete(self, timeout: int = 2000) -> None:
        """
        Ожидает завершения CSS анимаций на странице.

        Args:
            timeout: Максимальное время ожидания в миллисекундах
        """
        self.log_step("Ожидаем завершения анимаций")
        # Ждем стабилизации анимаций
        self.page.wait_for_timeout(timeout)

    def click_and_wait_for_response(self, selector: str, wait_time: int = 1000) -> None:
        """
        Кликает по элементу и ждет отклик интерфейса.

        Args:
            selector: CSS селектор элемента
            wait_time: Время ожидания отклика в миллисекундах
        """
        self.log_step(f"Кликаем по элементу и ждем отклик: {selector}")
        self.safe_click(selector)
        self.page.wait_for_timeout(wait_time)

    def hover_and_wait(self, selector: str, wait_time: int = 500) -> None:
        """
        Наводит курсор на элемент и ждет появления эффекта.

        Args:
            selector: CSS селектор элемента
            wait_time: Время ожидания эффекта в миллисекундах
        """
        self.log_step(f"Наводим курсор на элемент: {selector}")
        self.page.hover(selector)
        self.page.wait_for_timeout(wait_time)

    def wait_for_dropdown_to_appear(
        self, dropdown_selector: str, timeout: int = 5000
    ) -> bool:
        """
        Ожидает появления выпадающего меню.

        Args:
            dropdown_selector: CSS селектор выпадающего меню
            timeout: Максимальное время ожидания в миллисекундах

        Returns:
            bool: True если dropdown появился
        """
        try:
            self.page.wait_for_selector(
                dropdown_selector, state="visible", timeout=timeout
            )
            return True
        except:
            return False

    def select_dropdown_option(self, dropdown_selector: str, option_text: str) -> bool:
        """
        Выбирает опцию из выпадающего меню по тексту.

        Args:
            dropdown_selector: CSS селектор dropdown контейнера
            option_text: Текст опции для выбора

        Returns:
            bool: True если опция была выбрана
        """
        self.log_step(f"Выбираем опцию в dropdown: {option_text}")
        try:
            option = self.page.locator(f"{dropdown_selector} >> text={option_text}")
            if option.is_visible():
                option.click()
                return True
        except:
            pass
        return False

    def wait_for_widget_state_change(
        self, element_selector: str, expected_class: str, timeout: int = 5000
    ) -> bool:
        """
        Ожидает изменения состояния виджета по CSS классу.

        Args:
            element_selector: CSS селектор элемента
            expected_class: Ожидаемый CSS класс
            timeout: Максимальное время ожидания в миллисекундах

        Returns:
            bool: True если состояние изменилось
        """
        self.log_step(f"Ожидаем изменения состояния виджета: {expected_class}")
        start_time = time.time()

        while time.time() - start_time < timeout / 1000:
            current_class = self.page.get_attribute(element_selector, "class") or ""
            if expected_class in current_class:
                return True
            time.sleep(0.1)

        return False

    def get_widget_attribute(self, selector: str, attribute: str) -> str:
        """
        Безопасно получает атрибут виджета.

        Args:
            selector: CSS селектор элемента
            attribute: Название атрибута

        Returns:
            str: Значение атрибута или пустая строка
        """
        try:
            return self.page.get_attribute(selector, attribute) or ""
        except:
            return ""

    def scroll_into_view(self, selector: str) -> None:
        """
        Прокручивает страницу до видимости элемента.

        Args:
            selector: CSS селектор элемента
        """
        self.log_step(f"Прокручиваем до элемента: {selector}")
        self.page.locator(selector).scroll_into_view_if_needed()

    def wait_for_tooltip(
        self, tooltip_selector: str = ".tooltip", timeout: int = 3000
    ) -> bool:
        """
        Ожидает появления tooltip подсказки.

        Args:
            tooltip_selector: CSS селектор tooltip
            timeout: Максимальное время ожидания в миллисекундах

        Returns:
            bool: True если tooltip появился
        """
        self.log_step("Ожидаем появления tooltip")
        try:
            self.page.wait_for_selector(
                tooltip_selector, state="visible", timeout=timeout
            )
            return True
        except:
            return False
