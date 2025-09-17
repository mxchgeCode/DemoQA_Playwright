import time
from pages.widgets.base_page import BasePage
from locators.widgets.progress_bar_locators import ProgressBarLocators


class ProgressBarPage(BasePage):
    def _wait_for_enabled(self, locator, timeout=5000):
        start_time = time.time()
        while True:
            if locator.is_enabled():
                return
            if time.time() - start_time > timeout / 1000:
                raise TimeoutError(f"Element did not become enabled in {timeout} ms")
            self.page.wait_for_timeout(100)

    def start_progress(self, retries=3):
        for attempt in range(retries):
            try:
                button = self.page.locator(ProgressBarLocators.START_STOP_BUTTON)
                button.wait_for(state="visible", timeout=10000)
                self._wait_for_enabled(button, timeout=5000)
                button.click()
                return
            except Exception as e:
                if attempt == retries - 1:
                    raise Exception(f"Failed to start after {retries} attempts") from e
                self.page.wait_for_timeout(1000)

    def stop_progress(self, retries=3):
        for attempt in range(retries):
            try:
                button = self.page.locator(ProgressBarLocators.START_STOP_BUTTON)
                button.wait_for(state="visible", timeout=10000)
                self._wait_for_enabled(button, timeout=5000)
                button.click()
                return
            except Exception as e:
                if attempt == retries - 1:
                    raise Exception(f"Failed to stop after {retries} attempts") from e
                self.page.wait_for_timeout(1000)

    def reset_progress(self, retries=3):
        for attempt in range(retries):
            try:
                button = self.page.locator(ProgressBarLocators.RESET_BUTTON)
                button.wait_for(state="visible", timeout=10000)
                self._wait_for_enabled(button, timeout=5000)
                print("Clicking reset button")
                button.click()
                print("Clicked reset button")
                return
            except Exception as e:
                if attempt == retries - 1:
                    raise Exception(f"Failed to reset after {retries} attempts") from e
                self.page.wait_for_timeout(1000)

    def wait_for_progress_value(self, expected_value: str, timeout=30_000):
        import time

        start = time.time()
        while time.time() - start < timeout / 1000:
            val = self.get_progress_value()
            if val == expected_value:
                return
            time.sleep(0.1)
        raise TimeoutError(f"Timeout waiting for progress value {expected_value}")

    def get_progress_value(self) -> str:
        progress_bar = self.page.locator(ProgressBarLocators.PROGRESS_BAR)
        progress_bar.wait_for(state="visible", timeout=10000)
        return progress_bar.inner_text().strip()

    def get_button_text(self) -> str:
        button = self.page.locator(ProgressBarLocators.START_STOP_BUTTON)
        button.wait_for(state="visible", timeout=10000)
        return button.inner_text().strip()
