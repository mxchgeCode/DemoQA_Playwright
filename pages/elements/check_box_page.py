"""
Page Object для страницы CheckBox с иерархическими чекбоксами.
Содержит методы для работы с раскрытием/сворачиванием дерева и выбором элементов.
"""

from playwright.sync_api import Page
from locators.elements.check_box_locators import CheckboxLocators
from pages.base_page import BasePage


class CheckBoxPage(BasePage):
    """
    Страница тестирования чекбоксов в виде дерева.
    Поддерживает раскрытие/сворачивание узлов и выбор элементов.
    """

    def __init__(self, page: Page):
        """
        Инициализация страницы чекбоксов.

        Args:
            page: Экземпляр страницы Playwright
        """
        super().__init__(page)

    def expand_all(self) -> None:
        """
        Раскрывает все узлы дерева чекбоксов.
        Postconditions: все вложенные чекбоксы становятся видимыми.
        """
        self.log_step("Раскрываем все узлы дерева")
        self.safe_click(CheckboxLocators.EXPAND_ALL_BUTTON)

    def collapse_all(self) -> None:
        """
        Сворачивает все узлы дерева чекбоксов.
        Postconditions: остается виден только корневой узел.
        """
        self.log_step("Сворачиваем все узлы дерева")
        self.safe_click(CheckboxLocators.COLLAPSE_ALL_BUTTON)

    def check_home(self) -> None:
        """
        Отмечает корневой чекбокс Home.
        Postconditions: все вложенные чекбоксы автоматически отмечаются.
        """
        self.log_step("Отмечаем корневой чекбокс Home")
        self.safe_click(CheckboxLocators.HOME_CHECKBOX)

    def is_result_hidden_or_empty(self) -> bool:
        """
        Проверяет, скрыт ли блок результатов или пуст.

        Returns:
            bool: True если результаты скрыты или пусты
        """
        locator = self.page.locator(CheckboxLocators.CHECKBOX_RESULT)
        try:
            # Пытаемся дождаться скрытия элемента
            locator.wait_for(state="hidden", timeout=5000)
            return True
        except:
            # Если элемент виден, проверяем пустой ли текст
            try:
                text = locator.inner_text(timeout=1000).strip()
                return text == ""
            except:
                # Если не можем получить текст, считаем что скрыт
                return True

    def get_result_text(self) -> str:
        """
        Получает текст из блока результатов выбора чекбоксов.

        Returns:
            str: Текст с информацией о выбранных элементах
        """
        try:
            locator = self.page.locator(CheckboxLocators.CHECKBOX_RESULT)
            locator.wait_for(state="visible", timeout=5000)
            return locator.inner_text()
        except Exception as e:
            self.log_step(f"Не удалось получить текст результата: {e}")
            return ""
