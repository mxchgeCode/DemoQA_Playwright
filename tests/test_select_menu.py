# tests/test_select_menu.py
import pytest


def test_1_select_menu_page_loads(select_menu_page):
    """Тест 1: Страница Select Menu загружается корректно."""
    current_url = select_menu_page.page.url
    assert "select-menu" in current_url, "URL должен содержать 'select-menu'"
    assert select_menu_page.is_page_loaded(), "Страница должна быть загружена"
    select_count = select_menu_page.get_all_selects_count()
    # У нас 3 уникальных select элемента: simple_select (и old_style_select), select_one, multiselect (и standard_multi_select)
    assert select_count == 3, f"На странице должно быть 3 select элемента, найдено: {select_count}"
    print(f"✓ Страница загружена, найдено {select_count} select элементов")


# --- Тесты в порядке расположения на странице ---
def test_2_select_value_functionality(select_menu_page):
    """Тест 2: Функциональность Select Value (Simple Select Menu)."""
    # Проверяем, что локатор указывает на правильный элемент
    assert select_menu_page.simple_select.get_attribute(
        'id') == 'oldSelectMenu', "Локатор simple_select должен указывать на #oldSelectMenu"
    print("✓ Локатор simple_select корректен")

    options_count = select_menu_page.get_simple_select_options_count()
    assert options_count > 0, "В Select Value должно быть больше 0 опций"
    print(f"✓ Найдено {options_count} опций в Select Value")

    options_text = select_menu_page.get_simple_select_options_text()
    assert len(options_text) > 0, "Должны быть тексты опций"
    print(f"✓ Тексты опций: {options_text[:3]}...")

    if len(options_text) > 1:
        # Сохраняем начальное значение
        initial_value = select_menu_page.get_simple_select_selected_value()
        print(f"~ Начальное значение: '{initial_value}'")
        select_menu_page.select_simple_option_by_index(1)
        selected_text = select_menu_page.get_simple_select_selected_text()
        # Проверяем, что значение изменилось
        assert selected_text != options_text[0], "Выбранное значение должно отличаться от первого"
        assert len(selected_text) > 0, "Должно быть выбрано непустое значение"
        print(f"✓ Выбрана опция по индексу 1: '{selected_text}'")


def test_3_select_one_functionality(select_menu_page):
    """Тест 3: Функциональность Select One (React select)."""
    # Проверяем, что локатор указывает на правильный элемент
    assert select_menu_page.select_one_container.get_attribute(
        'id') == 'withOptGroup', "Локатор select_one_container должен указывать на #withOptGroup"
    print("✓ Локатор select_one_container корректен")

    # Проверка видимости контейнера критична
    assert select_menu_page.select_one_container.is_visible(), "Select One контейнер должен быть видим"
    print("✓ Контейнер Select One видим")

    # Открытие dropdown критично
    select_menu_page.open_select_one_dropdown()
    # Пауза после открытия
    select_menu_page.page.wait_for_timeout(1500)

    # Проверка наличия опций
    expected_options = ["Dr.", "Mr.", "Ms.", "Mrs.", "Prof.", "Other"]
    found_options = []
    # Ищем опции строго внутри контейнера Select One
    for option_text in expected_options:
        option_locator = select_menu_page.select_one_container.locator(f"div[class*='option']:has-text('{option_text}')")
        if option_locator.count() > 0 and option_locator.first.is_visible():
            found_options.append(option_text)
    print(f"✓ Найдены опции Select One: {found_options}")

    # Утверждение: хотя бы одна ожидаемая опция должна быть найдена
    assert len(found_options) > 0, f"В dropdown Select One должны быть опции из {expected_options}"

    # Выбор опции
    if len(found_options) > 0:
        option_to_select = found_options[0]
        select_menu_page.select_option_in_select_one(option_to_select)
        print(f"✓ Опция '{option_to_select}' выбрана в Select One")
        # Проверяем выбранное значение
        selected_value = select_menu_page.get_select_one_selected_text()
        assert len(selected_value) > 0, "Выбранное значение должно быть непустым"
        print(f"✓ Выбранное значение: '{selected_value}'")


