# pages/auto_complete_page.py
from playwright.sync_api import Page
from locators.auto_complete_locators import AutoCompleteLocators


class AutoCompletePage:
    def __init__(self, page: Page):
        self.page = page
        self.main_container = page.locator(AutoCompleteLocators.MAIN_CONTAINER)
        self.single_color_input = page.locator(AutoCompleteLocators.SINGLE_COLOR_INPUT)
        self.multi_color_input = page.locator(AutoCompleteLocators.MULTI_COLOR_INPUT)
        self.dropdown_options = page.locator(AutoCompleteLocators.DROPDOWN_OPTIONS)
        self.dropdown_container = page.locator(AutoCompleteLocators.DROPDOWN_CONTAINER)

    def is_page_loaded(self) -> bool:
        try:
            return self.main_container.is_visible()
        except:
            return False

    # --- Single Input ---
    def fill_single_color(self, text: str):
        """Заполняет поле single color."""
        # Очищаем поле перед вводом
        self.single_color_input.fill("")
        self.page.wait_for_timeout(200)
        self.single_color_input.fill(text)
        self.page.wait_for_timeout(500)

    def select_single_color_option(self, index: int):
        """Выбирает опцию из dropdown для single input по индексу."""
        option = self.dropdown_options.nth(index)
        if option.is_visible():
            option.click()
        else:
            # Если опция не видима, кликаем по тексту
            option_text = option.text_content().strip()
            self.page.locator(f"//*[text()='{option_text}']").first.click()
        self.page.wait_for_timeout(500)

    def get_single_color_value_correctly(self) -> str:
        """Получает значение из поля single color, учитывая разные способы отображения."""
        try:
            # Сначала пробуем получить значение напрямую из input
            input_value = self.single_color_input.input_value()
            if input_value and input_value.strip():
                return input_value.strip()
        except Exception as e:
            print(f"? Ошибка получения значения из input: {e}")

        try:
            # Если в input пусто, пробуем получить текст из самого input (если там текст)
            input_text = self.single_color_input.text_content().strip()
            placeholder = self.get_single_input_placeholder()
            if input_text and input_text != placeholder and input_text.strip():
                return input_text.strip()
        except Exception as e:
            print(f"? Ошибка получения текста из input: {e}")

        # Если и это не помогло, возвращаем пустую строку
        return ""

    def get_single_color_value(self) -> str:
        """Старый метод, возвращающий пустую строку для совместимости."""
        return self.get_single_color_value_correctly()

    # --- Multi Input ---
    def fill_multiple_colors(self, text: str):
        """Заполняет поле multiple colors."""
        # Очищаем поле перед вводом (не всегда возможно для multi-input)
        # self.multi_color_input.fill("")
        # self.page.wait_for_timeout(200)
        self.multi_color_input.fill(text)
        self.page.wait_for_timeout(500)

    def select_multi_color_option(self, index: int):
        """Выбирает опцию из dropdown для multi input по индексу."""
        option = self.dropdown_options.nth(index)
        if option.is_visible():
            option.click()
        else:
            # Если опция не видима, кликаем по тексту
            option_text = option.text_content().strip()
            self.page.locator(f"//*[text()='{option_text}']").first.click()
        self.page.wait_for_timeout(500)

    def get_multi_color_values_correctly(self) -> list:
        """Получает список выбранных значений из поля multiple colors."""
        values = []
        try:
            # Ищем элементы, представляющие выбранные значения (теги)
            # Они могут быть дочерними элементами multi_color_input или рядом с ним
            # Предположим, они находятся внутри контейнера multi_color_input или рядом
            # Более общий подход: ищем теги рядом с input
            selected_tags = self.multi_color_input.locator("xpath=following-sibling::div | ..//div[contains(@class, 'multi-value')]")
            count = selected_tags.count()
            for i in range(count):
                try:
                    tag_text = selected_tags.nth(i).text_content().strip()
                    # Убираем возможный "x" для удаления
                    cleaned_text = tag_text.rstrip('×').strip()
                    if cleaned_text:
                        values.append(cleaned_text)
                except:
                    continue # Игнорируем ошибки отдельных тегов
        except Exception as e:
            print(f"? Ошибка при получении multi значений (основной метод): {e}")
            # fallback: пробуем получить значение из input
            try:
                input_value = self.multi_color_input.input_value()
                if input_value and input_value.strip():
                    values.append(input_value.strip())
            except Exception as e2:
                print(f"? Ошибка при получении multi значений (fallback): {e2}")
        return values

    def get_multi_color_values(self) -> list:
        """Старый метод, возвращающий пустой список для совместимости."""
        return self.get_multi_color_values_correctly()

    # --- Dropdown ---
    def wait_for_dropdown(self, timeout=5000) -> bool:
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

    # --- Placeholders ---
    def get_single_input_placeholder(self) -> str:
        """Получает placeholder для single input."""
        try:
            return self.single_color_input.get_attribute("placeholder") or ""
        except:
            return ""

    def get_multi_input_placeholder(self) -> str:
        """Получает placeholder для multi input."""
        try:
            return self.multi_color_input.get_attribute("placeholder") or ""
        except:
            return ""
