import time

from playwright.sync_api import Page
from locators.alerts.alerts_locators import AlertsLocators


class AlertsPage:
    def __init__(self, page: Page):
        self.page = page

    def click_simple_alert(self):
        self.page.locator(AlertsLocators.SIMPLE_ALERT_BUTTON).wait_for(
            state="visible", timeout=30000
        )
        time.sleep(3)
        self.page.click(AlertsLocators.SIMPLE_ALERT_BUTTON)

    def click_timer_alert(self):
        self.page.locator(AlertsLocators.TIMER_ALERT_BUTTON).wait_for(
            state="visible", timeout=30000
        )
        self.page.click(AlertsLocators.TIMER_ALERT_BUTTON)

    def click_confirm_alert(self):
        self.page.locator(AlertsLocators.CONFIRM_BUTTON).wait_for(
            state="visible", timeout=30000
        )
        self.page.click(AlertsLocators.CONFIRM_BUTTON)

    def click_prompt_alert(self):
        self.page.locator(AlertsLocators.PROMPT_BUTTON).wait_for(
            state="visible", timeout=30000
        )
        self.page.click(AlertsLocators.PROMPT_BUTTON)

    def get_confirm_result(self) -> str:
        return self.page.locator(AlertsLocators.CONFIRM_RESULT_TEXT).text_content()

    def get_prompt_result(self) -> str:
        return self.page.locator(AlertsLocators.PROMPT_RESULT_TEXT).text_content()
