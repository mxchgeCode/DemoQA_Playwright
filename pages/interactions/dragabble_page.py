"""
Page Object для страницы Dragabble с перетаскиваемыми элементами.
Содержит методы для различных типов перетаскивания (свободное, ограниченное по осям, контейнерное).
"""

import time
import logging
from playwright.sync_api import Page
from locators.interactions.dragabble_locators import DragabbleLocators
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class DragabblePage(BasePage):
    """
    Страница тестирования перетаскивания элементов с различными ограничениями.
    Поддерживает свободное перетаскивание, ограничения по осям, контейнерные ограничения.
    """

    def __init__(self, page: Page):
        """
        Инициализация страницы перетаскивания.

        Args:
            page: Экземпляр страницы Playwright
        """
        super().__init__(page)

    def drag_box(self, x_offset: int, y_offset: int) -> None:
        """
        Перетаскивает основной элемент на указанные смещения.

        Args:
            x_offset: Смещение по горизонтали в пикселях
            y_offset: Смещение по вертикали в пикселях

        Postconditions: элемент перемещен на новую позицию
        """
        self.log_step(f"Перетаскиваем элемент на смещение ({x_offset}, {y_offset})")
        drag_box = self.page.locator(DragabbleLocators.DRAG_BOX)
        box_bounding = drag_box.bounding_box()

        start_x = box_bounding["x"] + box_bounding["width"] / 2
        start_y = box_bounding["y"] + box_bounding["height"] / 2

        self.page.mouse.move(start_x, start_y)
        self.page.mouse.down()
        self.page.mouse.move(start_x + x_offset, start_y + y_offset, steps=10)
        self.page.mouse.up()

    def get_drag_box_position(self) -> tuple[float, float]:
        """
        Получает текущие координаты перетаскиваемого элемента.

        Returns:
            tuple: Координаты (x, y) левого верхнего угла элемента
        """
        drag_box = self.page.locator(DragabbleLocators.DRAG_BOX)
        box_bounding = drag_box.bounding_box()
        return box_bounding["x"], box_bounding["y"]

    def axis_restricted_tab(self) -> None:
        """
        Переключается на вкладку с ограничениями по осям.
        Postconditions: активна вкладка с элементами, ограниченными по X и Y осям.
        """
        self.log_step("Переключаемся на вкладку ограничений по осям")
        self.safe_click(DragabbleLocators.TAB_AXIS_RESTRICTED)
        time.sleep(1)

    def drag_box_axis(self, axis: str, offset: int) -> None:
        """
        Перетаскивает элемент с ограничением по определенной оси.

        Args:
            axis: Ось ограничения ("x" или "y")
            offset: Смещение в пикселях по указанной оси

        Postconditions: элемент перемещен только по указанной оси
        """
        self.log_step(f"Перетаскиваем элемент с ограничением по оси {axis}")

        if axis == "x":
            element = self.page.locator(DragabbleLocators.DRAG_BOX_AXIS_X)
        elif axis == "y":
            element = self.page.locator(DragabbleLocators.DRAG_BOX_AXIS_Y)
        else:
            return

        box_bounding = element.bounding_box()
        start_x = box_bounding["x"] + box_bounding["width"] / 2
        start_y = box_bounding["y"] + box_bounding["height"] / 2

        self.page.mouse.move(start_x, start_y)
        self.page.mouse.down()

        if axis == "x":
            self.page.mouse.move(start_x + offset, start_y, steps=10)
        else:
            self.page.mouse.move(start_x, start_y + offset, steps=10)

        self.page.mouse.up()

    def container_restricted_tab(self) -> None:
        """
        Переключается на вкладку с контейнерными ограничениями.
        Postconditions: активна вкладка с элементами, ограниченными контейнером.
        """
        self.log_step("Переключаемся на вкладку контейнерных ограничений")
        self.safe_click(DragabbleLocators.TAB_CONTAINER_RESTRICTED)
        time.sleep(1)

    def drag_box_container(
        self, locator: str, x_offset: int, y_offset: int, vertical_only: bool = False
    ) -> None:
        """
        Перетаскивает элемент в пределах контейнера.

        Args:
            locator: CSS селектор перетаскиваемого элемента
            x_offset: Смещение по горизонтали
            y_offset: Смещение по вертикали
            vertical_only: Ограничить перемещение только по вертикали

        Postconditions: элемент перемещен в пределах родительского контейнера
        """
        self.log_step(f"Перетаскиваем контейнерный элемент с ограничениями")
        element = self.page.locator(locator)

        # Отключаем выделение текста для стабильности drag&drop
        self.page.eval_on_selector(
            locator,
            """
            (el) => {
                el.style.userSelect = 'none';
                el.style.webkitUserSelect = 'none'; 
                el.style.msUserSelect = 'none';
            }
        """,
        )

        box_bounding = element.bounding_box()
        start_x = box_bounding["x"] + box_bounding["width"] / 2
        start_y = box_bounding["y"] + box_bounding["height"] / 2

        self.page.mouse.move(start_x, start_y)
        self.page.mouse.down()

        steps = abs(y_offset) if vertical_only else max(abs(x_offset), abs(y_offset))
        steps = max(steps, 10)  # минимум 10 шагов для плавности

        for step in range(1, steps + 1):
            if vertical_only:
                new_y = start_y + y_offset * step / steps
                self.page.mouse.move(start_x, new_y)
            else:
                new_x = start_x + x_offset * step / steps
                new_y = start_y + y_offset * step / steps
                self.page.mouse.move(new_x, new_y)

        self.page.mouse.up()

        # Восстанавливаем возможность выделения текста
        self.page.eval_on_selector(
            locator,
            """
            (el) => {
                el.style.userSelect = '';
                el.style.webkitUserSelect = '';
                el.style.msUserSelect = '';
            }
        """,
        )

    def cursor_style_tab(self) -> None:
        """
        Переключается на вкладку с различными стилями курсора.
        Postconditions: активна вкладка с элементами разных стилей курсора.
        """
        self.log_step("Переключаемся на вкладку стилей курсора")
        self.safe_click(DragabbleLocators.TAB_CURSOR_STYLE)
        time.sleep(1)

    def drag_box_cursor(self, locator: str, x_offset: int, y_offset: int) -> None:
        """
        Перетаскивает элемент с определенным стилем курсора.

        Args:
            locator: CSS селектор элемента со специальным курсором
            x_offset: Смещение по горизонтали
            y_offset: Смещение по вертикали

        Postconditions: элемент перемещен с демонстрацией стиля курсора
        """
        self.log_step(f"Перетаскиваем элемент с курсорным стилем: {locator}")
        element = self.page.locator(locator)
        box_bounding = element.bounding_box()

        start_x = box_bounding["x"] + box_bounding["width"] / 2
        start_y = box_bounding["y"] + box_bounding["height"] / 2

        self.page.mouse.move(start_x, start_y)
        self.page.mouse.down()
        self.page.mouse.move(start_x + x_offset, start_y + y_offset, steps=10)
        self.page.mouse.up()
