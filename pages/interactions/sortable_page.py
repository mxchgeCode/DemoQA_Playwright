"""
Page Object для страницы Sortable.
Содержит методы для тестирования сортировки элементов перетаскиванием.
"""

import time
from playwright.sync_api import Page
from locators.interactions.sortable_locators import SortableLocators
from pages.base_page import BasePage


class SortablePage(BasePage):
    """
    Страница тестирования сортировки элементов перетаскиванием.
    Поддерживает сортировку в режимах списка и сетки.
    """

    def __init__(self, page: Page):
        """
        Инициализация страницы Sortable.

        Args:
            page: Экземпляр страницы Playwright
        """
        super().__init__(page)

    def list_tab(self) -> None:
        """
        Переключается на вкладку List для сортировки элементов в виде списка.
        Postconditions: активна вкладка со списком элементов для сортировки.
        """
        self.log_step("Переключаемся на вкладку List")
        self.safe_click(SortableLocators.LIST_TAB)
        time.sleep(1)

    def grid_tab(self) -> None:
        """
        Переключается на вкладку Grid для сортировки элементов в виде сетки.
        Postconditions: активна вкладка с сеткой элементов для сортировки.
        """
        self.log_step("Переключаемся на вкладку Grid")
        self.safe_click(SortableLocators.GRID_TAB)
        time.sleep(1)

    def get_list_order(self) -> list[str]:
        """
        Получает текущий порядок элементов в списке.

        Returns:
            list: Список текстов элементов в их текущем порядке
        """
        list_items = self.page.locator(SortableLocators.LIST_ITEMS)
        return [
            list_items.nth(i).inner_text().strip() for i in range(list_items.count())
        ]

    def get_grid_order(self) -> list[str]:
        """
        Получает текущий порядок элементов в сетке.

        Returns:
            list: Список текстов элементов в их текущем порядке
        """
        grid_items = self.page.locator(SortableLocators.GRID_ITEMS)
        return [
            grid_items.nth(i).inner_text().strip() for i in range(grid_items.count())
        ]

    def drag_list_item(self, from_index: int, to_index: int) -> None:
        """
        Перетаскивает элемент списка с одной позиции на другую.

        Args:
            from_index: Исходный индекс элемента (начиная с 0)
            to_index: Целевой индекс для перемещения

        Postconditions: элемент перемещен на новую позицию, порядок списка изменен
        """
        self.log_step(
            f"Перетаскиваем элемент списка с позиции {from_index} на {to_index}"
        )
        list_items = self.page.locator(SortableLocators.LIST_ITEMS)

        if list_items.count() > max(from_index, to_index):
            source = list_items.nth(from_index)
            target = list_items.nth(to_index)

            source.drag_to(target)
            time.sleep(500)  # Пауза для стабилизации

    def drag_grid_item(self, from_index: int, to_index: int) -> None:
        """
        Перетаскивает элемент сетки с одной позиции на другую.

        Args:
            from_index: Исходный индекс элемента (начиная с 0)
            to_index: Целевой индекс для перемещения

        Postconditions: элемент перемещен на новую позицию в сетке
        """
        self.log_step(
            f"Перетаскиваем элемент сетки с позиции {from_index} на {to_index}"
        )
        grid_items = self.page.locator(SortableLocators.GRID_ITEMS)

        if grid_items.count() > max(from_index, to_index):
            source = grid_items.nth(from_index)
            target = grid_items.nth(to_index)

            source.drag_to(target)
            time.sleep(500)  # Пауза для стабилизации

    def move_list_item_to_position(self, item_text: str, target_position: int) -> None:
        """
        Перемещает элемент списка с указанным текстом на определенную позицию.

        Args:
            item_text: Текст элемента для перемещения
            target_position: Целевая позиция (начиная с 0)

        Postconditions: элемент с указанным текстом перемещен на целевую позицию
        """
        self.log_step(f"Перемещаем элемент '{item_text}' на позицию {target_position}")
        current_order = self.get_list_order()

        try:
            current_index = current_order.index(item_text)
            self.drag_list_item(current_index, target_position)
        except ValueError:
            self.log_step(f"Элемент '{item_text}' не найден в списке")

    def move_grid_item_to_position(self, item_text: str, target_position: int) -> None:
        """
        Перемещает элемент сетки с указанным текстом на определенную позицию.

        Args:
            item_text: Текст элемента для перемещения
            target_position: Целевая позиция (начиная с 0)

        Postconditions: элемент с указанным текстом перемещен на целевую позицию в сетке
        """
        self.log_step(
            f"Перемещаем элемент сетки '{item_text}' на позицию {target_position}"
        )
        current_order = self.get_grid_order()

        try:
            current_index = current_order.index(item_text)
            self.drag_grid_item(current_index, target_position)
        except ValueError:
            self.log_step(f"Элемент '{item_text}' не найден в сетке")

    def reverse_list_order(self) -> None:
        """
        Изменяет порядок элементов списка на обратный.
        Postconditions: элементы списка расположены в обратном порядке.
        """
        self.log_step("Изменяем порядок списка на обратный")
        list_count = self.page.locator(SortableLocators.LIST_ITEMS).count()

        # Перемещаем элементы с конца в начало
        for i in range(list_count - 1, 0, -1):
            self.drag_list_item(i, 0)
            time.sleep(200)

    def shuffle_list_items(self, moves: list[tuple[int, int]]) -> None:
        """
        Выполняет серию перестановок элементов списка.

        Args:
            moves: Список кортежей (from_index, to_index) для перестановок

        Postconditions: выполнены все указанные перестановки
        """
        self.log_step(f"Выполняем серию перестановок: {moves}")
        for from_idx, to_idx in moves:
            self.drag_list_item(from_idx, to_idx)
            time.sleep(300)

    def verify_list_order(self, expected_order: list[str]) -> bool:
        """
        Проверяет соответствие текущего порядка списка ожидаемому.

        Args:
            expected_order: Ожидаемый порядок элементов

        Returns:
            bool: True если порядок соответствует ожидаемому
        """
        current_order = self.get_list_order()
        return current_order == expected_order

    def verify_grid_order(self, expected_order: list[str]) -> bool:
        """
        Проверяет соответствие текущего порядка сетки ожидаемому.

        Args:
            expected_order: Ожидаемый порядок элементов

        Returns:
            bool: True если порядок соответствует ожидаемому
        """
        current_order = self.get_grid_order()
        return current_order == expected_order

    def get_item_position(self, item_text: str, is_grid: bool = False) -> int:
        """
        Получает текущую позицию элемента по его тексту.

        Args:
            item_text: Текст элемента для поиска
            is_grid: True для поиска в сетке, False для поиска в списке

        Returns:
            int: Индекс позиции элемента или -1 если не найден
        """
        current_order = self.get_grid_order() if is_grid else self.get_list_order()
        try:
            return current_order.index(item_text)
        except ValueError:
            return -1

    def get_items_count(self, is_grid: bool = False) -> int:
        """
        Получает количество элементов в списке или сетке.

        Args:
            is_grid: True для сетки, False для списка

        Returns:
            int: Количество элементов
        """
        if is_grid:
            return self.page.locator(SortableLocators.GRID_ITEMS).count()
        else:
            return self.page.locator(SortableLocators.LIST_ITEMS).count()
