from playwright.sync_api import Page
from locators.widgets.select_menu_locators import SelectMenuLocators


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
        return self.page.locator(SelectMenuLocators.DROPDOWN_VALUE).nth(2)

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

    def multiselect_open(self):
        control = self.multiselect_control
        print("Waiting for multiselect control to be visible...")
        try:
            control.wait_for(state="visible", timeout=10000)
            print("Multiselect control is visible.")
        except Exception as e:
            print(f"Failed to find multiselect control: {e}")
            raise

        print("Clicking on multiselect control to open menu...")
        try:
            control.click(force=True)
            print("Clicked on multiselect control.")
        except Exception as e:
            print(f"Failed to click multiselect control: {e}")
            raise

        try:
            print("Waiting for dropdown menu to be visible...")
            self.page.locator(SelectMenuLocators.DROPDOWN_MENU).wait_for(
                state="visible", timeout=10000
            )
            print("Dropdown menu is visible.")
        except Exception as e:
            print(f"Failed to find dropdown menu: {e}")
            raise

        self.page.wait_for_timeout(300)

    def multiselect_select_options(self, option_text: str):
        print(f"Selecting option: {option_text}")
        self.multiselect_open()
        option_locator = self.page.locator(
            f'{SelectMenuLocators.DROPDOWN_MENU} >> text="{option_text}"'
        ).first
        try:
            print("Waiting for option to be visible...")
            option_locator.wait_for(state="visible", timeout=7000)
            print(f"Option '{option_text}' is visible, clicking...")
            option_locator.click(force=True)
            print(f"Clicked option '{option_text}'.")
        except Exception as e:
            print(f"Failed to select option '{option_text}': {e}")
            raise
        self.page.wait_for_timeout(300)

    def multiselect_remove_selected_options(self, option_text: str):
        print(f"Removing option: {option_text}")
        tags = self.page.locator(SelectMenuLocators.SELECTED_TAG)
        count = tags.count()
        found = False
        for i in range(count):
            text = (
                tags.nth(i).locator(SelectMenuLocators.SELECTED_TAG_TEXT).text_content()
            )
            if text and option_text.strip().lower() == text.strip().lower():
                close_btn = tags.nth(i).locator(SelectMenuLocators.CLOSEBUTTON)
                print(f"Waiting for close button for option '{option_text}'...")
                close_btn.wait_for(state="visible", timeout=7000)
                print(f"Clicking close button for option '{option_text}'...")
                close_btn.click(force=True)
                self.page.wait_for_timeout(300)
                found = True
                print(f"Option '{option_text}' removed.")
                break
        if not found:
            raise Exception(f"Option '{option_text}' not found for removal")

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
        locator.wait_for(state="visible", timeout=3000)
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
