# tests/test_select_menu.py
import pytest
import re  # Для частичного совпадения текста


def test_1_select_menu_page_loads(select_menu_page):
    current_url = select_menu_page.page.url
    assert "select-menu" in current_url
    assert select_menu_page.is_page_loaded()
    select_count = select_menu_page.get_all_selects_count()
    assert select_count >= 4
    print(f"✓ Страница загружена, найдено {select_count} select элементов")


def test_2_select_value_functionality(select_menu_page):
    assert select_menu_page.select_value_container.get_attribute("id") == "withOptGroup"
    print("✓ Локатор select_value_container корректен")

    # Открываем и проверяем опции
    select_menu_page.open_select_value_dropdown()
    expected_options = [
        "Group 1, option 1",
        "Group 1, option 2",
        "Group 2, option 1",
        "Group 2, option 2",
        "Another root option",
    ]
    found_options = []
    for option_text in expected_options:
        option_locator = select_menu_page.page.locator("div[class*='option']").filter(
            has_text=option_text
        )
        if option_locator.count() > 0 and option_locator.first.is_visible():
            found_options.append(option_text)
    print(f"✓ Найдены опции Select Value: {found_options}")
    assert len(found_options) > 0

    # Выбираем опцию
    if found_options:
        option_to_select = found_options[0]
        select_menu_page.select_option_in_select_value(option_to_select)
        selected_value = select_menu_page.get_select_value_selected_text()
        assert len(selected_value) > 0
        print(f"✓ Выбрана опция '{option_to_select}', значение: '{selected_value}'")


def test_3_select_one_functionality(select_menu_page):
    assert select_menu_page.select_one_container.get_attribute("id") == "selectOne"
    print("✓ Локатор select_one_container корректен")
    assert select_menu_page.select_one_container.is_visible()
    print("✓ Контейнер Select One видим")

    # Открываем и проверяем опции
    select_menu_page.open_select_one_dropdown()
    expected_options = ["Dr.", "Mr.", "Ms.", "Mrs.", "Prof.", "Other"]
    found_options = []
    for option_text in expected_options:
        option_locator = select_menu_page.page.locator("div[class*='option']").filter(
            has_text=option_text
        )
        if option_locator.count() > 0 and option_locator.first.is_visible():
            found_options.append(option_text)
    print(f"✓ Найдены опции Select One: {found_options}")
    assert len(found_options) > 0

    # Выбираем опцию
    if found_options:
        option_to_select = found_options[0]
        select_menu_page.select_option_in_select_one(option_to_select)
        selected_value = select_menu_page.get_select_one_selected_text()
        assert len(selected_value) > 0
        print(f"✓ Выбрана опция '{option_to_select}', значение: '{selected_value}'")


def test_4_old_style_select_menu_functionality(select_menu_page):
    assert select_menu_page.old_style_select.get_attribute("id") == "oldSelectMenu"
    print("✓ Локатор old_style_select корректен")

    options_count = select_menu_page.get_old_style_select_options_count()
    assert options_count > 0
    print(f"✓ Найдено {options_count} опций в Old Style Select")

    options_text = select_menu_page.get_old_style_select_options_text()
    assert len(options_text) > 0
    print(f"✓ Тексты опций: {options_text[:3]}...")

    if len(options_text) > 1:
        initial_value = select_menu_page.get_old_style_select_selected_value()
        print(f"~ Начальное значение: '{initial_value}'")
        select_menu_page.select_old_style_option_by_index(1)
        selected_value = select_menu_page.get_old_style_select_selected_value()
        assert len(selected_value) > 0
        print(f"✓ Выбрана опция по индексу 1, значение: '{selected_value}'")


