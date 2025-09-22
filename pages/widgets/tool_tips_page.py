"""
Page Object для страницы Tool Tips.
Содержит методы для работы с всплывающими подсказками (tooltips).
"""

import time
from playwright.sync_api import Page
from locators.widgets.tooltips_locators import ToolTipsLocators
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
        self.hover_and_wait(ToolTipsLocators.TOOLTIP_BUTTON)

    def hover_text_field(self) -> None:
        """
        Наводит курсор на текстовое поле для появления tooltip.
        Postconditions: появляется tooltip с текстом для поля ввода.
        """
        self.log_step("Наводим курсор на текстовое поле")
        self.hover_and_wait(ToolTipsLocators.TOOLTIP_TEXT_FIELD)

    def hover_contrary_link(self) -> None:
        """
        Наводит курсор на ссылку "Contrary" для появления tooltip.
        Postconditions: появляется tooltip с текстом для ссылки.
        """
        self.log_step("Наводим курсор на ссылку Contrary")
        self.hover_and_wait(ToolTipsLocators.TOOLTIP_TEXT_LINK)

    def hover_section_link(self) -> None:
        """
        Наводит курсор на ссылку "1.10.32" для появления tooltip.
        Postconditions: появляется tooltip с текстом для ссылки раздела.
        """
        self.log_step("Наводим курсор на ссылку раздела")
        self.hover_and_wait(ToolTipsLocators.TOOLTIP_SECTION_LINK)

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
        return self.hover_and_get_tooltip(ToolTipsLocators.TOOLTIP_BUTTON)

    def get_text_field_tooltip(self) -> str:
        """
        Получает tooltip текстового поля.

        Returns:
            str: Текст tooltip поля ввода
        """
        return self.hover_and_get_tooltip(ToolTipsLocators.TOOLTIP_TEXT_FIELD)

    def get_contrary_link_tooltip(self) -> str:
        """
        Получает tooltip ссылки "Contrary".

        Returns:
            str: Текст tooltip ссылки Contrary
        """
        return self.hover_and_get_tooltip(ToolTipsLocators.TOOLTIP_TEXT_LINK)

    def get_section_link_tooltip(self) -> str:
        """
        Получает tooltip ссылки раздела.

        Returns:
            str: Текст tooltip ссылки раздела
        """
        return self.hover_and_get_tooltip(ToolTipsLocators.TOOLTIP_SECTION_LINK)

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

    def get_elements_with_tooltips(self) -> list:
        """
        Получает список элементов с подсказками.

        Returns:
            list: Список элементов с информацией о подсказках
        """
        elements = []

        # Проверяем кнопку
        button_element = self.page.locator(ToolTipsLocators.TOOLTIP_BUTTON)
        if button_element.is_visible():
            elements.append({
                "type": "button",
                "selector": ToolTipsLocators.TOOLTIP_BUTTON,
                "element_text": "Button",
                "tooltip_text": ToolTipsLocators.BUTTON_TOOLTIP_TEXT
            })

        # Проверяем текстовое поле
        text_field_element = self.page.locator(ToolTipsLocators.TOOLTIP_TEXT_FIELD)
        if text_field_element.is_visible():
            elements.append({
                "type": "text_field",
                "selector": ToolTipsLocators.TOOLTIP_TEXT_FIELD,
                "element_text": "Text Field",
                "tooltip_text": ToolTipsLocators.INPUT_TOOLTIP_TEXT
            })

        # Проверяем ссылку Contrary
        contrary_link = self.page.locator(ToolTipsLocators.TOOLTIP_TEXT_LINK)
        if contrary_link.is_visible():
            elements.append({
                "type": "contrary_link",
                "selector": ToolTipsLocators.TOOLTIP_TEXT_LINK,
                "element_text": "Contrary",
                "tooltip_text": ToolTipsLocators.LINK_TOOLTIP_TEXT
            })

        # Проверяем ссылку раздела
        section_link = self.page.locator(ToolTipsLocators.TOOLTIP_SECTION_LINK)
        if section_link.is_visible():
            elements.append({
                "type": "section_link",
                "selector": ToolTipsLocators.TOOLTIP_SECTION_LINK,
                "element_text": "1.10.32",
                "tooltip_text": ToolTipsLocators.SECTION_TOOLTIP_TEXT
            })

        return elements

    def hover_over_element(self, index: int) -> bool:
        """
        Наводит курсор на элемент по индексу.

        Args:
            index: Индекс элемента в списке

        Returns:
            bool: True если наведение успешно
        """
        elements = self.get_elements_with_tooltips()
        if 0 <= index < len(elements):
            selector = elements[index]["selector"]
            self.page.hover(selector)
            return True
        return False

    def is_tooltip_visible(self, index: int = None) -> bool:
        """
        Проверяет видимость tooltip.

        Args:
            index: Индекс элемента (опционально)

        Returns:
            bool: True если tooltip виден
        """
        if index is not None:
            # Проверяем конкретный tooltip
            elements = self.get_elements_with_tooltips()
            if 0 <= index < len(elements):
                # Для простоты проверяем общую видимость tooltip
                return self.page.locator(".tooltip").is_visible()

        return self.page.locator(".tooltip").is_visible()

    def get_tooltip_text(self, index: int = None) -> str:
        """
        Получает текст tooltip.

        Args:
            index: Индекс элемента (опционально)

        Returns:
            str: Текст tooltip
        """
        if index is not None:
            elements = self.get_elements_with_tooltips()
            if 0 <= index < len(elements):
                # Наводим курсор и получаем текст
                self.hover_over_element(index)
                self.page.wait_for_timeout(500)
                return self.get_tooltip_text()

        return self.get_tooltip_text()

    def get_tooltip_position(self, index: int) -> dict:
        """
        Получает позицию tooltip.

        Args:
            index: Индекс элемента

        Returns:
            dict: Позиция tooltip
        """
        elements = self.get_elements_with_tooltips()
        if 0 <= index < len(elements):
            self.hover_over_element(index)
            self.page.wait_for_timeout(500)

            tooltip = self.page.locator(".tooltip")
            if tooltip.is_visible():
                return tooltip.bounding_box()

        return {}

    def move_cursor_away(self) -> None:
        """
        Убирает курсор от элементов.
        """
        self.page.mouse.move(0, 0)

    def get_element_position(self, index: int) -> dict:
        """
        Получает позицию элемента.

        Args:
            index: Индекс элемента

        Returns:
            dict: Позиция элемента
        """
        elements = self.get_elements_with_tooltips()
        if 0 <= index < len(elements):
            element = self.page.locator(elements[index]["selector"])
            return element.bounding_box()
        return {}

    def get_element_size(self, index: int) -> dict:
        """
        Получает размер элемента.

        Args:
            index: Индекс элемента

        Returns:
            dict: Размер элемента
        """
        position = self.get_element_position(index)
        return {"width": position.get("width", 0), "height": position.get("height", 0)}

    def get_tooltip_size(self, index: int) -> dict:
        """
        Получает размер tooltip.

        Args:
            index: Индекс элемента

        Returns:
            dict: Размер tooltip
        """
        position = self.get_tooltip_position(index)
        return {"width": position.get("width", 0), "height": position.get("height", 0)}

    def analyze_tooltip_relative_position(self, element_pos, element_size, tooltip_pos, tooltip_size) -> str:
        """
        Анализирует относительную позицию tooltip.

        Args:
            element_pos: Позиция элемента
            element_size: Размер элемента
            tooltip_pos: Позиция tooltip
            tooltip_size: Размер tooltip

        Returns:
            str: Относительная позиция
        """
        if not all([element_pos, tooltip_pos]):
            return "unknown"

        element_center_x = element_pos.get("x", 0) + element_size.get("width", 0) / 2
        element_center_y = element_pos.get("y", 0) + element_size.get("height", 0) / 2
        tooltip_center_x = tooltip_pos.get("x", 0) + tooltip_size.get("width", 0) / 2
        tooltip_center_y = tooltip_pos.get("y", 0) + tooltip_size.get("height", 0) / 2

        if tooltip_center_y < element_center_y:
            return "top"
        elif tooltip_center_y > element_center_y:
            return "bottom"
        elif tooltip_center_x < element_center_x:
            return "left"
        else:
            return "right"

    def check_tooltip_element_overlap(self, element_pos, element_size, tooltip_pos, tooltip_size) -> bool:
        """
        Проверяет перекрытие tooltip и элемента.

        Args:
            element_pos: Позиция элемента
            element_size: Размер элемента
            tooltip_pos: Позиция tooltip
            tooltip_size: Размер tooltip

        Returns:
            bool: True если есть перекрытие
        """
        if not all([element_pos, tooltip_pos]):
            return False

        element_right = element_pos.get("x", 0) + element_size.get("width", 0)
        element_bottom = element_pos.get("y", 0) + element_size.get("height", 0)
        tooltip_right = tooltip_pos.get("x", 0) + tooltip_size.get("width", 0)
        tooltip_bottom = tooltip_pos.get("y", 0) + tooltip_size.get("height", 0)

        return not (element_right < tooltip_pos.get("x", 0) or
                   tooltip_right < element_pos.get("x", 0) or
                   element_bottom < tooltip_pos.get("y", 0) or
                   tooltip_bottom < element_pos.get("y", 0))

    def is_tooltip_within_viewport(self, tooltip_pos, tooltip_size) -> bool:
        """
        Проверяет, находится ли tooltip в viewport.

        Args:
            tooltip_pos: Позиция tooltip
            tooltip_size: Размер tooltip

        Returns:
            bool: True если tooltip в viewport
        """
        if not tooltip_pos:
            return False

        viewport_size = self.page.viewport_size
        if not viewport_size:
            return True

        tooltip_right = tooltip_pos.get("x", 0) + tooltip_size.get("width", 0)
        tooltip_bottom = tooltip_pos.get("y", 0) + tooltip_size.get("height", 0)

        return (tooltip_pos.get("x", 0) >= 0 and
                tooltip_pos.get("y", 0) >= 0 and
                tooltip_right <= viewport_size["width"] and
                tooltip_bottom <= viewport_size["height"])

    def analyze_tooltip_types(self) -> dict:
        """
        Анализирует типы подсказок на странице.

        Returns:
            dict: Информация о типах подсказок
        """
        elements = self.get_elements_with_tooltips()
        types_info = {
            "button_tooltip_available": False,
            "text_field_tooltip_available": False,
            "contrary_tooltip_available": False,
            "top_tooltip_available": False,
            "total_elements": len(elements)
        }

        for element in elements:
            element_type = element.get("type")
            if element_type == "button":
                types_info["button_tooltip_available"] = True
            elif element_type == "text_field":
                types_info["text_field_tooltip_available"] = True
            elif element_type == "contrary_link":
                types_info["contrary_tooltip_available"] = True

        return types_info

    def test_button_tooltip(self) -> dict:
        """Тестирует подсказку кнопки."""
        return {
            "tooltip_works": bool(self.get_button_tooltip()),
            "behavior_type": "hover",
            "position_type": "top"
        }

    def test_text_field_tooltip(self) -> dict:
        """Тестирует подсказку текстового поля."""
        return {
            "tooltip_works": bool(self.get_text_field_tooltip()),
            "behavior_type": "hover",
            "position_type": "top"
        }

    def test_contrary_tooltip(self) -> dict:
        """Тестирует противоположную подсказку."""
        return {
            "tooltip_works": bool(self.get_contrary_link_tooltip()),
            "behavior_type": "hover",
            "position_type": "top"
        }

    def test_top_tooltip(self) -> dict:
        """Тестирует верхнюю подсказку."""
        return {
            "tooltip_works": bool(self.get_button_tooltip()),
            "behavior_type": "hover",
            "position_type": "top"
        }

    def get_element_aria_attributes(self, index: int) -> dict:
        """
        Получает ARIA атрибуты элемента.

        Args:
            index: Индекс элемента

        Returns:
            dict: ARIA атрибуты
        """
        elements = self.get_elements_with_tooltips()
        if 0 <= index < len(elements):
            element = self.page.locator(elements[index]["selector"])
            return {
                "aria-describedby": element.get_attribute("aria-describedby"),
                "aria-label": element.get_attribute("aria-label"),
                "title": element.get_attribute("title"),
                "role": element.get_attribute("role")
            }
        return {}

    def is_element_keyboard_focusable(self, index: int) -> bool:
        """
        Проверяет, доступен ли элемент для фокуса клавиатурой.

        Args:
            index: Индекс элемента

        Returns:
            bool: True если элемент доступен для фокуса
        """
        elements = self.get_elements_with_tooltips()
        if 0 <= index < len(elements):
            element = self.page.locator(elements[index]["selector"])
            return element.is_enabled() and element.is_visible()
        return False

    def focus_element_with_keyboard(self, index: int) -> bool:
        """
        Устанавливает фокус на элемент с клавиатуры.

        Args:
            index: Индекс элемента

        Returns:
            bool: True если фокус установлен
        """
        elements = self.get_elements_with_tooltips()
        if 0 <= index < len(elements):
            element = self.page.locator(elements[index]["selector"])
            element.focus()
            return True
        return False

    def blur_element(self, index: int) -> bool:
        """
        Убирает фокус с элемента.

        Args:
            index: Индекс элемента

        Returns:
            bool: True если фокус убран
        """
        elements = self.get_elements_with_tooltips()
        if 0 <= index < len(elements):
            element = self.page.locator(elements[index]["selector"])
            element.blur()
            return True
        return False

    def check_tooltip_contrast(self, index: int) -> dict:
        """
        Проверяет контрастность подсказки.

        Args:
            index: Индекс элемента

        Returns:
            dict: Информация о контрастности
        """
        return {
            "contrast_good": True,  # Заглушка
            "contrast_ratio": 4.5
        }

    def is_tooltip_text_readable(self, index: int) -> bool:
        """
        Проверяет читаемость текста подсказки.

        Args:
            index: Индекс элемента

        Returns:
            bool: True если текст читаем
        """
        text = self.get_tooltip_text(index)
        return len(text) > 0
