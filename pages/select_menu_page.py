# pages/select_menu_page.py
from playwright.sync_api import Page
from locators.select_menu_locators import SelectMenuLocators


class SelectMenuPage:
    def __init__(self, page: Page):
        self.page = page
        # Основные элементы
        self.main_container = page.locator(SelectMenuLocators.MAIN_CONTAINER)

        # Select Value (Simple Select Menu) - Это обычный <select>
        self.simple_select = page.locator(SelectMenuLocators.SELECT_VALUE)
        self.simple_select_options = page.locator(SelectMenuLocators.SELECT_VALUE_OPTIONS)

        # Select One (React select) - React компонент
        self.select_one_container = page.locator(SelectMenuLocators.SELECT_ONE_CONTAINER)
        self.select_one_control = page.locator(SelectMenuLocators.SELECT_ONE_CONTROL)
        self.select_one_input = page.locator(SelectMenuLocators.SELECT_ONE_INPUT)

        # Old Style Select Menu - Это тот же самый <select>, что и Select Value
        self.old_style_select = page.locator(SelectMenuLocators.OLD_STYLE_SELECT)
        self.old_style_select_options = page.locator(SelectMenuLocators.OLD_STYLE_SELECT_OPTIONS)

        # Multiselect drop down (React) - React компонент
        self.multiselect = page.locator(SelectMenuLocators.MULTISELECT)
        self.multiselect_options = page.locator(SelectMenuLocators.MULTISELECT_OPTIONS)

        # Standard multi select (обычный select multiple) - Это тот же самый <select>, что и multiselect
        # Он имеет тот же ID, что и multiselect! Это один и тот же элемент на странице.
        # Поэтому мы используем тот же локатор, что и для multiselect.
        self.standard_multi_select = page.locator(SelectMenuLocators.STANDARD_MULTI_SELECT)
        self.standard_multi_select_options = page.locator(SelectMenuLocators.STANDARD_MULTI_SELECT_OPTIONS)

        # Общие элементы для dropdown (используются внутри контейнеров)
        self.dropdown_option = page.locator(SelectMenuLocators.DROPDOWN_OPTION)
        self.dropdown_menu = page.locator(SelectMenuLocators.DROPDOWN_MENU)

    # --- Вспомогательный метод ожидания ---
    def _wait_for_element_visible(self, locator, timeout=10000, description="Элемент"):
        """Универсальный метод ожидания видимости элемента."""
        try:
            locator.wait_for(state="visible", timeout=timeout)
            print(f"✓ {description} стал видимым")
            return True
        except Exception as e:
            print(f"Х {description} не стал видимым в течение {timeout}мс: {e}")
            return False

    # --- Simple Select Menu (Select Value) ---
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

    def get_simple_select_selected_text(self) -> str:
        selected_option = self.simple_select.locator("option:checked")
        return selected_option.text_content().strip() if selected_option.count() > 0 else ""

    def get_simple_select_options_count(self) -> int:
        return self.simple_select_options.count()

    def get_simple_select_options_text(self) -> list:
        options = []
        count = self.simple_select_options.count()
        for i in range(count):
            option_text = self.simple_select_options.nth(i).text_content().strip()
            if option_text:
                options.append(option_text)
        return options

    # --- Select One (React select) ---
    def open_select_one_dropdown(self):
        """Открывает dropdown для Select One."""
        print("Попытка открыть dropdown Select One...")
        # 1. Убедиться, что контейнер видим
        if not self._wait_for_element_visible(self.select_one_container, 10000, "Контейнер Select One"):
            raise Exception("Контейнер Select One не стал видимым")
        # 2. Найти элемент управления
        control_locator = self.select_one_control
        if not self._wait_for_element_visible(control_locator, 5000, "Элемент управления Select One"):
            raise Exception("Элемент управления Select One не найден или не видим")

        # 3. Прокрутить в область видимости
        try:
            control_locator.scroll_into_view_if_needed()
            print("✓ Элемент управления Select One прокручен в видимую область")
        except Exception as e:
            print(f"? Ошибка прокрутки элемента управления Select One: {e}")

        # 4. Кликнуть
        try:
            control_locator.click(force=False)
            print("✓ Клик по элементу управления Select One (обычный)")
        except Exception as e1:
            print(f"? Обычный клик не удался: {e1}")
            try:
                control_locator.click(force=True)
                print("✓ Клик по элементу управления Select One (force)")
            except Exception as e2:
                print(f"? Force-клик не удался: {e2}")
                try:
                    bbox = control_locator.bounding_box()
                    if bbox:
                        self.page.mouse.click(bbox['x'] + bbox['width'] / 2, bbox['y'] + bbox['height'] / 2)
                        print("✓ Клик по элементу управления Select One (JS через mouse)")
                    else:
                        raise Exception("Не удалось получить координаты для JS клика")
                except Exception as e3:
                    print(f"? JS-клик не удался: {e3}")
                    raise Exception(
                        f"Не удалось кликнуть по элементу управления Select One всеми способами: {e1}, {e2}, {e3}")

        # 5. Подождать, пока dropdown появится (проверим наличие меню внутри контейнера)
        select_one_menu = self.select_one_container.locator(SelectMenuLocators.DROPDOWN_MENU)
        if self._wait_for_element_visible(select_one_menu, 5000, "Dropdown меню Select One"):
            print("✓ Dropdown Select One открыт")
        else:
            print("? Dropdown Select One, возможно, открыт, но меню не обнаружено")

    def select_option_in_select_one(self, option_text: str):
        """Выбирает опцию в Select One по тексту."""
        # Открываем dropdown
        self.open_select_one_dropdown()
        # Небольшая пауза, чтобы опции точно отрендерились
        self.page.wait_for_timeout(1000)

        # Ищем опцию строго внутри меню Select One
        select_one_menu = self.select_one_container.locator(SelectMenuLocators.DROPDOWN_MENU)
        option_locator = select_one_menu.locator(f"div[class*='option']:has-text('{option_text}')")
        if option_locator.count() > 0 and option_locator.first.is_visible():
            option_to_click = option_locator.first
            print(f"✓ Опция '{option_text}' найдена по точному совпадению")
        else:
            # Пробуем частичное совпадение
            option_locator_partial = select_one_menu.locator(
                f"div[class*='option']:text-matches('(?i).*{option_text}.*')")
            if option_locator_partial.count() > 0 and option_locator_partial.first.is_visible():
                option_to_click = option_locator_partial.first
                print(f"✓ Опция '{option_text}' найдена по частичному совпадению")
            else:
                # Если не нашли, ищем первую доступную опцию в этом меню
                any_option = select_one_menu.locator(SelectMenuLocators.DROPDOWN_OPTION).first
                if any_option.count() > 0 and any_option.is_visible():
                    option_to_click = any_option
                    print(f"~ Выбираем первую доступную опцию, так как '{option_text}' не найдена")
                else:
                    raise Exception(f"Опция '{option_text}' и другие опции не найдены или не видимы")

        # Прокручиваем опцию в видимую область
        try:
            option_to_click.scroll_into_view_if_needed()
        except Exception as e:
            print(f"? Ошибка прокрутки опции: {e}")

        # Кликаем по опции
        try:
            option_to_click.click(force=False)
            print(f"✓ Опция '{option_text}' кликнута")
        except Exception as e:
            print(f"? Обычный клик по опции не удался: {e}")
            try:
                option_to_click.click(force=True)
                print(f"✓ Опция '{option_text}' кликнута (force)")
            except Exception as e2:
                print(f"? Force-клик по опции не удался: {e2}")
                raise Exception(f"Не удалось кликнуть по опции '{option_text}': {e}, {e2}")

        # Пауза после выбора
        self.page.wait_for_timeout(1000)

    def get_select_one_selected_text(self) -> str:
        """Получает текст выбранной опции в Select One."""
        try:
            # Ищем элемент с выбранным значением внутри контейнера.
            value_container = self.select_one_container.locator("div[class*='singleValue']")
            if value_container.count() > 0 and value_container.is_visible():
                text = value_container.text_content().strip()
                print(f"✓ Получено значение Select One из singleValue: '{text}'")
                return text
            else:
                # Альтернатива: попробовать получить текст из самого контрола, исключая стрелки и плейсхолдеры
                control_text = self.select_one_control.text_content().strip()
                # Простая эвристика: если текст не стандартный плейсхолдер и не пустой
                if control_text and control_text not in ["Select Option", "Select Title", ""]:
                    print(f"~ Получено значение Select One из контрола: '{control_text}'")
                    return control_text
                else:
                    print("? Значение Select One не определено или стандартное")
                    return ""
        except Exception as e:
            print(f"Х Ошибка получения значения Select One: {e}")
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

    # --- Multiselect drop down (React) ---
    def select_multiselect_option_by_index(self, index: int):
        # Для React-селекта используем стандартный метод select_option
        self.multiselect.select_option(index=index)
        self.page.wait_for_timeout(500)

    def select_multiselect_option_by_value(self, value: str):
        # Для React-селекта используем стандартный метод select_option
        self.multiselect.select_option(value)
        self.page.wait_for_timeout(500)

    def get_multiselect_selected_values(self) -> list:
        """Получает все выбранные значения из Multiselect drop down (React)."""
        values = []
        try:
            # Ищем элементы с выбранными значениями (теги)
            selected_value_elements = self.multiselect.locator("div[class*='multiValue']")
            count = selected_value_elements.count()
            for i in range(count):
                try:
                    element = selected_value_elements.nth(i)
                    # Текст может содержать '×' для удаления, убираем его
                    text = element.text_content().strip().rstrip('×').strip()
                    if text:
                        values.append(text)
                except Exception:
                    continue  # Игнорируем ошибки отдельных элементов
        except Exception as e:
            print(f"? Ошибка при получении выбранных значений Multiselect: {e}")
        return values

    # --- Standard multi select (обычный select multiple) ---
    def select_standard_multi_select_option_by_index(self, index: int):
        """Выбирает опцию в стандартном мульти-селекте по индексу."""
        # Это обычный <select multiple>, поэтому используем стандартный метод
        self.standard_multi_select.select_option(index=index)
        self.page.wait_for_timeout(500)

    def select_standard_multi_select_option_by_value(self, value: str):
        """Выбирает опцию в стандартном мульти-селекте по значению."""
        # Это обычный <select multiple>, поэтому используем стандартный метод
        self.standard_multi_select.select_option(value=value)
        self.page.wait_for_timeout(500)

    def get_standard_multi_select_selected_values(self) -> list:
        """Получает все выбранные значения из Standard Multi Select (обычный select)."""
        values = []
        try:
            # Получаем выбранные опции
            selected_options = self.standard_multi_select.locator("option:checked")
            count = selected_options.count()
            for i in range(count):
                value = selected_options.nth(i).get_attribute("value")
                if value:
                    values.append(value)
        except Exception as e:
            print(f"? Ошибка при получении выбранных значений Standard Multi Select: {e}")
        return values

    # --- Вспомогательные методы ---
    def is_page_loaded(self) -> bool:
        try:
            return self.main_container.is_visible()
        except:
            return False

    def get_all_selects_count(self) -> int:
        # Подсчитываем разные типы селектов
        # У нас есть 4 уникальных селекта: simple_select, select_one, multiselect, standard_multi_select
        # Но simple_select и old_style_select - это один и тот же элемент, поэтому считаем его только один раз.
        # select_one - это React-компонент, он считается отдельно.
        # multiselect и standard_multi_select - это один и тот же элемент (#cars), поэтому считаем его только один раз.
        try:
            simple_count = 1 if self.simple_select.count() > 0 else 0
            select_one_count = 1 if self.select_one_control.count() > 0 else 0
            # Для multiselect и standard_multi_select: они указывают на один и тот же элемент
            multiselect_count = 1 if self.multiselect.count() > 0 else 0
            return simple_count + select_one_count + multiselect_count
        except:
            return 0