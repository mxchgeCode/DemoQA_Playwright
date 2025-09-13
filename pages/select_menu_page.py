# pages/select_menu_page.py
from playwright.sync_api import Page
from locators.select_menu_locators import SelectMenuLocators


class SelectMenuPage:
    def __init__(self, page: Page):
        self.page = page
        self.main_container = page.locator(SelectMenuLocators.MAIN_CONTAINER)

        # Select Value
        self.select_value_container = page.locator(SelectMenuLocators.SELECT_VALUE_CONTAINER)
        self.select_value_input = page.locator(SelectMenuLocators.SELECT_VALUE_INPUT)
        self.select_value_indicator = page.locator(SelectMenuLocators.SELECT_VALUE_INDICATOR)

        # Select One
        self.select_one_container = page.locator(SelectMenuLocators.SELECT_ONE_CONTAINER)
        self.select_one_input = page.locator(SelectMenuLocators.SELECT_ONE_INPUT)
        self.select_one_indicator = page.locator(SelectMenuLocators.SELECT_ONE_INDICATOR)

        # Old Style Select
        self.old_style_select = page.locator(SelectMenuLocators.OLD_STYLE_SELECT)
        self.old_style_select_options = page.locator(SelectMenuLocators.OLD_STYLE_SELECT_OPTIONS)

        # Multiselect
        self.multiselect_input = page.locator(SelectMenuLocators.MULTISELECT_INPUT)
        self.multiselect_indicator = page.locator(SelectMenuLocators.MULTISELECT_INDICATOR)

        # Standard Multi Select
        self.standard_multi_select = page.locator(SelectMenuLocators.STANDARD_MULTI_SELECT)
        self.standard_multi_select_options = page.locator(SelectMenuLocators.STANDARD_MULTI_SELECT_OPTIONS)

        # Общие
        self.dropdown_option = page.locator(SelectMenuLocators.DROPDOWN_OPTION)
        self.dropdown_menu = page.locator(SelectMenuLocators.DROPDOWN_MENU)

    def _wait_for_element_visible(self, locator, timeout=5000, description="Элемент"):  # Уменьшен таймаут
        """Универсальный метод ожидания видимости элемента."""
        try:
            locator.wait_for(state="visible", timeout=timeout)
            print(f"✓ {description} стал видимым")
            return True
        except Exception as e:
            print(f"Х {description} не стал видимым в течение {timeout}мс: {e}")
            return False

    # --- Select Value ---
    def open_select_value_dropdown(self):
        print("Попытка открыть dropdown Select Value...")
        if not self._wait_for_element_visible(self.select_value_container, 5000, "Контейнер Select Value"):
            raise Exception("Контейнер Select Value не видим")

        # Прокрутка
        try:
            self.select_value_input.scroll_into_view_if_needed()
        except:
            pass

        # Клик по индикатору (стрелке) - более надежный способ
        try:
            self.select_value_indicator.click(force=True, timeout=2000)  # force=True, малый таймаут
            print("✓ Клик по индикатору Select Value")
        except Exception as e1:
            print(f"? Клик по индикатору не удался: {e1}")
            # fallback на input
            try:
                self.select_value_input.click(force=True, timeout=2000)
                print("✓ Клик по Input Select Value (force)")
            except Exception as e2:
                print(f"? Клик по Input тоже не удался: {e2}")
                raise Exception(f"Не удалось открыть Select Value: {e1}, {e2}")

        self.page.wait_for_timeout(500)  # Короткая пауза
        print("✓ Dropdown Select Value, вероятно, открыт")

    def select_option_in_select_value(self, option_text: str):
        # Ищем опцию сразу, не вызывая open_dropdown
        option_locator = self.page.locator(SelectMenuLocators.DROPDOWN_OPTION).filter(has_text=option_text)
        if option_locator.count() == 0 or not option_locator.first.is_visible():
            # Если не нашли, пробуем частичное совпадение
            option_locator = self.page.locator(SelectMenuLocators.DROPDOWN_OPTION).filter(
                has_text=re.compile(f".*{re.escape(option_text)}.*", re.IGNORECASE))

        if option_locator.count() > 0 and option_locator.first.is_visible():
            option_to_click = option_locator.first
            print(f"✓ Опция '{option_text}' найдена")
        else:
            any_option = self.page.locator(SelectMenuLocators.DROPDOWN_OPTION).first
            if any_option.count() > 0 and any_option.is_visible():
                option_to_click = any_option
                print(f"~ Выбираем первую доступную опцию, так как '{option_text}' не найдена точно")
            else:
                raise Exception(f"Опция '{option_text}' и другие опции не найдены или не видимы")

        try:
            option_to_click.click(force=True, timeout=2000)  # force=True, малый таймаут
            print(f"✓ Опция '{option_text}' кликнута")
        except Exception as e:
            print(f"? Клик по опции не удался: {e}")
            raise
        self.page.wait_for_timeout(500)

    def get_select_value_selected_text(self) -> str:
        try:
            value_container = self.select_value_container.locator("div[class*='singleValue']")
            if value_container.count() > 0 and value_container.is_visible():
                return value_container.text_content().strip()
        except:
            pass
        return ""

    # --- Select One ---
    def open_select_one_dropdown(self):
        print("Попытка открыть dropdown Select One...")
        if not self._wait_for_element_visible(self.select_one_container, 5000, "Контейнер Select One"):
            raise Exception("Контейнер Select One не видим")

        try:
            self.select_one_input.scroll_into_view_if_needed()
        except:
            pass

        try:
            self.select_one_indicator.click(force=True, timeout=2000)
            print("✓ Клик по индикатору Select One")
        except Exception as e1:
            print(f"? Клик по индикатору не удался: {e1}")
            try:
                self.select_one_input.click(force=True, timeout=2000)
                print("✓ Клик по Input Select One (force)")
            except Exception as e2:
                print(f"? Клик по Input тоже не удался: {e2}")
                raise Exception(f"Не удалось открыть Select One: {e1}, {e2}")

        self.page.wait_for_timeout(500)
        print("✓ Dropdown Select One, вероятно, открыт")

    def select_option_in_select_one(self, option_text: str):
        # Ищем опцию сразу
        option_locator = self.page.locator(SelectMenuLocators.DROPDOWN_OPTION).filter(has_text=option_text)
        if option_locator.count() == 0 or not option_locator.first.is_visible():
            option_locator = self.page.locator(SelectMenuLocators.DROPDOWN_OPTION).filter(
                has_text=re.compile(f".*{re.escape(option_text)}.*", re.IGNORECASE))

        if option_locator.count() > 0 and option_locator.first.is_visible():
            option_to_click = option_locator.first
            print(f"✓ Опция '{option_text}' найдена")
        else:
            any_option = self.page.locator(SelectMenuLocators.DROPDOWN_OPTION).first
            if any_option.count() > 0 and any_option.is_visible():
                option_to_click = any_option
                print(f"~ Выбираем первую доступную опцию, так как '{option_text}' не найдена точно")
            else:
                raise Exception(f"Опция '{option_text}' и другие опции не найдены или не видимы")

        try:
            option_to_click.click(force=True, timeout=2000)
            print(f"✓ Опция '{option_text}' кликнута")
        except Exception as e:
            print(f"? Клик по опции не удался: {e}")
            raise
        self.page.wait_for_timeout(500)

    def get_select_one_selected_text(self) -> str:
        try:
            value_container = self.select_one_container.locator("div[class*='singleValue']")
            if value_container.count() > 0 and value_container.is_visible():
                return value_container.text_content().strip()
        except:
            pass
        return ""

    # --- Old Style Select Menu ---
    def select_old_style_option_by_value(self, value: str):
        self.old_style_select.select_option(value)
        self.page.wait_for_timeout(500)

    def select_old_style_option_by_index(self, index: int):
        self.old_style_select.select_option(index=index)
        self.page.wait_for_timeout(500)

    def select_old_style_option_by_text(self, text: str):
        self.old_style_select.select_option(label=text)
        self.page.wait_for_timeout(500)

    def get_old_style_select_selected_value(self) -> str:
        return self.old_style_select.input_value()

    def get_old_style_select_options_count(self) -> int:
        return self.old_style_select_options.count()

    def get_old_style_select_options_text(self) -> list:
        options = []
        count = self.old_style_select_options.count()
        for i in range(count):
            option_text = self.old_style_select_options.nth(i).text_content().strip()
            if option_text:
                options.append(option_text)
        return options

    # --- Multiselect ---
    def open_multiselect_dropdown(self):
        print("Попытка открыть dropdown Multiselect...")
        try:
            self.multiselect_input.scroll_into_view_if_needed()
        except:
            pass

        try:
            self.multiselect_indicator.click(force=True, timeout=2000)
            print("✓ Клик по индикатору Multiselect")
        except Exception as e1:
            print(f"? Клик по индикатору не удался: {e1}")
            try:
                self.multiselect_input.click(force=True, timeout=2000)
                print("✓ Клик по Input Multiselect (force)")
            except Exception as e2:
                print(f"? Клик по Input тоже не удался: {e2}")
                raise Exception(f"Не удалось открыть Multiselect: {e1}, {e2}")

        self.page.wait_for_timeout(500)
        print("✓ Dropdown Multiselect, вероятно, открыт")

    def select_option_in_multiselect(self, option_text: str):
        # Ищем опцию сразу
        option_locator = self.page.locator(SelectMenuLocators.DROPDOWN_OPTION).filter(has_text=option_text)
        if option_locator.count() == 0 or not option_locator.first.is_visible():
            option_locator = self.page.locator(SelectMenuLocators.DROPDOWN_OPTION).filter(
                has_text=re.compile(f".*{re.escape(option_text)}.*", re.IGNORECASE))

        if option_locator.count() > 0 and option_locator.first.is_visible():
            option_to_click = option_locator.first
            print(f"✓ Опция '{option_text}' найдена")
        else:
            any_option = self.page.locator(SelectMenuLocators.DROPDOWN_OPTION).first
            if any_option.count() > 0 and any_option.is_visible():
                option_to_click = any_option
                print(f"~ Выбираем первую доступную опцию, так как '{option_text}' не найдена точно")
            else:
                raise Exception(f"Опция '{option_text}' и другие опции не найдены или не видимы")

        try:
            option_to_click.click(force=True, timeout=2000)
            print(f"✓ Опция '{option_text}' кликнута")
        except Exception as e:
            print(f"? Клик по опции не удался: {e}")
            raise
        self.page.wait_for_timeout(500)

    # --- Standard Multi Select ---
    def select_standard_multi_select_option_by_index(self, index: int):
        self.standard_multi_select.select_option(index=index)
        self.page.wait_for_timeout(500)

    def select_standard_multi_select_option_by_value(self, value: str):
        self.standard_multi_select.select_option(value)
        self.page.wait_for_timeout(500)

    def get_standard_multi_select_selected_values(self) -> list:
        selected_options = self.standard_multi_select.locator("option:checked")
        values = []
        count = selected_options.count()
        for i in range(count):
            value = selected_options.nth(i).get_attribute("value")
            if value:
                values.append(value)
        return values

    # --- Вспомогательные ---
    def is_page_loaded(self) -> bool:
        try:
            return self.main_container.is_visible()
        except:
            return False

    def get_all_selects_count(self) -> int:
        try:
            return (1 if self.old_style_select.count() > 0 else 0) + \
                (1 if self.standard_multi_select.count() > 0 else 0) + \
                (1 if self.select_value_container.locator("div[class*='control']").count() > 0 else 0) + \
                (1 if self.select_one_container.locator("div[class*='control']").count() > 0 else 0) + \
                (1 if self.multiselect_input.count() > 0 else 0)
        except:
            return 0
