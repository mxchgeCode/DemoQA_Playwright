"""
Page Object для страницы AutoComplete.
Содержит методы для тестирования полей с автодополнением.
"""

import time
from playwright.sync_api import Page
from locators.widgets.autocomplete_locators import AutoCompleteLocators
from pages.base_page import BasePage


class AutoCompletePage(BasePage):
    """
    Страница тестирования автодополнения.
    Содержит поля для множественного и единичного выбора с автодополнением.
    """

    def __init__(self, page: Page):
        """
        Инициализация страницы AutoComplete.

        Args:
            page: Экземпляр страницы Playwright
        """
        super().__init__(page)

    def fill_multiple_colors(self, colors: list[str]) -> None:
        """
        Заполняет поле множественного выбора цветов.

        Args:
            colors: Список названий цветов для ввода

        Postconditions: выбранные цвета отображаются как теги в поле
        """
        self.log_step(f"Заполняем множественное поле цветами: {colors}")
        input_field = self.page.locator(AutoCompleteLocators.MULTIPLE_INPUT)

        for color in colors:
            input_field.click()
            input_field.fill(color)
            time.sleep(500)  # Ждем появления dropdown

            # Выбираем первый вариант из dropdown
            suggestions = self.page.locator(AutoCompleteLocators.MULTIPLE_OPTIONS)
            if suggestions.count() > 0:
                suggestions.first.click()

    def fill_single_color(self, color: str) -> None:
        """
        Заполняет поле единичного выбора цвета.

        Args:
            color: Название цвета для ввода

        Postconditions: выбранный цвет отображается в поле
        """
        self.log_step(f"Заполняем одиночное поле цветом: {color}")
        input_field = self.page.locator(AutoCompleteLocators.SINGLE_INPUT)

        input_field.click()
        input_field.fill(color)
        time.sleep(500)  # Ждем появления dropdown

        suggestions = self.page.locator(AutoCompleteLocators.SINGLE_OPTIONS)
        if suggestions.count() > 0:
            suggestions.first.click()

    def get_multiple_values(self) -> list[str]:
        """
        Получает список выбранных значений из множественного поля.

        Returns:
            list: Список выбранных цветов
        """
        values = []
        tags = self.page.locator(AutoCompleteLocators.MULTIPLE_VALUES)

        for i in range(tags.count()):
            tag_text = tags.nth(i).inner_text()
            values.append(tag_text.strip())

        return values

    def get_single_value(self) -> str:
        """
        Получает выбранное значение из одиночного поля.

        Returns:
            str: Выбранный цвет или пустая строка
        """
        input_field = self.page.locator(AutoCompleteLocators.SINGLE_INPUT)
        return input_field.input_value().strip()

    def remove_multiple_value(self, index: int = 0) -> None:
        """
        Удаляет значение из множественного поля по индексу.

        Args:
            index: Индекс удаляемого элемента (по умолчанию первый)

        Postconditions: указанный тег удален из поля
        """
        self.log_step(f"Удаляем значение с индексом {index}")
        remove_buttons = self.page.locator(AutoCompleteLocators.REMOVE_VALUE)

        if remove_buttons.count() > index:
            remove_buttons.nth(index).click()

    def clear_single_value(self) -> None:
        """
        Очищает одиночное поле автодополнения.
        Postconditions: поле очищено от выбранного значения.
        """
        self.log_step("Очищаем одиночное поле")
        clear_button = self.page.locator(AutoCompleteLocators.SINGLE_CLEAR)
        if clear_button.is_visible():
            clear_button.click()

    def is_dropdown_visible(self, multiple: bool = True) -> bool:
        """
        Проверяет видимость dropdown с вариантами.

        Args:
            multiple: True для множественного поля, False для одиночного

        Returns:
            bool: True если dropdown виден
        """
        locator = (
            AutoCompleteLocators.MULTIPLE_OPTIONS
            if multiple
            else AutoCompleteLocators.SINGLE_OPTIONS
        )
        return self.page.locator(locator).count() > 0

    def get_dropdown_options(self, multiple: bool = True) -> list[str]:
        """
        Получает список доступных опций в dropdown.

        Args:
            multiple: True для множественного поля, False для одиночного

        Returns:
            list: Список текстов доступных опций
        """
        locator = (
            AutoCompleteLocators.MULTIPLE_OPTIONS
            if multiple
            else AutoCompleteLocators.SINGLE_OPTIONS
        )
        options = self.page.locator(locator)

        return [options.nth(i).inner_text() for i in range(options.count())]

    # === Методы для совместимости с тестами ===

    def is_single_auto_complete_input_present(self) -> bool:
        """
        Проверяет наличие поля одиночного автодополнения.

        Returns:
            bool: True если поле присутствует
        """
        return self.page.locator(AutoCompleteLocators.SINGLE_INPUT).is_visible()

    def is_multiple_auto_complete_input_present(self) -> bool:
        """
        Проверяет наличие поля множественного автодополнения.

        Returns:
            bool: True если поле присутствует
        """
        return self.page.locator(AutoCompleteLocators.MULTIPLE_INPUT).is_visible()
