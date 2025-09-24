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

    # === ДОПОЛНИТЕЛЬНЫЕ МЕТОДЫ ДЛЯ ТЕСТОВ ===

    def clear_single_input(self) -> None:
        """
        Очищает поле одиночного автодополнения.
        """
        self.log_step("Очищаем поле одиночного автодополнения")
        # Для React Select нужно кликнуть на контейнер, а не на input
        container = self.page.locator(AutoCompleteLocators.SINGLE_CONTAINER)
        container.click()

        # Проверяем, есть ли кнопка очистки
        clear_button = self.page.locator(AutoCompleteLocators.SINGLE_CLEAR)
        if clear_button.is_visible():
            clear_button.click()
        else:
            # Если нет кнопки очистки, используем клавиатуру
            self.page.keyboard.press("Backspace")
            self.page.keyboard.press("Delete")

    def get_single_input_value(self) -> str:
        """
        Получает значение поля одиночного автодополнения.

        Returns:
            str: Текущее значение поля
        """
        input_field = self.page.locator(AutoCompleteLocators.SINGLE_INPUT)
        return input_field.input_value()

    def type_in_single_input(self, text: str) -> None:
        """
        Вводит текст в поле одиночного автодополнения.

        Args:
            text: Текст для ввода
        """
        self.log_step(f"Вводим текст в одиночное поле: '{text}'")
        # Сначала кликаем на контейнер, чтобы активировать поле
        container = self.page.locator(AutoCompleteLocators.SINGLE_CONTAINER)
        container.click()

        # Затем вводим текст
        input_field = self.page.locator(AutoCompleteLocators.SINGLE_INPUT)
        input_field.fill(text)

    def are_single_suggestions_visible(self) -> bool:
        """
        Проверяет видимость предложений для одиночного поля.

        Returns:
            bool: True если предложения видны
        """
        return self.page.locator(AutoCompleteLocators.SINGLE_OPTIONS).count() > 0

    def get_single_suggestions_list(self) -> list[str]:
        """
        Получает список предложений для одиночного поля.

        Returns:
            list: Список текстов предложений
        """
        options = self.page.locator(AutoCompleteLocators.SINGLE_OPTIONS)
        return [options.nth(i).inner_text() for i in range(options.count())]

    def select_first_single_suggestion(self) -> bool:
        """
        Выбирает первое предложение для одиночного поля.

        Returns:
            bool: True если выбор успешен
        """
        try:
            options = self.page.locator(AutoCompleteLocators.SINGLE_OPTIONS)
            if options.count() > 0:
                options.first.click()
                return True
        except Exception as e:
            self.log_step(f"Ошибка при выборе предложения: {e}")
        return False

    def clear_multiple_input(self) -> None:
        """
        Очищает все выбранные значения множественного поля.
        """
        self.log_step("Очищаем множественное поле автодополнения")
        # Удаляем все выбранные значения
        remove_buttons = self.page.locator(AutoCompleteLocators.REMOVE_VALUE)
        count = remove_buttons.count()
        for i in range(count):
            try:
                remove_buttons.nth(i).click()
                self.page.wait_for_timeout(100)  # Небольшая пауза между удалениями
            except:
                break

    def get_multiple_selected_values(self) -> list[str]:
        """
        Получает список выбранных значений множественного поля.

        Returns:
            list: Список выбранных значений
        """
        values = []
        tags = self.page.locator(AutoCompleteLocators.MULTIPLE_VALUES)
        for i in range(tags.count()):
            tag_text = tags.nth(i).inner_text()
            values.append(tag_text.strip())
        return values

    def type_in_multiple_input(self, text: str) -> None:
        """
        Вводит текст в поле множественного автодополнения.

        Args:
            text: Текст для ввода
        """
        self.log_step(f"Вводим текст в множественное поле: '{text}'")
        # Кликаем на контейнер множественного поля
        container = self.page.locator(AutoCompleteLocators.MULTIPLE_CONTAINER)
        container.click()

        # Затем вводим текст в input поле
        input_field = self.page.locator(AutoCompleteLocators.MULTIPLE_INPUT)
        input_field.fill(text)

    def are_multiple_suggestions_visible(self) -> bool:
        """
        Проверяет видимость предложений для множественного поля.

        Returns:
            bool: True если предложения видны
        """
        return self.page.locator(AutoCompleteLocators.MULTIPLE_OPTIONS).count() > 0

    def get_multiple_suggestions_list(self) -> list[str]:
        """
        Получает список предложений для множественного поля.

        Returns:
            list: Список текстов предложений
        """
        options = self.page.locator(AutoCompleteLocators.MULTIPLE_OPTIONS)
        return [options.nth(i).inner_text() for i in range(options.count())]

    def select_multiple_suggestion_by_text(self, text: str) -> bool:
        """
        Выбирает предложение множественного поля по тексту.

        Args:
            text: Текст предложения для выбора

        Returns:
            bool: True если выбор успешен
        """
        try:
            options = self.page.locator(AutoCompleteLocators.MULTIPLE_OPTIONS)
            for i in range(options.count()):
                option_text = options.nth(i).inner_text()
                if text.lower() in option_text.lower():
                    options.nth(i).click()
                    return True
        except Exception as e:
            self.log_step(f"Ошибка при выборе предложения '{text}': {e}")
        return False

    def select_first_multiple_suggestion(self) -> bool:
        """
        Выбирает первое предложение для множественного поля.

        Returns:
            bool: True если выбор успешен
        """
        try:
            options = self.page.locator(AutoCompleteLocators.MULTIPLE_OPTIONS)
            if options.count() > 0:
                options.first.click()
                return True
        except Exception as e:
            self.log_step(f"Ошибка при выборе первого предложения: {e}")
        return False

    def clear_multiple_input_text(self) -> None:
        """
        Очищает текстовое поле множественного автодополнения (не выбранные значения).
        """
        self.log_step("Очищаем текстовое поле множественного автодополнения")
        input_field = self.page.locator(AutoCompleteLocators.MULTIPLE_INPUT)
        input_field.click()
        input_field.clear()

    def remove_multiple_value_by_index(self, index: int) -> bool:
        """
        Удаляет выбранное значение множественного поля по индексу.

        Args:
            index: Индекс значения для удаления

        Returns:
            bool: True если удаление успешно
        """
        try:
            remove_buttons = self.page.locator(AutoCompleteLocators.REMOVE_VALUE)
            if remove_buttons.count() > index:
                remove_buttons.nth(index).click()
                return True
        except Exception as e:
            self.log_step(f"Ошибка при удалении значения с индексом {index}: {e}")
        return False
