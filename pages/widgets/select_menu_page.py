"""
Page Object для страницы Select Menu.
Содержит методы для работы с различными типами выпадающих списков.
"""

import time
from playwright.sync_api import Page
from locators.widgets.selectmenu_locators import SelectMenuLocators
from pages.widgets.base_page import WidgetBasePage


class SelectMenuPage(WidgetBasePage):
    """
    Страница тестирования различных типов select меню.
    Включает одиночный выбор, множественный выбор, стандартный select и группированные опции.
    """

    def __init__(self, page: Page):
        """
        Инициализация страницы Select Menu.

        Args:
            page: Экземпляр страницы Playwright
        """
        super().__init__(page)

    def select_value(self, value_text: str) -> None:
        """
        Выбирает значение в dropdown "Select Value".

        Args:
            value_text: Текст опции для выбора

        Postconditions: выбранное значение отображается в поле
        """
        self.log_step(f"Выбираем значение в Select Value: {value_text}")

        # Кликаем по dropdown для его открытия
        self.safe_click(SelectMenuLocators.SELECT_VALUE)
        self.wait_for_dropdown_to_appear(".css-26l3qy-menu")

        # Выбираем опцию по тексту
        option = self.page.locator(f"text={value_text}").first
        if option.is_visible():
            option.click()

    def select_one(self, option_text: str) -> None:
        """
        Выбирает опцию в dropdown "Select One".

        Args:
            option_text: Текст опции для выбора

        Postconditions: выбранная опция отображается в поле
        """
        self.log_step(f"Выбираем опцию в Select One: {option_text}")

        # Кликаем по dropdown
        self.safe_click(SelectMenuLocators.SELECT_ONE)
        self.wait_for_dropdown_to_appear(".css-26l3qy-menu")

        # Выбираем опцию
        option = self.page.locator(f"text={option_text}").first
        if option.is_visible():
            option.click()

    def select_old_style_menu(self, value: str) -> None:
        """
        Выбирает значение в стандартном HTML select элементе.

        Args:
            value: Значение опции для выбора

        Postconditions: выбранное значение установлено в select
        """
        self.log_step(f"Выбираем в старом стиле меню: {value}")
        select_element = self.page.locator(SelectMenuLocators.OLD_STYLE_SELECT_MENU)
        select_element.select_option(value)

    def select_multiple_values(self, values: list[str]) -> None:
        """
        Выбирает несколько значений в multiselect dropdown.

        Args:
            values: Список текстов опций для выбора

        Postconditions: все выбранные значения отображаются как теги
        """
        self.log_step(f"Выбираем множественные значения: {values}")

        for value in values:
            # Кликаем по multiselect полю
            self.safe_click(SelectMenuLocators.MULTISELECT)

            # Ждем появления dropdown
            time.sleep(500)

            # Выбираем опцию
            option = self.page.locator(f".css-26l3qy-menu text={value}").first
            if option.is_visible():
                option.click()

    def select_standard_multiselect(self, values: list[str]) -> None:
        """
        Выбирает множественные значения в стандартном HTML multiselect.

        Args:
            values: Список значений для выбора

        Postconditions: все указанные опции выбраны в multiselect
        """
        self.log_step(f"Выбираем в стандартном multiselect: {values}")
        multiselect = self.page.locator(SelectMenuLocators.STANDARD_MULTISELECT)

        # Выбираем каждое значение с зажатым Ctrl
        for i, value in enumerate(values):
            if i == 0:
                multiselect.select_option(value)
            else:
                # Для множественного выбора используем модификатор
                multiselect.select_option(value, modifiers=["Control"])

    def get_selected_value(self) -> str:
        """
        Получает выбранное значение из "Select Value" dropdown.

        Returns:
            str: Текст выбранного значения
        """
        selected_element = self.page.locator(
            f"{SelectMenuLocators.SELECT_VALUE} .css-1wa3eu0-placeholder"
        )
        return selected_element.inner_text() if selected_element.is_visible() else ""

    def get_selected_one(self) -> str:
        """
        Получает выбранную опцию из "Select One" dropdown.

        Returns:
            str: Текст выбранной опции
        """
        selected_element = self.page.locator(
            f"{SelectMenuLocators.SELECT_ONE} .css-1wa3eu0-placeholder"
        )
        return selected_element.inner_text() if selected_element.is_visible() else ""

    def get_old_style_selected(self) -> str:
        """
        Получает выбранное значение из стандартного select.

        Returns:
            str: Значение выбранной опции
        """
        select_element = self.page.locator(SelectMenuLocators.OLD_STYLE_SELECT_MENU)
        return select_element.input_value()

    def get_multiselect_values(self) -> list[str]:
        """
        Получает список выбранных значений из multiselect dropdown.

        Returns:
            list: Список текстов выбранных значений
        """
        values = []
        tags = self.page.locator(f"{SelectMenuLocators.MULTISELECT} .css-12jo7m5")

        for i in range(tags.count()):
            tag_text = tags.nth(i).inner_text()
            # Убираем символ X из текста тега
            clean_text = tag_text.replace("×", "").strip()
            if clean_text:
                values.append(clean_text)

        return values

    def get_standard_multiselect_values(self) -> list[str]:
        """
        Получает выбранные значения из стандартного HTML multiselect.

        Returns:
            list: Список значений выбранных опций
        """
        multiselect = self.page.locator(SelectMenuLocators.STANDARD_MULTISELECT)
        return multiselect.evaluate(
            "el => Array.from(el.selectedOptions).map(o => o.value)"
        )

    def clear_select_value(self) -> None:
        """
        Очищает выбранное значение в "Select Value" dropdown.
        Postconditions: dropdown возвращается к состоянию placeholder.
        """
        self.log_step("Очищаем Select Value")
        clear_button = self.page.locator(
            f"{SelectMenuLocators.SELECT_VALUE} .css-1wy0on6"
        )
        if clear_button.is_visible():
            clear_button.click()

    def clear_select_one(self) -> None:
        """
        Очищает выбранную опцию в "Select One" dropdown.
        Postconditions: dropdown возвращается к состоянию placeholder.
        """
        self.log_step("Очищаем Select One")
        clear_button = self.page.locator(
            f"{SelectMenuLocators.SELECT_ONE} .css-1wy0on6"
        )
        if clear_button.is_visible():
            clear_button.click()

    def remove_multiselect_value(self, value_text: str) -> None:
        """
        Удаляет конкретное значение из multiselect dropdown.

        Args:
            value_text: Текст значения для удаления

        Postconditions: указанное значение удалено из выбранных
        """
        self.log_step(f"Удаляем значение из multiselect: {value_text}")

        # Ищем тег с указанным текстом и кликаем по кнопке X
        tags = self.page.locator(f"{SelectMenuLocators.MULTISELECT} .css-12jo7m5")

        for i in range(tags.count()):
            tag = tags.nth(i)
            if value_text in tag.inner_text():
                remove_button = tag.locator(".css-1wy0on6")
                if remove_button.is_visible():
                    remove_button.click()
                    break

    def clear_all_multiselect(self) -> None:
        """
        Очищает все выбранные значения в multiselect dropdown.
        Postconditions: все значения удалены из multiselect.
        """
        self.log_step("Очищаем все значения multiselect")
        clear_all_button = self.page.locator(
            f"{SelectMenuLocators.MULTISELECT} .css-1wy0on6"
        ).first
        if clear_all_button.is_visible():
            clear_all_button.click()

    def is_dropdown_open(self, dropdown_selector: str) -> bool:
        """
        Проверяет, открыт ли указанный dropdown.

        Args:
            dropdown_selector: CSS селектор dropdown элемента

        Returns:
            bool: True если dropdown открыт
        """
        menu = self.page.locator(".css-26l3qy-menu")
        return menu.is_visible()

    def get_available_options(self, dropdown_selector: str) -> list[str]:
        """
        Получает список доступных опций в открытом dropdown.

        Args:
            dropdown_selector: CSS селектор dropdown для открытия

        Returns:
            list: Список текстов доступных опций
        """
        self.log_step("Получаем список доступных опций")

        # Открываем dropdown
        self.safe_click(dropdown_selector)
        self.wait_for_dropdown_to_appear(".css-26l3qy-menu")

        # Собираем опции
        options = []
        option_elements = self.page.locator(".css-26l3qy-menu .css-1n7v3ny-option")

        for i in range(option_elements.count()):
            option_text = option_elements.nth(i).inner_text()
            options.append(option_text)

        # Закрываем dropdown кликом вне его
        self.page.click("body", position={"x": 10, "y": 10})

        return options

    def type_and_select(self, dropdown_selector: str, search_text: str) -> None:
        """
        Печатает текст в searchable dropdown и выбирает первую найденную опцию.

        Args:
            dropdown_selector: CSS селектор dropdown
            search_text: Текст для поиска

        Postconditions: выбрана первая найденная опция
        """
        self.log_step(f"Печатаем и выбираем в dropdown: {search_text}")

        # Кликаем по dropdown
        self.safe_click(dropdown_selector)

        # Печатаем текст поиска
        search_input = self.page.locator(f"{dropdown_selector} input")
        if search_input.is_visible():
            search_input.type(search_text)
            time.sleep(500)

            # Выбираем первую опцию
            first_option = self.page.locator(
                ".css-26l3qy-menu .css-1n7v3ny-option"
            ).first
            if first_option.is_visible():
                first_option.click()
