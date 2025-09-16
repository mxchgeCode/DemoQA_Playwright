from playwright.sync_api import Page
from locators.elements.check_box_locators import CheckboxLocators
from data import URLs


class CheckboxPage:
    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto(URLs.CHECK_BOX)

    def expand_all(self):
        self.page.click(CheckboxLocators.EXPAND_ALL_BUTTON)

    def collapse_all(self):
        self.page.click(CheckboxLocators.COLLAPSE_ALL_BUTTON)

    def check_home(self):
        self.page.click(CheckboxLocators.HOME_CHECKBOX)

    def get_result_text(self) -> str:
        return self.page.locator(CheckboxLocators.CHECKBOX_RESULT).inner_text()

    def is_result_hidden_or_empty(self) -> bool:
        locator = self.page.locator(CheckboxLocators.CHECKBOX_RESULT)
        try:
            locator.wait_for(state="hidden", timeout=5000)
            return True
        except:
            # Если элемент не скрылся, проверить пустой ли текст
            try:
                text = locator.inner_text(timeout=1000).strip()
                return text == ""
            except:
                # Если не удалось получить текст - считаем, что скрыт
                return True
