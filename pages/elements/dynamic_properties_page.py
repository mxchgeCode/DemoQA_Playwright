"""
Page Object для страницы Dynamic Properties.
Содержит методы для работы с элементами, изменяющими свои свойства во времени.
"""

from playwright.sync_api import Page

from data import Colors
from locators.elements.dynamic_locators import DynamicPropertiesLocators
from pages.base_page import BasePage


class DynamicPropertiesPage(BasePage):
    """
    Страница тестирования динамических свойств элементов.
    Элементы изменяют состояние (активность, видимость, цвет) через определенное время.
    """

    def __init__(self, page: Page):
        """
        Инициализация страницы динамических свойств.

        Args:
            page: Экземпляр страницы Playwright
        """
        super().__init__(page)

    def is_enable_after_enabled(self) -> bool:
        """
        Проверяет, активна ли кнопка "Enable After".

        Returns:
            bool: True если кнопка активна (не disabled)
        """
        return self.page.locator(
            DynamicPropertiesLocators.ENABLE_AFTER_BUTTON
        ).is_enabled()

    def wait_and_check_enable_after(self, timeout: int = 10000) -> bool:
        """
        Ожидает активации кнопки "Enable After" и проверяет её состояние.

        Args:
            timeout: Максимальное время ожидания в миллисекундах

        Returns:
            bool: True если кнопка стала активной в указанное время
        """
        self.log_step("Ожидаем активации кнопки Enable After")
        self.page.wait_for_function(
            "element => !element.disabled",
            arg=self.page.locator(
                DynamicPropertiesLocators.ENABLE_AFTER_BUTTON
            ).element_handle(),
            timeout=timeout,
        )
        return self.is_enable_after_enabled()

    def is_visible_after_visible(self, timeout: int = 10000) -> bool:
        """
        Проверяет видимость кнопки "Visible After" с ожиданием.

        Args:
            timeout: Максимальное время ожидания появления элемента

        Returns:
            bool: True если кнопка стала видимой
        """
        self.log_step("Проверяем видимость кнопки Visible After")
        try:
            self.page.wait_for_selector(
                DynamicPropertiesLocators.VISIBLE_AFTER_BUTTON, timeout=timeout
            )
            return self.page.locator(
                DynamicPropertiesLocators.VISIBLE_AFTER_BUTTON
            ).is_visible()
        except:
            return False

    def wait_for_text_color_change(
        self,
        expected_hex_color: str = Colors.RED,
        timeout: int = 10000,
        poll_interval: int = 200,
    ) -> bool:
        """
        Ожидает изменения цвета текста кнопки на ожидаемый.

        Args:
            expected_hex_color: Ожидаемый HEX цвет (по умолчанию красный)
            timeout: Максимальное время ожидания в миллисекундах
            poll_interval: Интервал между проверками в миллисекундах

        Returns:
            bool: True если цвет изменился на ожидаемый
        """
        self.log_step(f"Ожидаем изменения цвета текста на {expected_hex_color}")
        locator = self.page.locator(DynamicPropertiesLocators.COLOR_CHANGE_BUTTON)
        elapsed = 0

        while elapsed < timeout:
            try:
                current_rgb = locator.evaluate(
                    "el => window.getComputedStyle(el).color"
                )
                # Конвертируем RGB в HEX
                parts = current_rgb.strip()[4:-1].split(",")
                r, g, b = [int(p.strip()) for p in parts]
                current_hex = f"#{r:02x}{g:02x}{b:02x}"

                if current_hex.lower() == expected_hex_color.lower():
                    return True
            except Exception as e:
                self.log_step(f"Ошибка при проверке цвета: {e}")

            self.page.wait_for_timeout(poll_interval)
            elapsed += poll_interval

        return False

    def click_enable_after_button(self) -> None:
        """
        Кликает по кнопке "Enable After" если она активна.

        Preconditions: кнопка должна быть активной
        """
        if self.is_enable_after_enabled():
            self.log_step("Кликаем по активной кнопке Enable After")
            self.safe_click(DynamicPropertiesLocators.ENABLE_AFTER_BUTTON)
        else:
            raise Exception("Кнопка Enable After не активна")

    def click_visible_after_button(self) -> None:
        """
        Кликает по кнопке "Visible After" если она видима.

        Preconditions: кнопка должна быть видимой
        """
        if self.is_visible_after_visible():
            self.log_step("Кликаем по видимой кнопке Visible After")
            self.safe_click(DynamicPropertiesLocators.VISIBLE_AFTER_BUTTON)
        else:
            raise Exception("Кнопка Visible After не видима")

    def click_color_change_button(self) -> None:
        """
        Кликает по кнопке с изменяющимся цветом.
        """
        self.log_step("Кликаем по кнопке Color Change")
        self.safe_click(DynamicPropertiesLocators.COLOR_CHANGE_BUTTON)

    def get_current_text_color(self) -> str:
        """
        Получает текущий цвет текста кнопки Color Change в HEX формате.

        Returns:
            str: Цвет в HEX формате (например, "#000000")
        """
        locator = self.page.locator(DynamicPropertiesLocators.COLOR_CHANGE_BUTTON)
        current_rgb = locator.evaluate("el => window.getComputedStyle(el).color")
        parts = current_rgb.strip()[4:-1].split(",")
        r, g, b = [int(p.strip()) for p in parts]
        return f"#{r:02x}{g:02x}{b:02x}"
