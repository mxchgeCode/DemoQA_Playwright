from playwright.sync_api import Page
from locators.select_menu_locators import SelectMenuLocators


class SelectMenuPage:
    def __init__(self, page: Page):
        self.page = page
        self.main_container = page.locator(SelectMenuLocators.MAIN_CONTAINER)
        self.simple_select = page.locator(SelectMenuLocators.SELECT_VALUE)
        self.select_one_container = page.locator(
            SelectMenuLocators.SELECT_ONE_CONTAINER
        )
        self.select_one_control = page.locator(
            f"{SelectMenuLocators.SELECT_ONE_CONTAINER} div[class*='control']"
        )
        self.select_one_input = page.locator(
            f"{SelectMenuLocators.SELECT_ONE_CONTAINER} input"
        )
        self.multiselect_control = (
            page.locator(SelectMenuLocators.MULTISELECT_CONTROL)
            .filter(has_text="Select...")
            .first
        )

    def get_multiselect_control(self):
        # return (
        #     self.page.locator(SelectMenuLocators.MULTISELECT_CONTROL)
        #     .filter(has_text="Select...")
        #     .first
        # )
        return self.page.locator(SelectMenuLocators.DROPDOWN_VALUE).nth(2)

    def multiselect_open(self):
        control = self.get_multiselect_control()
        control.wait_for(state="visible", timeout=5000)
        control.click()
        self.page.locator(SelectMenuLocators.DROPDOWN_MENU).wait_for(
            state="visible", timeout=5000
        )

    def multiselect_select_option(self, option_text: str):
        self.multiselect_open()
        input_field = self.get_multiselect_control().locator("input").first
        input_field.fill(option_text)
        self.page.keyboard.press("Enter")
        self.page.wait_for_timeout(300)
        self.page.mouse.click(0, 0)
        self.page.wait_for_timeout(300)

    def multiselect_get_placeholder(self) -> str:
        placeholder_loc = self.multiselect_control.locator(
            SelectMenuLocators.PLACEHOLDER
        ).first
        placeholder_loc.wait_for(state="visible", timeout=5000)
        text = placeholder_loc.text_content()
        return text.strip() if text else ""

    def multiselect_get_selected_options(self):
        tags = self.page.locator(SelectMenuLocators.SELECTED_TAG)
        selected = []
        for i in range(tags.count()):
            text = (
                tags.nth(i).locator(SelectMenuLocators.SELECTED_TAG_TEXT).text_content()
            )
            if text:
                selected.append(text.strip())
        return selected

    def multiselect_remove_selected_option(self, option_text: str):
        tags = self.page.locator(SelectMenuLocators.SELECTED_TAG)
        for i in range(tags.count()):
            text = (
                tags.nth(i).locator(SelectMenuLocators.SELECTED_TAG_TEXT).text_content()
            )
            if text and option_text.strip().lower() == text.strip().lower():
                close_btn = tags.nth(i).locator(SelectMenuLocators.CLOSEBUTTON)
                close_btn.click()
                self.page.wait_for_timeout(300)
                self.page.mouse.click(0, 0)
                self.page.wait_for_timeout(300)
                return
        raise Exception(f"Опция '{option_text}' для удаления не найдена")

    # --- Simple Select ---
    def select_simple_option_by_value(self, value: str):
        self.simple_select.select_option(value)
        self.page.wait_for_timeout(500)

    def select_simple_option_by_index(self, index: int):
        self.simple_select.select_option(index=index)
        self.page.wait_for_timeout(500)

    def select_simple_option_by_text(self, text: str):
        self.simple_select.select_option(label=text)
        self.page.wait_for_timeout(500)

    def get_simple_select_selected_value(self) -> str:
        return self.simple_select.input_value()

    def get_simple_select_options_count(self) -> int:
        return self.simple_select.locator("option").count()

    # def get_simple_select_options_text(self) -> list[str]:
    #     options = []
    #     count = self.get_simple_select_options_count()
    #     for i in range(count):
    #         text = self.simple_select.locator("option").nth(i).text_content()
    #         if text:
    #             options.append(text.strip())
    #     return options

    # --- Select One ---
    def select_option_in_dropdown(self, option_text: str):
        dropdown_menu = self.page.locator(SelectMenuLocators.DROPDOWN_MENU)
        dropdown_menu.wait_for(state="visible", timeout=5000)
        options = dropdown_menu.locator(SelectMenuLocators.DROPDOWN_OPTIONS)
        for i in range(options.count()):
            text = options.nth(i).text_content()
            if text and option_text in text:
                options.nth(i).click()
                return
        raise Exception(f"Опция '{option_text}' не найдена в dropdown")

    def get_select_one_display_text(self) -> str:
        locator = self.select_one_container.locator(
            SelectMenuLocators.SELECT_ONE_DISPLAY_TEXT
        )
        locator.wait_for(state="visible", timeout=5000)
        text = locator.text_content()
        return text.strip() if text else ""

    # --- Standard Multi Select ---
    def select_standard_multiselect_options(self, options: list[str]):
        multi_select = self.page.locator(SelectMenuLocators.MULTISELECT)
        multi_select.select_option(options)

    def get_selected_standard_multiselect_options(self) -> list[str]:
        multi_select = self.page.locator(SelectMenuLocators.MULTISELECT)
        return multi_select.evaluate(
            "el => Array.from(el.selectedOptions).map(opt => opt.value)"
        )

    def clear_standard_multiselect_selection(self):
        multi_select = self.page.locator(SelectMenuLocators.MULTISELECT)
        multi_select.select_option([])
