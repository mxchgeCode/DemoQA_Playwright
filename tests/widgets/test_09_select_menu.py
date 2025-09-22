"""
Тесты для страницы Select Menu.
Проверяет функциональность различных типов выпадающих меню.
"""

import pytest
import allure
import time
from pages.widgets.select_menu_page import SelectMenuPage
from locators.widgets.selectmenu_locators import SelectMenuLocators


@allure.epic("Widgets")
@allure.feature("Select Menu")
@allure.story("Basic Selection")
@pytest.mark.widgets
@pytest.mark.smoke
def test_select_option_via_persistent_control(select_menu_page: SelectMenuPage):
    """
    Тест базового выбора опции в первом dropdown меню.

    Шаги:
    1. Проверить видимость контрола
    2. Открыть dropdown
    3. Выбрать первую доступную опцию
    4. Проверить отображение выбранного значения
    """
    with allure.step("Проверяем видимость dropdown контрола"):
        container = select_menu_page.page.locator(SelectMenuLocators.CONTAINER)
        dropdown_control = container.locator(SelectMenuLocators.DROPDOWN_CONTROL)

        assert dropdown_control.is_visible(), "Dropdown control должен быть видим"

    with allure.step("Получаем начальное состояние"):
        selected_text_locator = container.locator(
            SelectMenuLocators.SELECT_ONE_DISPLAY_TEXT
        )
        initial_text = selected_text_locator.text_content().strip()

        assert initial_text, "Текст выбранного значения должен присутствовать"
        allure.attach(initial_text, "initial_selection")

    with allure.step("Открываем dropdown и выбираем первую опцию"):
        dropdown_control.click()
        select_menu_page.page.wait_for_timeout(200)

        # Нажимаем Enter чтобы выбрать первую опцию
        container.press("Enter")
        select_menu_page.page.wait_for_timeout(500)

    with allure.step("Проверяем результат выбора"):
        selected_text = selected_text_locator.text_content().strip()
        expected_text = "Group 1, option 1"

        assert (
            selected_text == expected_text
        ), f"Ожидаем '{expected_text}', получено '{selected_text}'"

        allure.attach(selected_text, "final_selection")
        time.sleep(1)  # Пауза для наблюдения


@allure.epic("Widgets")
@allure.feature("Select Menu")
@allure.story("Title Selection")
@pytest.mark.widgets
def test_select_title_option(select_menu_page: SelectMenuPage):
    """
    Тест выбора опции Title.

    Проверяет функциональность выбора конкретной опции из dropdown.
    """
    with allure.step("Проверяем начальное состояние Select One"):
        initial_text = select_menu_page.get_select_one_display_text()
        expected_initial = "Select Title"

        assert (
            initial_text == expected_initial
        ), f"Начальный текст должен быть '{expected_initial}', получено '{initial_text}'"
        allure.attach(initial_text, "initial_state")

    with allure.step("Выбираем опцию Mrs."):
        select_menu_page.select_one_control.click()
        select_menu_page.select_option_in_dropdown("Mrs.")
        select_menu_page.page.wait_for_timeout(500)

    with allure.step("Проверяем успешный выбор"):
        selected_text = select_menu_page.get_select_one_display_text()
        expected_selection = "Mrs."

        assert (
            selected_text == expected_selection
        ), f"Ожидается '{expected_selection}', получено '{selected_text}'"

        allure.attach(selected_text, "selected_title")
        time.sleep(1)


@allure.epic("Widgets")
@allure.feature("Select Menu")
@allure.story("Old Style Select")
@pytest.mark.widgets
def test_old_style_select_menu_functionality(select_menu_page: SelectMenuPage):
    """
    Тест функциональности стандартного HTML select элемента.

    Проверяет работу с классическим HTML select меню.
    """
    with allure.step("Проверяем корректность селектора старого стиля"):
        simple_select = select_menu_page.simple_select
        select_id = simple_select.get_attribute("id")

        assert (
            select_id == "oldSelectMenu"
        ), f"Локатор должен быть #oldSelectMenu, получен #{select_id}"
        allure.attach(select_id, "select_element_id")

    with allure.step("Получаем количество доступных опций"):
        options_count = select_menu_page.get_simple_select_options_count()

        assert options_count > 1, f"Должно быть больше 1 опции, найдено {options_count}"
        allure.attach(str(options_count), "available_options_count")

    with allure.step("Тестируем выбор опции по индексу"):
        if options_count > 1:
            initial_value = select_menu_page.get_simple_select_selected_value()

            # Выбираем вторую опцию (индекс 1)
            select_menu_page.select_simple_option_by_index(1)
            selected_value = select_menu_page.get_simple_select_selected_value()

            assert len(selected_value) > 0, "Должно быть выбрано значение"
            assert (
                selected_value != initial_value
            ), "Выбранное значение должно отличаться от начального"

            selection_result = {
                "initial_value": initial_value,
                "selected_value": selected_value,
                "selection_changed": selected_value != initial_value,
            }
            allure.attach(str(selection_result), "selection_change_result")

        time.sleep(1)


@allure.epic("Widgets")
@allure.feature("Select Menu")
@allure.story("Multiselect Placeholder")
@pytest.mark.widgets
def test_multiselect_placeholder(select_menu_page: SelectMenuPage):
    """
    Тест отображения placeholder в мультиселекте.

    Проверяет начальное состояние multiselect элемента.
    """
    with allure.step("Проверяем placeholder мультиселекта"):
        placeholder = select_menu_page.multiselect_get_placeholder()
        expected_placeholder = "Select..."

        assert (
            placeholder == expected_placeholder
        ), f"Ожидаемый placeholder '{expected_placeholder}', получено '{placeholder}'"

        allure.attach(placeholder, "multiselect_placeholder")


