"""
Page Object для страницы Tool Tips.
Содержит методы для работы с всплывающими подсказками (tooltips).
"""

import time
from playwright.sync_api import Page
from locators.widgets.tooltips_locators import TooltipsLocators
from pages.widgets.base_page import WidgetBasePage


class ToolTipsPage(WidgetBasePage):
    """
    Страница тестирования всплывающих подсказок.
    Поддерживает hover tooltip для кнопок, полей ввода и ссылок.
    """

    def __init__(self, page: Page):
        """
        Инициализация страницы Tool Tips.

        Args:
            page: Экземпляр страницы Playwright
        """
        super().__init__(page)

    def hover_button(self) -> None:
        """
        Наводит курсор на кнопку для появления tooltip.
        Postconditions: появляется tooltip с текстом для кнопки.
        """
        self.log_step("Наводим курсор на кнопку")
        self.hover_and_wait(TooltipsLocators.HOVER_BUTTON)

    def hover_text_field(self) -> None:
        """
        Наводит курсор на текстовое поле для появления tooltip.
        Postconditions: появляется tooltip с текстом для поля ввода.
        """
        self.log_step("Наводим курсор на текстовое поле")
        self.hover_and_wait(TooltipsLocators.TEXT_FIELD)

    def hover_contrary_link(self) -> None:
        """
        Наводит курсор на ссылку "Contrary" для появления tooltip.
        Postconditions: появляется tooltip с текстом для ссылки.
        """
        self.log_step("Наводим курсор на ссылку Contrary")
        self.hover_and_wait(TooltipsLocators.CONTRARY_LINK)

    def hover_section_link(self) -> None:
        """
        Наводит курсор на ссылку "1.10.32" для появления tooltip.
        Postconditions: появляется tooltip с текстом для ссылки раздела.
        """
        self.log_step("Наводим курсор на ссылку раздела")
        self.hover_and_wait(TooltipsLocators.SECTION_LINK)

    def get_tooltip_text(self) -> str:
        """
        Получает текст видимого tooltip.

        Returns:
            str: Текст tooltip или пустая строка если tooltip не виден
        """
        tooltip_selectors = [
            ".tooltip-inner",
            ".tooltip .tooltip-inner",
            "[role='tooltip']",
            ".react-tooltip",
        ]

        for selector in tooltip_selectors:
            tooltip = self.page.locator(selector)
            if tooltip.is_visible():
                return tooltip.inner_text().strip()

        return ""

    def is_tooltip_visible(self) -> bool:
        """
        Проверяет видимость tooltip.

        Returns:
            bool: True если tooltip виден на странице
        """
        return self.wait_for_tooltip(timeout=3000)

    def wait_for_tooltip_to_appear(self, timeout: int = 5000) -> bool:
        """
        Ожидает появления tooltip.

        Args:
            timeout: Максимальное время ожидания в миллисекундах

        Returns:
            bool: True если tooltip появился в указанное время
        """
        return self.wait_for_tooltip(timeout=timeout)

    def hover_and_get_tooltip(self, element_selector: str) -> str:
        """
        Наводит курсор на элемент и получает текст tooltip.

        Args:
            element_selector: CSS селектор элемента для наведения

        Returns:
            str: Текст tooltip или пустая строка

        Postconditions: курсор наведен на элемент, tooltip виден
        """
        self.log_step(f"Наводим курсор и получаем tooltip для: {element_selector}")

        self.page.hover(element_selector)

        # Ждем появления tooltip
        if self.wait_for_tooltip_to_appear(3000):
            time.sleep(500)  # Дополнительная задержка для стабилизации
            return self.get_tooltip_text()
        else:
            return ""

    def get_button_tooltip(self) -> str:
        """
        Получает tooltip кнопки.

        Returns:
            str: Текст tooltip кнопки
        """
        return self.hover_and_get_tooltip(TooltipsLocators.HOVER_BUTTON)

    def get_text_field_tooltip(self) -> str:
        """
        Получает tooltip текстового поля.

        Returns:
            str: Текст tooltip поля ввода
        """
        return self.hover_and_get_tooltip(TooltipsLocators.TEXT_FIELD)

    def get_contrary_link_tooltip(self) -> str:
        """
        Получает tooltip ссылки "Contrary".

        Returns:
            str: Текст tooltip ссылки Contrary
        """
        return self.hover_and_get_tooltip(TooltipsLocators.CONTRARY_LINK)

    def get_section_link_tooltip(self) -> str:
        """
        Получает tooltip ссылки раздела.

        Returns:
            str: Текст tooltip ссылки раздела
        """
        return self.hover_and_get_tooltip(TooltipsLocators.SECTION_LINK)

    def move_away_from_elements(self) -> None:
        """
        Убирает курсор от всех элементов для скрытия tooltip.
        Postconditions: все tooltip скрыты.
        """
        self.log_step("Убираем курсор от элементов")
        # Перемещаем курсор в нейтральную область
        self.page.mouse.move(50, 50)
        time.sleep(500)

    def verify_tooltip_positioning(self, element_selector: str) -> dict:
        """
        Проверяет позиционирование tooltip относительно элемента.

        Args:
            element_selector: CSS селектор элемента с tooltip

        Returns:
            dict: Словарь с информацией о позиции tooltip

        Example:
            {
                'tooltip_visible': True,
                'tooltip_position': 'top',
                'element_bounds': {...},
                'tooltip_bounds': {...}
            }
        """
        self.log_step(f"Проверяем позиционирование tooltip для: {element_selector}")

        result = {
            "tooltip_visible": False,
            "tooltip_position": "unknown",
            "element_bounds": None,
            "tooltip_bounds": None,
        }

        # Наводим курсор на элемент
        self.page.hover(element_selector)

        if self.wait_for_tooltip_to_appear(3000):
            result["tooltip_visible"] = True

            # Получаем границы элемента
            element = self.page.locator(element_selector)
            result["element_bounds"] = element.bounding_box()

            # Пытаемся найти tooltip и получить его границы
            tooltip_selectors = [".tooltip-inner", "[role='tooltip']", ".react-tooltip"]

            for selector in tooltip_selectors:
                tooltip = self.page.locator(selector)
                if tooltip.is_visible():
                    result["tooltip_bounds"] = tooltip.bounding_box()

                    # Определяем позицию tooltip относительно элемента
                    if result["element_bounds"] and result["tooltip_bounds"]:
                        element_y = result["element_bounds"]["y"]
                        tooltip_y = result["tooltip_bounds"]["y"]

                        if tooltip_y < element_y:
                            result["tooltip_position"] = "top"
                        elif tooltip_y > element_y:
                            result["tooltip_position"] = "bottom"
                        else:
                            result["tooltip_position"] = "side"
                    break

        return result

    def test_all_tooltips(self) -> dict:
        """
        Тестирует все tooltip на странице и собирает их тексты.

        Returns:
            dict: Словарь с текстами всех tooltip

        Example:
            {
                'button': 'You hovered over the Button',
                'text_field': 'You hovered over the text field',
                'contrary_link': 'You hovered over the Contrary',
                'section_link': 'You hovered over the 1.10.32'
            }
        """
        tooltips = {}

        # Тестируем кнопку
        tooltips["button"] = self.get_button_tooltip()
        self.move_away_from_elements()

        # Тестируем текстовое поле
        tooltips["text_field"] = self.get_text_field_tooltip()
        self.move_away_from_elements()

        # Тестируем ссылку Contrary
        tooltips["contrary_link"] = self.get_contrary_link_tooltip()
        self.move_away_from_elements()

        # Тестируем ссылку раздела
        tooltips["section_link"] = self.get_section_link_tooltip()
        self.move_away_from_elements()

        return tooltips
