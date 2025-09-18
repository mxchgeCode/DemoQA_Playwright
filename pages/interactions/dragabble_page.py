import logging
import time
from playwright.sync_api import Page, expect

from locators.interactions.dragabble_locators import DragabbleLocators

logger = logging.getLogger(__name__)

class DragabblePage:
    def __init__(self, page: Page):
        self.page = page

    def open(self):
        logger.info("Opening https://demoqa.com/dragabble")
        self.page.goto("https://demoqa.com/dragabble", wait_until="load")
        # Убедимся, что вкладка Simple активирована
        self.activate_simple_tab()

    def activate_simple_tab(self):
        logger.info("Activating Simple tab")
        self.page.click(DragabbleLocators.SIMPLE_TAB)
        expect(self.page.locator(DragabbleLocators.SIMPLE_DRAG)).to_be_visible(timeout=15000)
        time.sleep(1)

    def activate_axis_restriction_tab(self):
        logger.info("Activating Axis Restriction tab")
        self.page.click(DragabbleLocators.AXIS_RESTRICT_TAB)
        expect(self.page.locator(DragabbleLocators.AXIS_X_DRAG)).to_be_visible(timeout=15000)
        time.sleep(1)

    def activate_container_restriction_tab(self):
        logger.info("Activating Container Restriction tab")
        self.page.click(DragabbleLocators.CONTAINER_RESTRICT_TAB)
        expect(self.page.locator(DragabbleLocators.CONTAINER_DRAG)).to_be_visible(timeout=15000)
        time.sleep(1)

    def activate_cursor_style_tab(self):
        logger.info("Activating Cursor Style tab")
        self.page.click(DragabbleLocators.CURSOR_STYLE_TAB)
        expect(self.page.locator(DragabbleLocators.CURSOR_DRAG)).to_be_visible(timeout=15000)
        time.sleep(1)

    def get_position(self, locator_str: str):
        locator = self.page.locator(locator_str)
        expect(locator).to_be_visible(timeout=15000)
        box = locator.bounding_box()
        logger.info(f"Bounding box for {locator_str}: {box}")
        return box

    def drag_element_by(self, locator_str: str, dx: int, dy: int):
        locator = self.page.locator(locator_str)
        box = self.get_position(locator_str)
        start_x = box["x"] + box["width"] / 2
        start_y = box["y"] + box["height"] / 2

        logger.info(f"Dragging element {locator_str} from ({start_x},{start_y}) by dx={dx}, dy={dy}")

        mouse = self.page.mouse
        mouse.move(start_x, start_y)
        mouse.down()
        steps = 20
        for step in range(steps):
            mouse.move(
                start_x + dx * (step + 1) / steps,
                start_y + dy * (step + 1) / steps,
            )
            time.sleep(0.05)
        mouse.up()
        time.sleep(1)
