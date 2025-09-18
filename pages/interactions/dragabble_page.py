import time

from data import URLs
from locators.interactions.dragabble_locators import DragabbleLocators
from playwright.sync_api import Page
import logging

logger = logging.getLogger(__name__)


class DragabblePage:
    def __init__(self, page: Page):
        self.page = page

    def drag_box(self, x_offset: int, y_offset: int):
        drag_box = self.page.locator(DragabbleLocators.DRAG_BOX)
        box_bounding = drag_box.bounding_box()
        start_x = box_bounding["x"] + box_bounding["width"] / 2
        start_y = box_bounding["y"] + box_bounding["height"] / 2

        self.page.mouse.move(start_x, start_y)
        self.page.mouse.down()
        self.page.mouse.move(start_x + x_offset, start_y + y_offset, steps=10)
        self.page.mouse.up()

    def get_drag_box_position(self):
        drag_box = self.page.locator(DragabbleLocators.DRAG_BOX)
        box_bounding = drag_box.bounding_box()
        return box_bounding["x"], box_bounding["y"]

    def axis_restricted_tab(self):
        logger.info("Axis Restricted Tab")
        self.page.click(DragabbleLocators.TAB_AXIS_RESTRICTED)
        time.sleep(1)

    def drag_box_axis(self, axis: str, offset: int):
        element = None
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

    # 3d tab
    def container_restricted_tab(self):
        logger.info("Container Restricted Tab")
        self.page.click(DragabbleLocators.TAB_CONTAINER_RESTRICTED)
        time.sleep(1)

    def drag_box_container(
        self, locator, x_offset: int, y_offset: int, vertical_only=False
    ):
        element = self.page.locator(locator)

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
        steps = max(steps, 10)  # минимум 10 шагов

        for step in range(1, steps + 1):
            if vertical_only:
                new_y = start_y + y_offset * step / steps
                self.page.mouse.move(start_x, new_y)
            else:
                new_x = start_x + x_offset * step / steps
                new_y = start_y + y_offset * step / steps
                self.page.mouse.move(new_x, new_y)
            # time.sleep(0.015)  # пауза 15мс

        self.page.mouse.up()

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

    def js_drag_vertical(self, locator, y_offset):
        self.page.eval_on_selector(
            locator,
            f"""
            el => {{
                const currentTop = parseFloat(window.getComputedStyle(el).top) || 0;
                el.style.top = (currentTop + {y_offset}) + 'px';
            }}
        """,
        )

    def cursor_style_tab(self):
        logger.info("Cursor Style Tab")
        self.page.click(DragabbleLocators.TAB_CURSOR_STYLE)
        time.sleep(1)

    def drag_box_cursor(self, locator, x_offset: int, y_offset: int):
        element = self.page.locator(locator)
        box_bounding = element.bounding_box()
        start_x = box_bounding["x"] + box_bounding["width"] / 2
        start_y = box_bounding["y"] + box_bounding["height"] / 2

        self.page.mouse.move(start_x, start_y)
        self.page.mouse.down()
        self.page.mouse.move(start_x + x_offset, start_y + y_offset, steps=10)
        self.page.mouse.up()
