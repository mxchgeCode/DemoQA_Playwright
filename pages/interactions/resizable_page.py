from playwright.sync_api import Page
import logging

logger = logging.getLogger(__name__)


class ResizablePage:
    def __init__(self, page: Page):
        self.page = page

    def resize_box(self, delta_x: int, delta_y: int):
        logger.info(
            f"Начинаем ресайз блока с ограничением на dx={delta_x}, dy={delta_y}"
        )
        handle = self.page.locator(
            "#resizableBoxWithRestriction > span.react-resizable-handle-se"
        )
        box = self.page.locator("#resizableBoxWithRestriction")
        size_before = self.get_box_size()

        box_bounding = box.bounding_box()
        handle_bounding = handle.bounding_box()

        # Координаты начала drag (центр ручки)
        start_x = handle_bounding["x"] + handle_bounding["width"] / 2
        start_y = handle_bounding["y"] + handle_bounding["height"] / 2

        # Координаты конца drag с учетом смещений
        end_x = start_x + delta_x
        end_y = start_y + delta_y

        mouse = self.page.mouse
        mouse.move(start_x, start_y)
        mouse.down()
        mouse.move(end_x, end_y, steps=10)
        mouse.up()

        size_after = self.get_box_size()
        logger.info(f"Размер блока до: {size_before}, после: {size_after}")
        return size_before, size_after

    def get_box_size(self):
        box = self.page.locator("#resizableBoxWithRestriction")
        width = box.evaluate("el => el.offsetWidth")
        height = box.evaluate("el => el.offsetHeight")
        return width, height

    # Аналогично можно для кнопки resizable
    def resize_button(self, delta_x: int, delta_y: int):
        logger.info(f"Начинаем ресайз кнопки на dx={delta_x}, dy={delta_y}")
        handle = self.page.locator("#resizable > span.react-resizable-handle-se")
        btn = self.page.locator("#resizable")
        size_before = self.get_button_size()

        btn_bounding = btn.bounding_box()
        handle_bounding = handle.bounding_box()

        start_x = handle_bounding["x"] + handle_bounding["width"] / 2
        start_y = handle_bounding["y"] + handle_bounding["height"] / 2
        end_x = start_x + delta_x
        end_y = start_y + delta_y

        mouse = self.page.mouse
        mouse.move(start_x, start_y)
        mouse.down()
        mouse.move(end_x, end_y, steps=10)
        mouse.up()

        size_after = self.get_button_size()
        logger.info(f"Размер кнопки до: {size_before}, после: {size_after}")
        return size_before, size_after

    def get_button_size(self):
        btn = self.page.locator("#resizable")
        width = btn.evaluate("el => el.offsetWidth")
        height = btn.evaluate("el => el.offsetHeight")
        return width, height
