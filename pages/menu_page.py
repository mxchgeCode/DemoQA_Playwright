from playwright.sync_api import Page, expect
import time


class MenuPage:
    def __init__(self, page: Page):
        self.page = page
        self.menu1_items = page.locator("ul#nav > li")
        self.menu2_items = page.locator("ul#nav > li:nth-child(2) ul > li")
        self.menu3_items = page.locator("ul#nav > li:nth-child(2) ul > li ul > li")

    def goto(self):
        self.page.goto("https://demoqa.com/menu#")

    def menu1_count(self):
        return self.menu1_items.count()

    def is_menu1_visible(self, index: int):
        return self.menu1_items.nth(index).is_visible()

    def is_menu2_visible(self, index: int):
        locator = self.menu2_items.nth(index)
        if locator.count() == 0:
            return False
        expect(locator).to_be_visible(timeout=500)
        return True

    def is_menu3_visible(self, index: int):
        locator = self.menu3_items.nth(index)
        if locator.count() == 0:
            return False
        expect(locator).to_be_visible(timeout=500)
        return True

    def hover_menu1(self, index: int):
        self.menu1_items.nth(index).hover()
        time.sleep(2)  # пауза для стабильности

    def hover_menu2(self, index: int):
        self.menu2_items.nth(index).hover()
        time.sleep(2)

    def hover_sub_sub_list(self):
        sub_sub_list_item = self.page.locator(
            "ul#nav > li:nth-child(2) ul > li", has_text="SUB SUB LIST »"
        )
        sub_sub_list_item.hover()
        time.sleep(2)
