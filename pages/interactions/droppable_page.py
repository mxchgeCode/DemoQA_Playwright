"""
Page Object для страницы Droppable.
Содержит методы для drag-and-drop операций с различными ограничениями.
"""

import time
from playwright.sync_api import Page
from locators.interactions.droppable_locators import DroppableLocators
from pages.base_page import BasePage


class DroppablePage(BasePage):
    """
    Страница тестирования drag-and-drop операций.
    Поддерживает простой drag-and-drop, проверку accept и prevent propogation.
    """

    def __init__(self, page: Page):
        """
        Инициализация страницы Droppable.

        Args:
            page: Экземпляр страницы Playwright
        """
        super().__init__(page)

    def drag_to_drop_box(self) -> None:
        """
        Перетаскивает элемент в drop box на простой вкладке.
        Postconditions: drop box меняет цвет и текст на "Dropped!"
        """
        self.log_step("Перетаскиваем элемент в drop box")
        drag_element = self.page.locator(DroppableLocators.DRAG_ME_BOX)
        drop_element = self.page.locator(DroppableLocators.DROP_HERE_BOX)
        drag_element.drag_to(drop_element)

    def get_drop_box_text(self) -> str:
        """
        Получает текст из drop box.

        Returns:
            str: Текущий текст в drop box
        """
        return self.get_text_safe(DroppableLocators.DROP_HERE_BOX)

    def is_dropped(self) -> bool:
        """
        Проверяет, был ли успешно выполнен drop.

        Returns:
            bool: True если drop box содержит "Dropped!"
        """
        return "Dropped!" in self.get_drop_box_text()

    def accept_tab(self) -> None:
        """
        Переключается на вкладку Accept.
        Postconditions: активна вкладка с acceptable и not acceptable элементами.
        """
        self.log_step("Переключаемся на вкладку Accept")
        self.safe_click(DroppableLocators.TAB_ACCEPT)
        time.sleep(1)

    def drag_acceptable_to_drop_box(self) -> None:
        """
        Перетаскивает acceptable элемент в drop box.
        Postconditions: drop принимает элемент, меняется цвет и текст.
        """
        self.log_step("Перетаскиваем acceptable элемент")
        drag_element = self.page.locator(DroppableLocators.ACCEPTABLE)
        drop_element = self.page.locator(DroppableLocators.DROP_HERE_BOX_ACCEPT)
        drag_element.drag_to(drop_element)

    def drag_not_acceptable_to_drop_box(self) -> None:
        """
        Перетаскивает not acceptable элемент в drop box.
        Postconditions: drop не принимает элемент, остается без изменений.
        """
        self.log_step("Перетаскиваем not acceptable элемент")
        drag_element = self.page.locator(DroppableLocators.NOT_ACCEPTABLE)
        drop_element = self.page.locator(DroppableLocators.DROP_HERE_BOX_ACCEPT)
        drag_element.drag_to(drop_element)

    def get_accept_drop_box_text(self) -> str:
        """
        Получает текст из accept drop box.

        Returns:
            str: Текущий текст в accept drop box
        """
        return self.get_text_safe(DroppableLocators.DROP_HERE_BOX_ACCEPT)

    def prevent_propogation_tab(self) -> None:
        """
        Переключается на вкладку Prevent Propogation.
        Postconditions: активна вкладка с nested drop boxes.
        """
        self.log_step("Переключаемся на вкладку Prevent Propogation")
        self.safe_click(DroppableLocators.TAB_PREVENT_PROPOGATION)
        time.sleep(1)

    def drag_to_outer_drop_box(self) -> None:
        """
        Перетаскивает элемент во внешний drop box.
        Postconditions: только внешний box меняется, внутренний остается.
        """
        self.log_step("Перетаскиваем во внешний drop box")
        drag_element = self.page.locator(DroppableLocators.DRAG_BOX_PREVENT)
        drop_element = self.page.locator(DroppableLocators.OUTER_DROP_BOX)
        drag_element.drag_to(drop_element)

    def drag_to_inner_drop_box(self) -> None:
        """
        Перетаскивает элемент во внутренний drop box.
        Postconditions: изменяется состояние внутреннего box.
        """
        self.log_step("Перетаскиваем во внутренний drop box")
        drag_element = self.page.locator(DroppableLocators.DRAG_BOX_PREVENT)
        drop_element = self.page.locator(DroppableLocators.INNER_DROP_BOX)
        drag_element.drag_to(drop_element)

    def get_outer_drop_box_text(self) -> str:
        """
        Получает текст внешнего drop box.

        Returns:
            str: Текст внешнего drop box
        """
        return self.get_text_safe(DroppableLocators.OUTER_DROP_BOX)

    def get_inner_drop_box_text(self) -> str:
        """
        Получает текст внутреннего drop box.

        Returns:
            str: Текст внутреннего drop box
        """
        return self.get_text_safe(DroppableLocators.INNER_DROP_BOX)

    def revert_draggable_tab(self) -> None:
        """
        Переключается на вкладку Revert Draggable.
        Postconditions: активна вкладка с revertible элементами.
        """
        self.log_step("Переключаемся на вкладку Revert Draggable")
        self.safe_click(DroppableLocators.TAB_REVERT_DRAGGABLE)
        time.sleep(1)

    # === Методы для совместимости с тестами ===

    def get_simple_drag_element_position(self) -> tuple[int, int]:
        """
        Получает позицию простого drag элемента.

        Returns:
            tuple: (x, y) координаты элемента
        """
        drag_element = self.page.locator(DroppableLocators.DRAG_ME_BOX)
        box = drag_element.bounding_box()
        return int(box["x"]), int(box["y"])

    def switch_to_accept_tab(self) -> None:
        """
        Переключается на вкладку Accept.
        """
        self.accept_tab()

    def switch_to_prevent_propagation_tab(self) -> None:
        """
        Переключается на вкладку Prevent Propagation.
        """
        self.prevent_propogation_tab()

    def switch_to_revert_draggable_tab(self) -> None:
        """
        Переключается на вкладку Revert Draggable.
        """
        self.revert_draggable_tab()

    def switch_to_simple_tab(self) -> None:
        """
        Переключается на простую вкладку (Simple).
        """
        # Для простой вкладки не нужно переключение, она активна по умолчанию
        pass
