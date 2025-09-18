import time

from data import URLs
from locators.interactions.dragabble_locators import DragabbleLocators
from playwright.sync_api import Page
import logging

logger = logging.getLogger(__name__)


class DragabblePage:
    def __init__(self, page: Page):
        self.page = page

    def open(self):
        logger.info("Open https://demoqa.com/dragabble")
        self.page.goto(URLs.DRAGABBLE, wait_until="domcontentloaded")

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