@allure.epic("Widgets")
@allure.feature("Select Menu")
@allure.story("Multiple Selection")
@pytest.mark.widgets
@pytest.mark.regression
def test_select_multiple_options(select_menu_page: SelectMenuPage):
    """
    Тест выбора нескольких опций в стандартном multiselect.

    Проверяет функциональность множественного выбора.
    """
    options_to_select = ["volvo", "saab", "opel", "audi"]

    with allure.step(f"Выбираем множественные опции: {options_to_select}"):
        select_menu_page.select_standard_multiselect_options(options_to_select)

    with allure.step("Проверяем что все опции выбраны"):
        selected = select_menu_page.get_selected_standard_multiselect_options()

        assert set(selected) == set(
            options_to_select
        ), f"Ожидались: {options_to_select}, выбраны: {selected}"

        allure.attach(str(selected), "selected_multiple_options")
        time.sleep(1)


@allure.epic("Widgets")
@allure.feature("Select Menu")
@allure.story("Clear Selection")
@pytest.mark.widgets
def test_deselect_all_options(select_menu_page: SelectMenuPage):
    """
    Тест очистки всех выбранных опций в multiselect.

    Шаги:
    1. Выбрать несколько опций
    2. Очистить все выборы
    3. Проверить что список выбранных опций пустой
    """
    options_to_select = ["volvo", "saab", "opel", "audi"]

    with allure.step("Сначала выбираем несколько опций"):
        select_menu_page.select_standard_multiselect_options(options_to_select)
        initial_selected = select_menu_page.get_selected_standard_multiselect_options()

        assert len(initial_selected) > 0, "Должны быть выбранные опции перед очисткой"
        allure.attach(str(initial_selected), "options_before_clearing")

    with allure.step("Очищаем все выбранные опции"):
        select_menu_page.clear_standard_multiselect_selection()

    with allure.step("Проверяем что все опции сняты с выбора"):
        selected_after_clear = (
            select_menu_page.get_selected_standard_multiselect_options()
        )

        assert (
            selected_after_clear == []
        ), f"После очистки ожидался пустой список, получили: {selected_after_clear}"

        allure.attach(str(selected_after_clear), "options_after_clearing")
        time.sleep(1)


@allure.epic("Widgets")
@allure.feature("Select Menu")
@allure.story("Advanced Multiselect")
@pytest.mark.widgets
@pytest.mark.regression
def test_multiselect_select_and_remove_options(select_menu_page: SelectMenuPage):
    """
    Тест продвинутого мультиселекта с добавлением и удалением опций.

    Проверяет полный цикл: выбор, отображение, удаление опций.
    """
    options = ["Blue", "Black", "Green", "Red"]

    with allure.step(f"Выбираем опции в продвинутом мультиселекте: {options}"):
        select_menu_page.multiselect_open()  # Открываем меню один раз

        for option in options:
            with allure.step(f"Выбираем опцию: {option}"):
                option_locator = select_menu_page.page.locator(
                    f"{SelectMenuLocators.DROPDOWN_MENU} >> text='{option}'"
                ).first

                # Ждем видимости опции и кликаем
                option_locator.wait_for(state="visible", timeout=7000)
                option_locator.click(force=True)
                select_menu_page.page.wait_for_timeout(300)

                allure.attach(f"Selected: {option}", f"option_selection_{option}")

    with allure.step("Закрываем меню кликом вне области"):
        select_menu_page.page.mouse.click(0, 0)  # Клик в левый верхний угол

    with allure.step("Проверяем что все опции выбраны"):
        selected = select_menu_page.multiselect_get_selected_options()

        for option in options:
            assert (
                option in selected
            ), f"Опция '{option}' должна быть выбрана, выбранные: {selected}"

        allure.attach(str(selected), "all_selected_options")

    with allure.step("Удаляем каждую выбранную опцию"):
        for option in options:
            with allure.step(f"Удаляем опцию: {option}"):
                select_menu_page.multiselect_remove_selected_options(option)

                # Проверяем промежуточное состояние
                current_selected = select_menu_page.multiselect_get_selected_options()
                allure.attach(
                    f"After removing {option}: {current_selected}",
                    f"after_removing_{option}",
                )

    with allure.step("Проверяем что все опции удалены"):
        selected_after_removal = select_menu_page.multiselect_get_selected_options()

        assert (
            not selected_after_removal
        ), f"После удаления всех опций список не пустой: {selected_after_removal}"

        allure.attach("All options successfully removed", "final_removal_result")


@allure.epic("Widgets")
@allure.feature("Select Menu")
@allure.story("Dropdown Interaction")
@pytest.mark.widgets
@pytest.mark.parametrize(
    "dropdown_type,test_value",
    [
        ("select_one", "Dr."),
        ("select_value", "Group 2, option 1"),
        ("old_style", "2"),
    ],
)
def test_different_dropdown_types(
    select_menu_page: SelectMenuPage, dropdown_type, test_value
):
    """
    Параметризованный тест различных типов dropdown меню.

    Проверяет консистентность поведения разных типов селекторов.
    """
    with allure.step(f"Тестируем {dropdown_type} dropdown с значением {test_value}"):
        if dropdown_type == "select_one":
            select_menu_page.select_one_control.click()
            select_menu_page.select_option_in_dropdown(test_value)

            result = select_menu_page.get_select_one_display_text()
            assert (
                test_value in result
            ), f"Выбранное значение должно содержать '{test_value}'"

        elif dropdown_type == "old_style":
            select_menu_page.select_simple_option_by_index(int(test_value))
            result = select_menu_page.get_simple_select_selected_value()
            assert result is not None, "Должно быть выбрано значение в old style select"

        allure.attach(f"Test completed for {dropdown_type}", "dropdown_test_result")