def test_4_old_style_select_menu_functionality(select_menu_page):
    """Тест 4: Функциональность Old Style Select Menu."""
    # Проверяем, что локатор указывает на правильный элемент
    assert select_menu_page.old_style_select.get_attribute(
        'id') == 'oldSelectMenu', "Локатор old_style_select должен указывать на #oldSelectMenu"
    print("✓ Локатор old_style_select корректен (совпадает с simple_select)")

    options_count = select_menu_page.old_style_select_options.count()
    assert options_count > 0, "В Old Style Select должно быть больше 0 опций"
    print(f"✓ Найдено {options_count} опций в Old Style Select")

    options_text = []
    for i in range(min(options_count, 5)):
        option_text = select_menu_page.old_style_select_options.nth(i).text_content().strip()
        if option_text:
            options_text.append(option_text)
    assert len(options_text) > 0, "Должны быть тексты опций"
    print(f"✓ Тексты опций: {options_text[:3]}...")

    if len(options_text) > 1:
        initial_value = select_menu_page.get_old_style_select_selected_value()
        print(f"~ Начальное значение: '{initial_value}'")
        select_menu_page.select_old_style_option_by_index(1)
        selected_value = select_menu_page.get_old_style_select_selected_value()
        assert len(selected_value) > 0, "Должно быть выбрано значение"
        assert selected_value != initial_value, "Выбранное значение должно отличаться от начального"
        print(f"✓ Выбрана опция по индексу 1, значение: '{selected_value}'")


def test_5_multiselect_drop_down_functionality(select_menu_page):
    """Тест 5: Функциональность Multiselect drop down (React)."""
    # Проверяем, что локатор указывает на правильный элемент
    assert select_menu_page.multiselect.get_attribute('id') == 'cars', "Локатор multiselect должен указывать на #cars"
    print("✓ Локатор multiselect корректен")
    assert select_menu_page.multiselect.is_visible(), "Multiselect должен быть видим"
    print("✓ Multiselect видим")

    options_count = select_menu_page.multiselect_options.count()
    assert options_count > 0, "В Multiselect должно быть больше 0 опций"
    print(f"✓ Найдено {options_count} опций в Multiselect")

    # Выбор одной опции
    if options_count > 0:
        select_menu_page.select_multiselect_option_by_index(0)
        selected_values = select_menu_page.get_multiselect_selected_values()
        assert len(selected_values) > 0, "Должно быть выбрано хотя бы одно значение"
        print(f"✓ Выбрана опция, значения: {selected_values}")


def test_6_standard_multi_select_functionality(select_menu_page):
    """Тест 6: Функциональность Standard multi select (обычный select multiple)."""
    # Проверяем, что локатор указывает на правильный элемент
    assert select_menu_page.standard_multi_select.get_attribute('id') == 'cars', "Локатор standard_multi_select должен указывать на #cars"
    print("✓ Локатор standard_multi_select корректен")
    assert select_menu_page.standard_multi_select.is_visible(), "Standard multi select должен быть видим"
    print("✓ Standard multi select видим")

    options_count = select_menu_page.standard_multi_select_options.count()
    assert options_count > 0, "В Standard multi select должно быть больше 0 опций"
    print(f"✓ Найдено {options_count} опций в Standard multi select")

    # Выбор двух опций
    if options_count >= 2:
        select_menu_page.select_standard_multi_select_option_by_index(0)
        select_menu_page.select_standard_multi_select_option_by_index(1)
        selected_values = select_menu_page.get_standard_multi_select_selected_values()
        assert len(selected_values) >= 2, "Должно быть выбрано хотя бы два значения"
        print(f"✓ Выбраны опции, значения: {selected_values}")