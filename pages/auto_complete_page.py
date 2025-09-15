# pages/auto_complete_page.py
from playwright.sync_api import Page
from locators.auto_complete_locators import AutoCompleteLocators


class AutoCompletePage:
    def __init__(self, page: Page):
        self.page = page
        # Основной контейнер
        self.main_container = page.locator(AutoCompleteLocators.MAIN_CONTAINER)
        # Поля ввода
        self.single_color_input = page.locator(AutoCompleteLocators.SINGLE_COLOR_INPUT)
        self.multi_color_input = page.locator(AutoCompleteLocators.MULTI_COLOR_INPUT)
        # Dropdown
        self.dropdown_options = page.locator(AutoCompleteLocators.DROPDOWN_OPTIONS)
        self.dropdown_container = page.locator(AutoCompleteLocators.DROPDOWN_OPTIONS)

    def is_page_loaded(self) -> bool:
        try:
            return self.main_container.is_visible()
        except:
            return False

    # --- Single Input ---
    def fill_single_color(self, text: str):
        """Заполняет поле single color."""
        # Очищаем поле перед вводом
        self.single_color_input.fill(text)
        self.page.wait_for_timeout(500)
        self.page.keyboard.press("Enter")

    # --- Multi Input ---
    def fill_multiple_colors(self, text: str):
        """Заполняет поле multiple colors."""

        self.multi_color_input.focus()
        self.multi_color_input.fill(text)
        self.page.wait_for_timeout(500)
        self.page.keyboard.press("Enter")

    def select_multi_color_option(self, index: int):
        """Выбирает опцию из dropdown для multi input по индексу."""
        option = self.dropdown_options.nth(index)
        if option.is_visible():
            option.click()
        else:
            # Если опция не видима, попробуем кликнуть по тексту
            option_text = option.text_content().strip()
            # Ищем элемент с этим текстом в любом месте
            self.page.locator(f"//*[text()='{option_text}']").first.click()
        self.page.wait_for_timeout(500)

    def get_single_color_value_correctly(self):
        """Получает значение из поля single color."""
        try:
            selected_items = self.page.locator("div.auto-complete__single-value")
            text = selected_items.text_content().strip()
        except Exception as e:
            print(f"? Ошибка получения значения из атрибута value: {e}")
        return text

    def get_multi_color_values_correctly(self) -> list:
        values = []
        try:
            # Предполагается, что выбранные цвета отображаются в виде отдельных опций в контейнере multi-color
            # Можно попробовать получить текст всех выбранных элементов
            selected_items = self.page.locator("div.css-1rhbuit-multiValue")
            count = selected_items.count()
            for i in range(count):
                text = selected_items.nth(i).text_content().strip()
                if text:
                    # Обычно в конце текста есть иконка удаления, её нужно убрать (например, символ '×')
                    values.append(text.rstrip("×").strip())
        except Exception as e:
            print(f"Ошибка при получении выбранных значений: {e}")

        return values

    # --- Dropdown ---
    def wait_for_dropdown(self, timeout=1000) -> bool:
        """Ждет появления dropdown."""
        try:
            self.dropdown_container.wait_for(state="visible", timeout=timeout)
            return True
        except:
            return False

    def get_dropdown_options_text(self) -> list:
        """Получает тексты опций из dropdown."""
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
