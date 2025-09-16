from data import URLs
from locators.elements.dynamic_locators import DynamicPropertiesLocators
from playwright.sync_api import Page


class DynamicPropertiesPage:
    def __init__(self, page: Page):
        self.page = page
        self.locators = DynamicPropertiesLocators

    def open(self):
        self.page.goto(URLs.DYNAMIC)
        self.page.wait_for_load_state("networkidle")

    def is_enable_after_enabled(self) -> bool:
        return self.page.locator(self.locators.ENABLE_AFTER_BUTTON).is_enabled()

    def wait_and_check_enable_after(self, timeout=7000) -> bool:
        self.page.wait_for_function(
            "el => !el.disabled",
            self.page.locator(self.locators.ENABLE_AFTER_BUTTON).element_handle(),
            timeout=timeout,
        )
        return self.is_enable_after_enabled()

    def is_visible_after_visible(self, timeout=7000) -> bool:
        try:
            self.page.wait_for_selector(
                self.locators.VISIBLE_AFTER_BUTTON, timeout=timeout
            )
            return self.page.locator(self.locators.VISIBLE_AFTER_BUTTON).is_visible()
        except:
            return False

    def wait_for_text_color_change(
        self, expected_hex_color="#dc3545", timeout=1000, poll_interval=200
    ) -> bool:
        locator = self.page.locator(self.locators.COLOR_CHANGE_BUTTON)
        elapsed = 0
        while elapsed < timeout:
            current_rgb = locator.evaluate("el => window.getComputedStyle(el).color")
            parts = current_rgb.strip()[4:-1].split(",")
            r, g, b = [int(p) for p in parts]
            current_hex = f"#{r:02x}{g:02x}{b:02x}"
            if current_hex.lower() == expected_hex_color.lower():
                return True
            self.page.wait_for_timeout(poll_interval)
            elapsed += poll_interval
        return False
