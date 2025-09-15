from playwright.sync_api import Page
from locators.auto_complete_locators import AutoCompleteLocators


class AutoCompletePage:
    def __init__(self, page: Page):
        self.page = page
        self.main_container = page.locator(AutoCompleteLocators.MAIN_CONTAINER)
        self.single_color_input = page.locator(AutoCompleteLocators.SINGLE_COLOR_INPUT)
        self.multi_color_input = page.locator(AutoCompleteLocators.MULTI_COLOR_INPUT)
        self.dropdown_options = page.locator(AutoCompleteLocators.DROPDOWN_OPTIONS)
        self.dropdown_container = page.locator(AutoCompleteLocators.DROPDOWN_OPTIONS)

    def is_page_loaded(self) -> bool:
        try:
            return self.main_container.is_visible()
        except:
            return False

    def fill_single_color(self, text: str):
        self.single_color_input.fill(text)
        self.page.wait_for_timeout(500)
        self.page.keyboard.press("Enter")

    def fill_multiple_colors(self, text: str):
        self.multi_color_input.focus()
        self.multi_color_input.fill(text)
        self.page.wait_for_timeout(1000)  # Увеличено ожидание dropdown
        self.page.keyboard.press("Enter")

    def select_multi_color_option(self, index: int):
        option = self.dropdown_options.nth(index)
        if option.is_visible():
            option.click()
        else:
            option_text = option.text_content().strip()
            self.page.locator(f"//*[text()='{option_text}']").first.click()
        self.page.wait_for_timeout(500)

    def get_single_color_value_correctly(self):
        try:
            selected_items = self.page.locator("div.auto-complete__single-value")
            text = selected_items.text_content().strip()
        except Exception as e:
            print(f"Ошибка получения значения: {e}")
            text = ""
        return text

    def get_multi_color_values_correctly(self) -> list:
        values = []
        try:
            selected_items = self.page.locator("div.css-1rhbuit-multiValue")
            count = selected_items.count()
            for i in range(count):
                text = selected_items.nth(i).text_content().strip()
                if text:
                    values.append(text.rstrip("×").strip())
        except Exception as e:
            print(f"Ошибка получения выбранных значений: {e}")
        return values

    def wait_for_dropdown(self, timeout=2000) -> bool:
        try:
            self.dropdown_container.wait_for(state="visible", timeout=timeout)
            return True
        except:
            return False

    def get_dropdown_options_text(self) -> list:
        options = []
        try:
            count = self.dropdown_options.count()
            for i in range(count):
                option_text = self.dropdown_options.nth(i).text_content().strip()
                if option_text:
                    options.append(option_text)
        except:
            pass
        return options
