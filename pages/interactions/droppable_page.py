import time
from playwright.sync_api import Page

from data import URLs
from locators.interactions.droppable_locators import DroppableLocators
import logging

logger = logging.getLogger(__name__)


class DroppablePage:
    def __init__(self, page: Page):
        self.page = page

    def open(self):
        logger.info("Open https://demoqa.com/droppable")
        self.page.goto(URLs.DROPPABLE, wait_until="domcontentloaded")

    def activate_simple_tab(self):
        logger.info("Activate Simple Tab")
        self.page.click(DroppableLocators.SIMPLE_TAB)
        self.page.wait_for_selector(DroppableLocators.SIMPLE_DRAG, state="visible")
        time.sleep(1)

    def drag_simple(self):
        logger.info("Drag simple element")
        self.page.locator(DroppableLocators.SIMPLE_DRAG).drag_to(
            self.page.locator(DroppableLocators.SIMPLE_DROP)
        )
        time.sleep(2)

    def get_simple_drop_text(self) -> str:
        text = self.page.locator(DroppableLocators.SIMPLE_DROP).text_content()
        logger.info(f"Simple Drop Text: {text}")
        return text.strip() if text else ""

    def activate_accept_tab(self):
        logger.info("Activate Accept Tab")
        self.page.click(DroppableLocators.ACCEPT_TAB)
        self.page.wait_for_selector(
            DroppableLocators.ACCEPT_DRAG_ACCEPT, state="visible"
        )
        time.sleep(1)

    def drag_accept(self, accepted: bool):
        logger.info(
            f"Drag accept - {'accepted' if accepted else 'non-accepted'} element"
        )
        source_selector = (
            DroppableLocators.ACCEPT_DRAG_ACCEPT
            if accepted
            else DroppableLocators.ACCEPT_DRAG_NON_ACCEPT
        )
        self.drag_and_drop_with_mouse(source_selector, DroppableLocators.ACCEPT_DROP)
        time.sleep(2)

    def get_accept_drop_text(self) -> str:
        text = self.page.locator(DroppableLocators.ACCEPT_DROP).text_content()
        logger.info(f"Accept Drop Text: {text}")
        return text.strip() if text else ""

    def activate_prevent_tab(self):
        logger.info("Activate Prevent Propogation Tab")
        self.page.click(DroppableLocators.PREVENT_TAB)
        self.page.wait_for_selector(
            DroppableLocators.NOT_GREEDY_DROP_BOX, state="visible"
        )
        time.sleep(1)

    def drag_and_drop_with_mouse(self, source_locator: str, target_locator: str):
        source = self.page.locator(source_locator)
        target = self.page.locator(target_locator)

        box_source = source.bounding_box()
        box_target = target.bounding_box()

        start_x = box_source["x"] + box_source["width"] / 2
        start_y = box_source["y"] + box_source["height"] / 2
        end_x = box_target["x"] + box_target["width"] / 2
        end_y = box_target["y"] + box_target["height"] / 2

        mouse = self.page.mouse
        mouse.move(start_x, start_y)
        mouse.down()
        # Разбиваем на шаги перемещение мыши с паузами между шагами, чтобы лучше сымитировать пользователя
        steps = 25
        for i in range(steps):
            x = start_x + (end_x - start_x) * (i + 1) / steps
            y = start_y + (end_y - start_y) * (i + 1) / steps
            mouse.move(x, y)
            # time.sleep(0.05)
        mouse.up()
        time.sleep(2)

    def is_drop_zone_highlighted(self, selector: str) -> bool:
        element = self.page.locator(selector)
        classes = element.get_attribute("class") or ""
        logger.info(f"Drop zone {selector} classes: {classes}")
        return "ui-state-highlight" in classes or "ui-droppable-active" in classes

    def activate_revert_tab(self):
        logger.info("Activate Revert Draggable Tab")
        self.page.click(DroppableLocators.REVERT_TAB)
        self.page.wait_for_selector(
            DroppableLocators.REVERT_DRAG_REVERT, state="visible"
        )
        time.sleep(1)

    def drag_revert(self, revert: bool):
        locator = (
            DroppableLocators.REVERT_DRAG_REVERT
            if revert
            else DroppableLocators.REVERT_DRAG_NOT_REVERT
        )
        logger.info(
            f"Drag revert - {'revertable' if revert else 'non revertable'} element"
        )
        before = self.get_position(locator)
        logger.info(f"Position before drag: {before}")

        self.drag_and_drop_with_mouse(locator, DroppableLocators.REVERT_DROP_BOX)

        after = self.get_position(locator)
        logger.info(f"Position after drag: {after}")
        return before, after

    def get_position(self, locator_str: str):
        locator = self.page.locator(locator_str)
        box = locator.bounding_box()
        logger.info(f"Bounding box of {locator_str}: {box}")
        return box

    def drag_and_drop_to_position(
        self,
        source_locator: str,
        target_locator: str,
        relative_x: float = 0.5,
        relative_y: float = 0.5,
    ):
        source = self.page.locator(source_locator)
        inner_p_locator = self.page.locator(
            f"{target_locator} > p"
        ).first  # берём первый <p> среди возможных
        box_source = source.bounding_box()
        box_target_text = inner_p_locator.bounding_box()

        logger.info(f"Source bounding box: {box_source}")
        logger.info(f"Target <p> bounding box: {box_target_text}")

        start_x = box_source["x"] + box_source["width"] / 2
        start_y = box_source["y"] + box_source["height"] / 2

        end_x = box_target_text["x"] + box_target_text["width"] * relative_x
        end_y = box_target_text["y"] + box_target_text["height"] * relative_y

        mouse = self.page.mouse
        mouse.move(start_x, start_y)
        mouse.down()
        mouse.move(end_x, end_y, steps=10)
        mouse.up()

        logger.info(f"Drag and drop from ({start_x},{start_y}) to ({end_x},{end_y})")
        time.sleep(2)
