from playwright.sync_api import Page
from locators.elements.links_locators import LinksLocators
from data import URLs


class LinksPage:
    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto(URLs.LINKS_PAGE)

    def click_home_link(self):
        self.page.click(LinksLocators.HOME_LINK)

    def click_home79udw_link(self):
        self.page.click(LinksLocators.HOME79UDW_LINK)

    def click_created_link(self):
        self.page.click(LinksLocators.CREATED_LINK)

    def click_no_content_link(self):
        self.page.click(LinksLocators.NO_CONTENT_LINK)

    def click_moved_link(self):
        self.page.click(LinksLocators.MOVED_LINK)

    def click_bad_request_link(self):
        self.page.click(LinksLocators.BAD_REQUEST_LINK)

    def click_unauthorized_link(self):
        self.page.click(LinksLocators.UNAUTHORIZED_LINK)

    def click_forbidden_link(self):
        self.page.click(LinksLocators.FORBIDDEN_LINK)

    def click_not_found_link(self):
        self.page.click(LinksLocators.NOT_FOUND_LINK)

    def get_link_response_text(self) -> str:
        return self.page.locator(LinksLocators.LINK_RESPONSE).inner_text()
