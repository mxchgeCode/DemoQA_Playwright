from playwright.sync_api import Page
from locators.select_menu_locators import SelectMenuLocators


class SelectMenuPage:
    def __init__(self, page: Page):
        self.page = page
        # Основные элементы
        self.main_container = page.locator(SelectMenuLocators.MAIN_CONTAINER)

        # У нас есть только 3 уникальных элемента
        # 1. Simple Select (который называется "Select Value" и "Old Style Select")
        self.simple_select = page.locator(SelectMenuLocators.SELECT_VALUE)

        # 2. React Select One
        self.select_one_container = page.locator(
            SelectMenuLocators.SELECT_ONE_CONTAINER
        )
        self.select_one_control = page.locator(
            f"{SelectMenuLocators.SELECT_ONE_CONTAINER} div[class*='control']"
        )
        self.select_one_input = page.locator(
            f"{SelectMenuLocators.SELECT_ONE_CONTAINER} input"
        )

        # 3. React Multiselect (который называется "Multiselect drop down" и "Standard multi select")
        self.multiselect = page.locator(SelectMenuLocators.MULTISELECT)
        self.multiselect_control = page.locator(
            f"{SelectMenuLocators.MULTISELECT} ~ div[class*='control']"
        )  # Ищем контрол рядом с #cars
        self.multiselect_input = page.locator(
            f"{SelectMenuLocators.MULTISELECT} ~ div[class*='control'] input"
        )

        self.dropdown_control = page.locator(SelectMenuLocators.DROPDOWN_CONTROL)
        self.dropdown_value = page.locator(SelectMenuLocators.DROPDOWN_VALUE)

    def is_page_loaded(self) -> bool:
        try:
            return self.main_container.is_visible()
        except:
            return False

    # --- Simple Select Menu (Select Value / Old Style Select) ---
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

    def get_simple_select_options_text(self) -> list:
        options = []
        count = self.get_simple_select_options_count()
        for i in range(count):
            option_text = (
                self.simple_select.locator("option").nth(i).text_content().strip()
            )
            if option_text:
                options.append(option_text)
        return options

    def select_option_in_dropdown(self, option_text: str):
        dropdown_menu = self.page.locator(SelectMenuLocators.DROPDOWN_MENU)
        dropdown_menu.wait_for(state="visible", timeout=5000)

        options = dropdown_menu.locator(SelectMenuLocators.DROPDOWN_OPTIONS)
        option_count = options.count()
        target_index = None
        for i in range(option_count):
            text = options.nth(i).text_content()
            if text and option_text in text:
                target_index = i
                break

        if target_index is None:
            raise Exception(f"Опция '{option_text}' не найдена в dropdown")

        options.nth(target_index).click()

    def get_select_one_display_text(self) -> str:
        locator = self.select_one_container.locator(
            SelectMenuLocators.SELECT_ONE_DISPLAY_TEXT
        )
        locator.wait_for(state="visible", timeout=10000)
        text = locator.text_content()
        return text.strip() if text else ""
