"""
Page Object для страницы Selectable.
Содержит методы для тестирования выбора элементов в списке и сетке.
"""

import time
from playwright.sync_api import Page
from locators.interactions.selectable_locators import SelectableLocators
from pages.base_page import BasePage


class SelectablePage(BasePage):
    """
    Страница тестирования выбора элементов.
    Поддерживает одиночный и множественный выбор в режимах списка и сетки.
    """

    def __init__(self, page: Page):
        """
        Инициализация страницы Selectable.

        Args:
            page: Экземпляр страницы Playwright
        """
        super().__init__(page)

    def list_tab(self) -> None:
        """
        Переключается на вкладку List для выбора элементов в виде списка.
        Postconditions: активна вкладка со списком элементов для выбора.
        """
        self.log_step("Переключаемся на вкладку List")
        self.safe_click(SelectableLocators.LIST_TAB)
        time.sleep(1)

    def grid_tab(self) -> None:
        """
        Переключается на вкладку Grid для выбора элементов в виде сетки.
        Postconditions: активна вкладка с сеткой элементов для выбора.
        """
        self.log_step("Переключаемся на вкладку Grid")
        self.safe_click(SelectableLocators.GRID_TAB)
        time.sleep(1)

    def select_list_item(self, item_text: str) -> None:
        """
        Выбирает элемент в списке по его тексту.

        Args:
            item_text: Текст элемента для выбора

        Postconditions: элемент выделен, добавлен класс active
        """
        self.log_step(f"Выбираем элемент списка: {item_text}")
        list_items = self.page.locator(SelectableLocators.LIST_ITEMS)

        for i in range(list_items.count()):
            item = list_items.nth(i)
            if item_text in item.inner_text():
                item.click()
                break

    def select_list_item_by_index(self, index: int) -> None:
        """
        Выбирает элемент в списке по индексу.

        Args:
            index: Индекс элемента для выбора (начиная с 0)

        Postconditions: элемент по указанному индексу выделен
        """
        self.log_step(f"Выбираем элемент списка по индексу: {index}")
        list_items = self.page.locator(SelectableLocators.LIST_ITEMS)

        if list_items.count() > index:
            list_items.nth(index).click()

    def select_grid_item(self, item_text: str) -> None:
        """
        Выбирает элемент в сетке по его тексту.

        Args:
            item_text: Текст элемента для выбора

        Postconditions: элемент сетки выделен, добавлен класс active
        """
        self.log_step(f"Выбираем элемент сетки: {item_text}")
        grid_items = self.page.locator(SelectableLocators.GRID_ITEMS)

        for i in range(grid_items.count()):
            item = grid_items.nth(i)
            if item_text in item.inner_text():
                item.click()
                break

    def select_grid_item_by_index(self, index: int) -> None:
        """
        Выбирает элемент в сетке по индексу.

        Args:
            index: Индекс элемента для выбора (начиная с 0)

        Postconditions: элемент сетки по указанному индексу выделен
        """
        self.log_step(f"Выбираем элемент сетки по индексу: {index}")
        grid_items = self.page.locator(SelectableLocators.GRID_ITEMS)

        if grid_items.count() > index:
            grid_items.nth(index).click()

    def select_multiple_list_items(self, indices: list[int]) -> None:
        """
        Выбирает несколько элементов в списке с зажатым Ctrl.

        Args:
            indices: Список индексов элементов для выбора

        Postconditions: все указанные элементы выделены
        """
        self.log_step(f"Выбираем несколько элементов списка: {indices}")
        list_items = self.page.locator(SelectableLocators.LIST_ITEMS)

        for i, index in enumerate(indices):
            if list_items.count() > index:
                if i == 0:
                    # Первый клик без модификаторов
                    list_items.nth(index).click()
                else:
                    # Остальные клики с зажатым Ctrl
                    list_items.nth(index).click(modifiers=["Control"])

    def select_multiple_grid_items(self, indices: list[int]) -> None:
        """
        Выбирает несколько элементов в сетке с зажатым Ctrl.

        Args:
            indices: Список индексов элементов для выбора

        Postconditions: все указанные элементы сетки выделены
        """
        self.log_step(f"Выбираем несколько элементов сетки: {indices}")
        grid_items = self.page.locator(SelectableLocators.GRID_ITEMS)

        for i, index in enumerate(indices):
            if grid_items.count() > index:
                if i == 0:
                    # Первый клик без модификаторов
                    grid_items.nth(index).click()
                else:
                    # Остальные клики с зажатым Ctrl
                    grid_items.nth(index).click(modifiers=["Control"])

    def get_selected_list_items(self) -> list[str]:
        """
        Получает список выбранных элементов в режиме List.

        Returns:
            list: Список текстов выбранных элементов
        """
        selected_items = self.page.locator(f"{SelectableLocators.LIST_ITEMS}.active")
        return [
            selected_items.nth(i).inner_text() for i in range(selected_items.count())
        ]

    def get_selected_grid_items(self) -> list[str]:
        """
        Получает список выбранных элементов в режиме Grid.

        Returns:
            list: Список текстов выбранных элементов
        """
        selected_items = self.page.locator(f"{SelectableLocators.GRID_ITEMS}.active")
        return [
            selected_items.nth(i).inner_text() for i in range(selected_items.count())
        ]

    def get_list_items_count(self) -> int:
        """
        Получает общее количество элементов в списке.

        Returns:
            int: Количество элементов в списке
        """
        return self.page.locator(SelectableLocators.LIST_ITEMS).count()

    def get_grid_items_count(self) -> int:
        """
        Получает общее количество элементов в сетке.

        Returns:
            int: Количество элементов в сетке
        """
        return self.page.locator(SelectableLocators.GRID_ITEMS).count()

    def clear_selection(self) -> None:
        """
        Очищает все выделенные элементы кликом в пустое место.
        Postconditions: все элементы сняты с выделения.
        """
        self.log_step("Очищаем выделение")
        # Кликаем в пустое место контейнера
        container = self.page.locator("#demo-tab-list, #demo-tab-grid")
        if container.count() > 0:
            container.first.click(position={"x": 10, "y": 10})

    def is_list_item_selected(self, index: int) -> bool:
        """
        Проверяет, выбран ли элемент списка по индексу.

        Args:
            index: Индекс элемента для проверки

        Returns:
            bool: True если элемент выбран (имеет класс active)
        """
        list_items = self.page.locator(SelectableLocators.LIST_ITEMS)
        if list_items.count() > index:
            item_class = list_items.nth(index).get_attribute("class") or ""
            return "active" in item_class
        return False

    def is_grid_item_selected(self, index: int) -> bool:
        """
        Проверяет, выбран ли элемент сетки по индексу.

        Args:
            index: Индекс элемента для проверки

        Returns:
            bool: True если элемент выбран (имеет класс active)
        """
        grid_items = self.page.locator(SelectableLocators.GRID_ITEMS)
        if grid_items.count() > index:
            item_class = grid_items.nth(index).get_attribute("class") or ""
            return "active" in item_class
        return False