def test_5_multiselect_drop_down_functionality(select_menu_page):
    """Тест 5: Функциональность Multiselect drop down."""
    # select_menu_page.page.wait_for_timeout(2000) # Страница уже загружена
    # Проверяем, что локатор указывает на правильный элемент
    assert (
        select_menu_page.multiselect.get_attribute("id") == "cars"
    ), "Локатор multiselect должен указывать на #cars"
    print("✓ Локатор multiselect корректен")
    assert select_menu_page.multiselect.is_visible(), "Multiselect должен быть видим"
    print("✓ Multiselect видим")

    options_count = select_menu_page.multiselect_options.count()
    assert options_count > 0, "В Multiselect должно быть больше 0 опций"
    print(f"✓ Найдено {options_count} опций в Multiselect")

    # --- Изменено: Выбор 2 опций ---
    if options_count > 2:
        # Сохраняем начальные значения
        initial_values = select_menu_page.get_multiselect_selected_values()
        print(f"~ Начальные выбранные значения: {initial_values}")

        # Выбираем первую опцию
        select_menu_page.select_multiselect_option_by_index(1)
        # Выбираем вторую опцию
        select_menu_page.select_multiselect_option_by_index(2)

        selected_values = select_menu_page.get_multiselect_selected_values()
        assert len(selected_values) >= 2, "Должно быть выбрано хотя бы два значения"
        print(f"✓ Выбраны опции по индексам 1 и 2, значения: {selected_values}")


def test_6_standard_multi_select_functionality(select_menu_page):
    """Тест 6: Функциональность Standard multi select (React)."""
    # select_menu_page.page.wait_for_timeout(3000) # Страница уже загружена
    # Проверяем, что локатор указывает на правильный контейнер
    select_menu_container = select_menu_page.page.locator("#selectMenuContainer")
    assert (
        select_menu_container.count() > 0
    ), "Контейнер #selectMenuContainer должен существовать"
    assert (
        select_menu_container.is_visible()
    ), "Контейнер #selectMenuContainer должен быть видим"
    print("✓ Контейнер Standard Multi Select (#selectMenuContainer) существует и видим")

    # Открытие dropdown критично
    select_menu_page.open_standard_multi_select_dropdown()
    select_menu_page.page.wait_for_timeout(1500)

    # Попробуем найти опции.
    potential_options = [
        "Group 1, option 1",
        "Group 2, option 1",
        "Aqua",
        "Blue",
        "Green",
        "Red",
    ]
    found_options = []
    for option_text in potential_options:
        option_locator = select_menu_page.page.locator(
            f"div[class*='option']:has-text('{option_text}')"
        )
        if option_locator.count() > 0 and option_locator.first.is_visible():
            found_options.append(option_text)
    print(
        f"✓ Найдено {len(found_options)} потенциальных опций в Standard Multi Select dropdown: {found_options}"
    )

    # Утверждение: хотя бы две опции должны быть найдены
    assert (
        len(found_options) >= 2
    ), f"В dropdown Standard Multi Select должны быть как минимум 2 опции из {potential_options}"

    # --- Изменено: Выбор 2 опций ---
    if len(found_options) >= 2:
        option_to_select_1 = found_options[0]
        option_to_select_2 = found_options[1]

        select_menu_page.select_option_in_standard_multi_select(option_to_select_1)
        print(f"✓ Опция '{option_to_select_1}' выбрана в Standard Multi Select")

        # Пауза между выборами, если необходимо
        select_menu_page.page.wait_for_timeout(500)

        select_menu_page.select_option_in_standard_multi_select(option_to_select_2)
        print(f"✓ Опция '{option_to_select_2}' выбрана в Standard Multi Select")

        # Проверим, что значения добавились
        selected_values = select_menu_page.get_standard_multi_select_selected_values()
        assert len(selected_values) >= 2, "Должно быть выбрано хотя бы два значения"
        assert (
            option_to_select_1 in selected_values
        ), f"Выбранное значение '{option_to_select_1}' должно быть в списке"
        assert (
            option_to_select_2 in selected_values
        ), f"Выбранное значение '{option_to_select_2}' должно быть в списке"
        print(f"✓ Выбранные значения: {selected_values}")
