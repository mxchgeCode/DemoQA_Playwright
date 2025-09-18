from data import URLs

from playwright.sync_api import Page


class NestedFramesPage:
    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto(URLs.NESTED_FRAMES)

    def get_parent_frame_text(self) -> str:
        # Получаем первый iframe по индексу на странице
        parent_frame = self.page.frames[
            1
        ]  # frames[0] - это main frame, frames[1] - первый iframe
        return parent_frame.locator("body").text_content().strip()

    def get_child_frame_text(self) -> str:
        parent_frame = self.page.frames[1]
        child_frame = parent_frame.child_frames[0]  # первый вложенный фрейм
        return child_frame.locator("body").text_content().strip()
