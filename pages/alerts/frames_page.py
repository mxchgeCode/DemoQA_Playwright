from playwright.sync_api import Page

from data import URLs
from locators.alerts.frames_locators import FramesLocators


class FramesPage:
    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto(URLs.FRAMES)

    def get_frame1_heading_text(self) -> str:
        frame1 = self.page.frame_locator(FramesLocators.FRAME1)
        return frame1.locator(FramesLocators.FRAME1_HEADING).text_content().strip()

    def get_frame2_heading_text(self) -> str:
        frame2 = self.page.frame_locator(FramesLocators.FRAME2)
        return frame2.locator(FramesLocators.FRAME2_HEADING).text_content().strip()
