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

    def click_enable_after_button(self) -> bool:
        """
        Кликает по кнопке "Enable After" если она активна.
    
        Returns:
            bool: True если клик выполнен, False если кнопка не активна
        """
        if self.is_enable_after_enabled():
            self.log_step("Кликаем по активной кнопке Enable After")
            self.safe_click(DynamicPropertiesLocators.ENABLE_AFTER_BUTTON)
            return True
        return False

    def click_visible_after_button(self) -> bool:
        """
        Кликает по кнопке "Visible After" если она видима.
    
        Returns:
            bool: True если клик выполнен, False если кнопка не видима
        """
        if self.is_visible_after_visible():
            self.log_step("Кликаем по видимой кнопке Visible After")
            self.safe_click(DynamicPropertiesLocators.VISIBLE_AFTER_BUTTON)
            return True
        return False

    def click_color_change_button(self) -> bool:
        """
        Кликает по кнопке с изменяющимся цветом.
    
        Returns:
            bool: True если клик выполнен
        """
        self.log_step("Кликаем по кнопке Color Change")
        self.safe_click(DynamicPropertiesLocators.COLOR_CHANGE_BUTTON)
        return True

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

    # ======== Совместимость с ожидаемым API тестов (алиасы/вспомогательные) ========
    def is_enable_after_button_enabled(self) -> bool:
        return self.is_enable_after_enabled()

    def get_enable_after_button_attributes(self) -> dict:
        loc = self.page.locator(DynamicPropertiesLocators.ENABLE_AFTER_BUTTON)
        return {
            "id": loc.get_attribute("id") or "",
            "disabled": (not loc.is_enabled()),
            "class": loc.get_attribute("class") or "",
        }

    def wait_for_enable_after_button(self, timeout: int = 10000) -> bool:
        return self.wait_and_check_enable_after(timeout=timeout)

    def get_color_change_button_color(self) -> str:
        loc = self.page.locator(DynamicPropertiesLocators.COLOR_CHANGE_BUTTON)
        return loc.evaluate("el => window.getComputedStyle(el).color")

    def get_color_change_button_classes(self) -> str:
        return self.page.locator(DynamicPropertiesLocators.COLOR_CHANGE_BUTTON).get_attribute("class") or ""

    def wait_for_color_change(self, timeout: int = 10000, poll_interval: int = 200) -> bool:
        loc = self.page.locator(DynamicPropertiesLocators.COLOR_CHANGE_BUTTON)
        try:
            initial_color = loc.evaluate("el => window.getComputedStyle(el).color")
        except Exception:
            initial_color = ""
        initial_class = loc.get_attribute("class") or ""
        elapsed = 0
        while elapsed < timeout:
            try:
                curr_color = loc.evaluate("el => window.getComputedStyle(el).color")
                curr_class = loc.get_attribute("class") or ""
                if curr_color != initial_color or curr_class != initial_class:
                    return True
            except Exception:
                pass
            self.page.wait_for_timeout(poll_interval)
            elapsed += poll_interval
        return False

    def is_visible_after_button_visible(self) -> bool:
        return self.page.locator(DynamicPropertiesLocators.VISIBLE_AFTER_BUTTON).is_visible()

    def is_visible_after_button_in_dom(self) -> bool:
        return self.page.locator(DynamicPropertiesLocators.VISIBLE_AFTER_BUTTON).count() > 0

    def wait_for_visible_after_button(self, timeout: int = 10000) -> bool:
        return self.is_visible_after_visible(timeout=timeout)

    def find_random_id_element(self):
        loc = self.page.locator("[id^='random']")
        return bool(loc.count() > 0)

    def get_random_id_element_info(self) -> dict:
        loc = self.page.locator("[id^='random']").first
        if loc.count() == 0:
            return {}
        tag = loc.evaluate("el => el.tagName") or ""
        return {
            "id": loc.get_attribute("id") or "",
            "tag": str(tag).lower(),
            "text": (loc.inner_text() or "").strip(),
        }

    def get_random_id_element_id(self) -> str:
        loc = self.page.locator("[id^='random']").first
        return loc.get_attribute("id") or ""

    def get_current_timestamp(self) -> int:
        """
        Возвращает текущую метку времени в миллисекундах.
        Используется тестами для измерения длительности операций.
        """
        import time
        return int(time.time() * 1000)
