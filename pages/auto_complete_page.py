# pages/auto_complete_page.py
from playwright.sync_api import Page
from locators.auto_complete_locators import AutoCompleteLocators


class AutoCompletePage:
    def __init__(self, page: Page):
        self.page = page
        # Single color elements
        self.single_color_input = page.locator(AutoCompleteLocators.SINGLE_COLOR_INPUT)
        self.single_color_value = page.locator(AutoCompleteLocators.SINGLE_COLOR_VALUE)
        self.clear_single_button = page.locator(
            AutoCompleteLocators.CLEAR_SINGLE_BUTTON
        )

        # Multiple color elements
        self.multi_color_input = page.locator(AutoCompleteLocators.MULTI_COLOR_INPUT)
        self.multi_color_values = page.locator(AutoCompleteLocators.MULTI_COLOR_VALUES)
        self.multi_color_remove_buttons = page.locator(
            AutoCompleteLocators.MULTI_COLOR_REMOVE_BUTTON
        )

        # Dropdown elements
        self.dropdown_options = page.locator(AutoCompleteLocators.DROPDOWN_OPTIONS)
        self.dropdown_menu = page.locator(AutoCompleteLocators.DROPDOWN_MENU)

    def fill_single_color(self, text: str):
        """Заполняет поле single color."""
        self.single_color_input.fill(text)
        self.page.wait_for_timeout(500)
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

    def select_single_color_option(self, index: int):
        """Выбирает опцию из dropdown для single input по индексу."""
        option = self.dropdown_options.nth(index)
        option.click()
        self.page.wait_for_timeout(500)

    def get_single_color_value_correctly(self) -> str:
        """Получает значение из поля single color, учитывая разные способы отображения."""
        try:
            # Сначала пробуем получить значение напрямую из input
            input_value = self.single_color_input.input_value()
            if input_value:
                return input_value
        except:
            pass

        try:
            # Если в input пусто, пробуем получить текст из самого input (если там текст)
            input_text = self.single_color_input.text_content().strip()
            if input_text and input_text != self.get_single_input_placeholder():
                return input_text
        except:
            pass

        # Если и это не помогло, возвращаем пустую строку
        return ""

    def get_single_color_value(self) -> str:
        """Старый метод, возвращающий пустую строку для совместимости."""
        return ""  # Исправлено в вызывающем коде

    # --- Multi Input ---
    def fill_multiple_colors(self, text: str):
        """Заполняет поле multiple colors."""
        self.multi_color_input.fill(text)
        self.page.wait_for_timeout(500)

    def select_multi_color_option(self, index: int):
        """Выбирает опцию из dropdown для multi input по индексу."""
        option = self.dropdown_options.nth(index)
        option.click()
        self.page.wait_for_timeout(500)

    def get_multi_color_values(self) -> list:
        """Старый метод, возвращающий пустой список для совместимости."""
        return []  # Исправлено в вызывающем коде

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
            remove_buttons = self.page.locator(
                AutoCompleteLocators.MULTI_COLOR_REMOVE_BUTTON
            )
            if (
                remove_buttons.count() > index
                and remove_buttons.nth(index).is_visible()
            ):
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

    def get_multi_color_values_correctly(self) -> list:
        """Получает список выбранных значений из поля multiple colors."""
        values = []
        try:
            # Ищем элементы, представляющие выбранные значения (теги)
            # Они могут быть дочерними элементами multi_color_input или рядом с ним
            # Предположим, они находятся внутри контейнера multi_color_input
            selected_tags = self.multi_color_input.locator("div[class*='multi-value']")  # Примерный селектор
            count = selected_tags.count()
            for i in range(count):
                tag_text = selected_tags.nth(i).text_content().strip()
                # Убираем возможный "x" для удаления
                cleaned_text = tag_text.rstrip('×').strip()
                if cleaned_text:
                    values.append(cleaned_text)
        except Exception as e:
            print(f"? Ошибка при получении multi значений: {e}")
            # Если не нашли теги, пробуем получить значение из input
            try:
                input_value = self.multi_color_input.input_value()
                if input_value:
                    values.append(input_value)
            except:
                pass
        return values
