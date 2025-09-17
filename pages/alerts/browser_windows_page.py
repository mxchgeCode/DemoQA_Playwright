from playwright.sync_api import Page

from data import URLs
from locators.alerts.browser_windows_locators import BrowserWindowsLocators


class BrowserWindowsPage:
    def __init__(self, page: Page):
        self.page = page

    def click_new_tab(self):
        self.page.click(BrowserWindowsLocators.NEW_TAB_BUTTON)

    def click_new_window(self):
        self.page.click(BrowserWindowsLocators.NEW_WINDOW_BUTTON)

    def click_new_window_message(self):
        self.page.click(BrowserWindowsLocators.NEW_WINDOW_MESSAGE_BUTTON)
