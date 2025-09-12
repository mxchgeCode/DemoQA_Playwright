# pages/auto_complete_page.py
from playwright.sync_api import Page
from locators.auto_complete_locators import AutoCompleteLocators


class AutoCompletePage:
    def __init__(self, page: Page):
        self.page = page
        # Single color elements
        self.single_color_input = page.locator(AutoCompleteLocators.SINGLE_COLOR_INPUT)
        self.single_color_value = page.locator(AutoCompleteLocators.SINGLE_COLOR_VALUE)
        self.clear_single_button = page.locator(AutoCompleteLocators.CLEAR_SINGLE_BUTTON)

        # Multiple color elements
        self.multi_color_input = page.locator(AutoCompleteLocators.MULTI_COLOR_INPUT)
        self.multi_color_values = page.locator(AutoCompleteLocators.MULTI_COLOR_VALUES)
        self.multi_color_remove_buttons = page.locator(AutoCompleteLocators.MULTI_COLOR_REMOVE_BUTTON)

        # Dropdown elements
        self.dropdown_options = page.locator(AutoCompleteLocators.DROPDOWN_OPTIONS)
        self.dropdown_menu = page.locator(AutoCompleteLocators.DROPDOWN_MENU)

    def fill_single_color(self, text: str):
        """Заполняет поле single color с обработкой ошибок."""
        try:
            # Явное ожидание, что элемент готов для ввода
            self.single_color_input.wait_for(state="visible", timeout=5000)
            self.single_color_input.focus()
            self.page.wait_for_timeout(500)

            # Очищаем поле перед вводом
            self.single_color_input.fill("")
            self.page.wait_for_timeout(200)

            # Вводим текст посимвольно для лучшей стабильности
            for char in text:
                self.single_color_input.type(char, delay=100)
                self.page.wait_for_timeout(100)

        except Exception as e:
            # Если fill не сработал, пробуем кликнуть и затем ввести
            try:
                self.single_color_input.click()
                self.page.wait_for_timeout(300)
                self.single_color_input.fill(text)
            except:
                # Последняя попытка - через press_sequentially
                self.single_color_input.click()
                self.page.wait_for_timeout(300)
                self.page.keyboard.press("Control+A")
                self.page.keyboard.press("Backspace")
                self.page.keyboard.type(text)

        self.page.wait_for_timeout(1000)

    def fill_multi_color(self, text: str):
        """Заполняет поле multiple color."""
        try:
            self.multi_color_input.wait_for(state="visible", timeout=5000)
            self.multi_color_input.focus()
            self.page.wait_for_timeout(500)
            self.multi_color_input.fill("")
            self.page.wait_for_timeout(200)

            for char in text:
                self.multi_color_input.type(char, delay=100)
                self.page.wait_for_timeout(100)

        except Exception as e:
            try:
                self.multi_color_input.click()
                self.page.wait_for_timeout(300)
                self.multi_color_input.fill(text)
            except:
                self.multi_color_input.click()
                self.page.wait_for_timeout(300)
                self.page.keyboard.press("Control+A")
                self.page.keyboard.press("Backspace")
                self.page.keyboard.type(text)

        self.page.wait_for_timeout(1000)

    def select_single_color_option(self, option_index: int = 0):
        """Выбирает опцию из dropdown для single color."""
        try:
            # Ждем появления опций
            self.dropdown_options.first.wait_for(state="visible", timeout=5000)
            self.dropdown_options.nth(option_index).click(force=True)
            self.page.wait_for_timeout(1000)
        except:
            # Альтернативный способ выбора
            try:
                self.page.keyboard.press("Enter")
                self.page.wait_for_timeout(1000)
            except:
                pass

    def select_multi_color_option(self, option_index: int = 0):
        """Выбирает опцию из dropdown для multiple color."""
        try:
            # Ждем появления опций
            self.dropdown_options.first.wait_for(state="visible", timeout=5000)
            self.dropdown_options.nth(option_index).click(force=True)
            self.page.wait_for_timeout(1000)
        except:
            # Альтернативный способ выбора
            try:
                self.page.keyboard.press("Enter")
                self.page.wait_for_timeout(1000)
            except:
                pass

    def get_single_color_value(self) -> str:
        """Получает значение single color."""
        try:
            if self.single_color_value.is_visible():
                return self.single_color_value.text_content().strip()
            return ""
        except:
            return ""

    def get_multi_color_values(self) -> list:
        """Получает список выбранных значений multiple color."""
        try:
            count = self.multi_color_values.count()
            values = []
            for i in range(count):
                if self.multi_color_values.nth(i).is_visible():
                    value = self.multi_color_values.nth(i).text_content().strip()
                    # Убираем символ '×' который используется для удаления
                    clean_value = value.replace('×', '').strip()
                    if clean_value:
                        values.append(clean_value)
            return values
        except:
            return []

    def clear_single_color(self):
        """Очищает single color значение."""
        try:
            if self.clear_single_button.is_visible():
                self.clear_single_button.click(force=True)
                self.page.wait_for_timeout(1000)
        except:
            pass

    def remove_multi_color_item(self, index: int = 0):
        """Удаляет элемент из multiple color по индексу."""
        try:
            remove_buttons = self.page.locator(AutoCompleteLocators.MULTI_COLOR_REMOVE_BUTTON)
            if remove_buttons.count() > index and remove_buttons.nth(index).is_visible():
                remove_buttons.nth(index).click(force=True)
                self.page.wait_for_timeout(1000)
        except:
            pass

    def get_dropdown_options_count(self) -> int:
        """Получает количество опций в dropdown."""
        try:
            # Ждем появления меню
            self.dropdown_menu.wait_for(state="visible", timeout=3000)
            return self.dropdown_options.count()
        except:
            return 0

    def get_dropdown_options_text(self) -> list:
        """Получает текст всех опций в dropdown."""
        try:
            # Ждем появления меню
            self.dropdown_menu.wait_for(state="visible", timeout=3000)
            count = self.dropdown_options.count()
            options = []
            for i in range(count):
                if self.dropdown_options.nth(i).is_visible():
                    option_text = self.dropdown_options.nth(i).text_content().strip()
                    if option_text:
                        options.append(option_text)
            return options
        except:
            return []

    def is_dropdown_visible(self) -> bool:
        """Проверяет, виден ли dropdown."""
        try:
            return self.dropdown_menu.is_visible()
        except:
            return False

    def wait_for_dropdown(self, timeout: int = 5000):
        """Ждет появления dropdown."""
        try:
            self.dropdown_menu.wait_for(state="visible", timeout=timeout)
            return True
        except:
            return False

    def wait_for_dropdown_hidden(self, timeout: int = 5000):
        """Ждет скрытия dropdown."""
        try:
            self.dropdown_menu.wait_for(state="hidden", timeout=timeout)
            return True
        except:
            return False

    def get_single_input_placeholder(self) -> str:
        """Получает placeholder текст для single input."""
        try:
            return self.single_color_input.get_attribute("placeholder") or ""
        except:
            return ""

    def get_multi_input_placeholder(self) -> str:
        """Получает placeholder текст для multi input."""
        try:
            return self.multi_color_input.get_attribute("placeholder") or ""
        except:
            return ""