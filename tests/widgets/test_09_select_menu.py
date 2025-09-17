import time
from pages.widgets.select_menu_page import SelectMenuPage
from locators.widgets.select_menu_locators import SelectMenuLocators


def test_select_option_via_persistent_control(select_menu_page: SelectMenuPage):
    container = select_menu_page.page.locator(SelectMenuLocators.CONTAINER)
    dropdown_control = container.locator(SelectMenuLocators.DROPDOWN_CONTROL)
    assert dropdown_control.is_visible(), "Dropdown control должен быть видим"
    selected_text_locator = container.locator(
        SelectMenuLocators.SELECT_ONE_DISPLAY_TEXT
    )
    initial_text = selected_text_locator.text_content().strip()
    assert initial_text, "Текст выбранного значения отсутствует"
    dropdown_control.click()
    select_menu_page.page.wait_for_timeout(200)
    container.press("Enter")
    select_menu_page.page.wait_for_timeout(500)
    selected_text = selected_text_locator.text_content().strip()
    assert (
        selected_text == "Group 1, option 1"
    ), f"Ожидаем выбранное 'Group 1, option 1', получено '{selected_text}'"
    time.sleep(2)


def test_select_title_option(select_menu_page: SelectMenuPage):
    initial_text = select_menu_page.get_select_one_display_text()
    assert (
        initial_text == "Select Title"
    ), f"Начальный текст должен быть 'Select Title', получено '{initial_text}'"
    select_menu_page.select_one_control.click()
    select_menu_page.select_option_in_dropdown("Mrs.")
    select_menu_page.page.wait_for_timeout(500)
    selected_text = select_menu_page.get_select_one_display_text()
    assert (
        selected_text == "Mrs."
    ), f"Ожидается выбранное 'Mrs.', получено '{selected_text}'"
    time.sleep(2)


def test_4_old_style_select_menu_functionality(select_menu_page: SelectMenuPage):
    simple_select = select_menu_page.simple_select
    assert (
        simple_select.get_attribute("id") == "oldSelectMenu"
    ), "Локатор должен быть #oldSelectMenu"
    options_count = select_menu_page.get_simple_select_options_count()
    if options_count > 1:
        initial_value = select_menu_page.get_simple_select_selected_value()
        select_menu_page.select_simple_option_by_index(1)
        selected_value = select_menu_page.get_simple_select_selected_value()
        assert len(selected_value) > 0, "Должно быть выбрано значение"
        assert (
            selected_value != initial_value
        ), "Выбранное значение должно отличаться от начального"
    time.sleep(2)


def test_multiselect_placeholder(select_menu_page: SelectMenuPage):
    placeholder = select_menu_page.multiselect_get_placeholder()
    assert (
        placeholder == "Select..."
    ), f"Ожидаемый placeholder 'Select...', получено '{placeholder}'"


def test_select_multiple_options(select_menu_page: SelectMenuPage):
    options_to_select = ["volvo", "saab", "opel", "audi"]
    select_menu_page.select_standard_multiselect_options(options_to_select)
    selected = select_menu_page.get_selected_standard_multiselect_options()
    assert set(selected) == set(
        options_to_select
    ), f"Ожидались: {options_to_select}, выбраны: {selected}"
    time.sleep(2)


def test_deselect_all_options(select_menu_page: SelectMenuPage):
    options_to_select = ["volvo", "saab", "opel", "audi"]
    select_menu_page.select_standard_multiselect_options(options_to_select)
    select_menu_page.clear_standard_multiselect_selection()
    selected = select_menu_page.get_selected_standard_multiselect_options()
    assert (
        selected == []
    ), f"После удаления выбранных опций ожидался пустой список, получили: {selected}"
    time.sleep(2)


def test_multiselect_select_and_remove_options(select_menu_page: SelectMenuPage):
    options = ["Blue", "Black", "Green", "Red"]
    select_menu_page.multiselect_open()  # открыть меню один раз

    for option in options:
        print(f"Selecting option {option}")  # для логирования
        option_locator = select_menu_page.page.locator(
            f"{SelectMenuLocators.DROPDOWN_MENU} >> text='{option}'"
        ).first
        option_locator.wait_for(state="visible", timeout=7000)
        option_locator.click(force=True)
        select_menu_page.page.wait_for_timeout(300)

    select_menu_page.page.mouse.click(0, 0)  # закрыть меню кликом вне

    selected = select_menu_page.multiselect_get_selected_options()
    for option in options:
        assert (
            option in selected
        ), f"Опция '{option}' должна быть выбрана, выбранные: {selected}"

    for option in options:
        select_menu_page.multiselect_remove_selected_options(option)
    selected_after_removal = select_menu_page.multiselect_get_selected_options()
    assert (
        not selected_after_removal
    ), f"После удаления опций список не пустой: {selected_after_removal}"
