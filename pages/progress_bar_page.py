from pages.base_page import BasePage


class ProgressBarPage(BasePage):
    PROGRESS_BAR = "#progressBar"
    START_STOP_BUTTON = "#startStopButton"
    RESET_BUTTON = "#resetButton"

    def start_progress(self):
        self.page.click(self.START_STOP_BUTTON)

    def stop_progress(self):
        self.page.click(self.START_STOP_BUTTON)

    def get_progress_value(self) -> str:
        return self.page.locator(self.PROGRESS_BAR).inner_text()

    def reset_progress(self):
        self.page.click(self.RESET_BUTTON)
