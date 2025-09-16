from playwright.sync_api import Page
from locators.elements.broken_links_locators import BrokenLinksLocators
from data import URLs


class BrokenLinksPage:
    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto(URLs.BROKEN_LINKS)
        self.page.wait_for_load_state("networkidle")

    def is_image_broken(self, selector: str) -> bool:
        widths = self.page.locator(selector).evaluate_all(
            "elements => elements.map(e => e.naturalWidth)"
        )
        if not widths:
            raise Exception(f"Ни одного элемента с селектором {selector} не найдено")
        return all(width == 0 for width in widths)

    def valid_image_broken(self) -> bool:
        return self.is_image_broken(BrokenLinksLocators.VALID_IMAGE)

    def broken_image_broken(self) -> bool:
        return self.is_image_broken(BrokenLinksLocators.BROKEN_IMAGE)

    def is_valid_link_broken(self) -> bool:
        href = self.page.get_attribute(BrokenLinksLocators.VALID_LINK, "href")
        response = self.page.request.get(href)
        return response.ok

    def is_broken_link_broken(self) -> bool:
        href = self.page.get_attribute(BrokenLinksLocators.BROKEN_LINK, "href")
        response = self.page.request.get(href)
        return not response.ok
