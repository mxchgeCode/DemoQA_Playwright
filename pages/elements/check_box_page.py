from playwright.sync_api import Page
from locators.elements.check_box_locators import CheckboxLocators
from data import URLs


class CheckBoxPage:
    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto(URLs.CHECK_BOX)

    def expand_all(self):
        print("Clicking expand all button")
        self.page.click(CheckboxLocators.EXPAND_ALL_BUTTON)
        print("Clicked expand all")

    def collapse_all(self):
        print("Clicking collapse all button")
        self.page.click(CheckboxLocators.COLLAPSE_ALL_BUTTON)
        print("Clicked collapse all")

    def is_result_hidden_or_empty(self) -> bool:
        locator = self.page.locator(CheckboxLocators.CHECKBOX_RESULT)
        try:
            print("Waiting for result element to be hidden...")
            locator.wait_for(state="hidden", timeout=5000)
            print("Result element is hidden")
            return True
        except:
            print("Result element is not hidden, checking if text is empty")
            try:
                text = locator.inner_text(timeout=1000).strip()
                print(f"Result element text: '{text}'")
                return text == ""
            except:
                print("Failed to get text from result element, assuming hidden")
                return True

    def check_home(self):
        print("Clicking home checkbox")
        self.page.click(CheckboxLocators.HOME_CHECKBOX)
        print("Clicked home checkbox")

    def get_result_text(self) -> str:
        try:
            locator = self.page.locator(CheckboxLocators.CHECKBOX_RESULT)
            locator.wait_for(state="visible", timeout=5000)
            text = locator.inner_text()
            print(f"Result text: {text}")
            return text
        except Exception as e:
            print(f"Failed to get result text: {e}")
            return ""
