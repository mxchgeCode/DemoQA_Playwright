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
            # Если опция не видима, попробуем кликнуть по тексту
            option_text = option.text_content().strip()
            # Ищем элемент с этим текстом в любом месте
            self.page.locator(f"//*[text()='{option_text}']").first.click()
        self.page.wait_for_timeout(500)

    def get_single_color_value_correctly(self) -> str:
        """Получает значение из поля single color. Прямой доступ к input.value."""
        # Этот метод должен возвращать значение, которое реально установлено в input
        # Для этого мы просто читаем атрибут value
        try:
            value = self.single_color_input.get_attribute("value")
            if value is not None:
                return value.strip()
            else:
                return ""
        except Exception as e:
            print(f"? Ошибка получения значения из атрибута value: {e}")
            return ""

    def get_single_color_value(self) -> str:
        """Старый метод, возвращающий пустую строку для совместимости."""
        return self.get_single_color_value_correctly()

    # --- Multi Input ---
    def fill_multiple_colors(self, text: str):
        """Заполняет поле multiple colors."""
        # Не очищаем, так как это multi-input
        self.multi_color_input.fill(text)
        self.page.wait_for_timeout(500)

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

    def get_multi_color_values_correctly(self) -> list:
        """Получает список выбранных значений из поля multiple colors."""
        values = []
        try:
            # Ищем элементы, представляющие выбранные значения (теги)
            # Они находятся внутри контейнера мульти-инпута
            selected_tags = self.multi_color_input.locator("xpath=../div[contains(@class, 'multi-value')]")
            count = selected_tags.count()
            for i in range(count):
                try:
                    tag_text = selected_tags.nth(i).text_content().strip()
                    # Убираем возможный "x" для удаления
                    cleaned_text = tag_text.rstrip('×').strip()
                    if cleaned_text:
                        values.append(cleaned_text)
                except Exception:
                    continue # Игнорируем ошибки отдельных тегов
        except Exception as e:
            print(f"? Ошибка при получении multi значений: {e}")
            # Fallback: пробуем получить значение из input
            try:
                input_value = self.multi_color_input.input_value()
                if input_value and input_value.strip():
                    values.append(input_value.strip())
            except Exception:
                pass
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
