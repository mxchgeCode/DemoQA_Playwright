"""
Page Object для страницы Radio Button.
Содержит методы для работы с радиокнопками и получения результатов выбора.
"""

from playwright.sync_api import Page
from locators.elements.radio_button_locators import RadioButtonLocators
from pages.base_page import BasePage


class RadioButtonPage(BasePage):
    """
    Страница тестирования радиокнопок.
    Содержит три радиокнопки: Yes, Impressive, No (отключена).
    """

    def __init__(self, page: Page):
        """
        Инициализация страницы Radio Button.

        Args:
            page: Экземпляр страницы Playwright
        """
        super().__init__(page)

    def select_yes(self) -> None:
        """
        Выбирает радиокнопку "Yes".
        Postconditions: радиокнопка Yes выбрана, отображается соответствующий результат.
        """
        self.log_step("Выбираем радиокнопку Yes")
        self.safe_click(RadioButtonLocators.YES_RADIO)

    def select_impressive(self) -> None:
        """
        Выбирает радиокнопку "Impressive".
        Postconditions: радиокнопка Impressive выбрана, отображается соответствующий результат.
        """
        self.log_step("Выбираем радиокнопку Impressive")
        self.safe_click(RadioButtonLocators.IMPRESSIVE_RADIO)

    def select_no(self) -> None:
        """
        Пытается выбрать радиокнопку "No" (отключена по умолчанию).

        Note:
            Радиокнопка No отключена и не может быть выбрана.
            Метод оставлен для тестирования поведения отключенных элементов.
        """
        self.log_step("Пытаемся выбрать радиокнопку No (отключена)")
        try:
            self.page.click(RadioButtonLocators.NO_RADIO, timeout=500)
        except:
            # Ожидаемое поведение - элемент отключен
            pass

    def get_result_text(self) -> str:
        """
        Получает текст результата выбора радиокнопки.

        Returns:
            str: Текст результата ("Yes", "Impressive" или пустая строка)
        """
        return self.get_text_safe(RadioButtonLocators.RESULT_TEXT) or ""

    def is_yes_selected(self) -> bool:
        """
        Проверяет, выбрана ли радиокнопка Yes.

        Returns:
            bool: True если Yes выбрана
        """
        try:
            yes_input = self.page.locator("input#yesRadio")
            return yes_input.is_checked()
        except:
            return False

    def is_impressive_selected(self) -> bool:
        """
        Проверяет, выбрана ли радиокнопка Impressive.

        Returns:
            bool: True если Impressive выбрана
        """
        try:
            impressive_input = self.page.locator("input#impressiveRadio")
            return impressive_input.is_checked()
        except:
            return False

    def is_no_enabled(self) -> bool:
        """
        Проверяет, доступна ли радиокнопка No для выбора.

        Returns:
            bool: True если No доступна (обычно False)
        """
        try:
            no_input = self.page.locator("input#noRadio")
            return no_input.is_enabled()
        except:
            return False

    def get_selected_option(self) -> str:
        """
        Получает название выбранной радиокнопки.

        Returns:
            str: "Yes", "Impressive", "No" или "None" если ничего не выбрано
        """
        if self.is_yes_selected():
            return "Yes"
        elif self.is_impressive_selected():
            return "Impressive"
        elif "No" in self.get_result_text():
            return "No"
        else:
            return "None"
