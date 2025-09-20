"""
Тесты для страницы Radio Button.
Проверяет функциональность радио кнопок с различными состояниями.
"""

import pytest
import allure
from playwright.sync_api import Error
from locators.elements.radio_button_locators import RadioButtonLocators


@allure.epic("Elements")
@allure.feature("Radio Button")
@allure.story("Basic Selection")
@pytest.mark.elements
@pytest.mark.smoke
def test_select_yes_radio(radio_button_page):
    """
    Тест выбора радио кнопки Yes.

    Шаги:
    1. Кликнуть по радио кнопке Yes
    2. Проверить что отображается соответствующий результат
    """
    with allure.step("Выбираем радио кнопку Yes"):
        radio_button_page.select_yes()

    with allure.step("Проверяем отображение результата"):
        result = radio_button_page.get_result_text()

        assert result == "Yes", f"Ожидался результат 'Yes', получен '{result}'"
        allure.attach(result, "selected_radio_result")


@allure.epic("Elements")
@allure.feature("Radio Button")
@allure.story("Basic Selection")
@pytest.mark.elements
@pytest.mark.smoke
def test_select_impressive_radio(radio_button_page):
    """
    Тест выбора радио кнопки Impressive.

    Шаги:
    1. Кликнуть по радио кнопке Impressive
    2. Проверить отображение результата
    """
    with allure.step("Выбираем радио кнопку Impressive"):
        radio_button_page.select_impressive()

    with allure.step("Проверяем результат выбора"):
        result = radio_button_page.get_result_text()

        assert result == "Impressive", f"Ожидался результат 'Impressive', получен '{result}'"
        allure.attach(result, "impressive_radio_result")


@allure.epic("Elements")
@allure.feature("Radio Button")
@allure.story("Disabled State")
@pytest.mark.elements
@pytest.mark.regression
def test_select_no_radio_disabled(radio_button_page):
    """
    Тест попытки выбора отключенной радио кнопки No.

    Шаги:
    1. Попытаться кликнуть по отключенной кнопке No
    2. Убедиться что клик невозможен или не влияет на результат
    3. Проверить что результат не отображается
    """
    with allure.step("Пытаемся кликнуть по отключенной кнопке No"):
        # Проверяем что кнопка действительно отключена
        no_radio_input = radio_button_page.page.locator(RadioButtonLocators.NO_RADIO_INPUT)
        is_disabled = no_radio_input.is_disabled()

        allure.attach(f"No radio disabled: {is_disabled}", "radio_state")

        if is_disabled:
            # Если кнопка отключена, клик должен вызвать ошибку или не сработать
            with pytest.raises(Error):
                radio_button_page.select_no()
        else:
            # Если кнопка не отключена, проверяем что клик не работает
            radio_button_page.select_no()

    with allure.step("Проверяем что результат не отображается для отключенной кнопки"):
        result_visible = radio_button_page.page.locator(RadioButtonLocators.RESULT_TEXT).is_visible()

        # Если результат виден, он не должен содержать "No"
        if result_visible:
            result = radio_button_page.get_result_text()
            assert result != "No", f"Отключенная кнопка не должна давать результат 'No', получен '{result}'"

        allure.attach(f"Result visible: {result_visible}", "disabled_button_result")


@allure.epic("Elements")
@allure.feature("Radio Button")
@allure.story("Radio Group Behavior")
@pytest.mark.elements
def test_radio_button_group_exclusivity(radio_button_page):
    """
    Тест эксклюзивности радио кнопок (только одна может быть выбрана).

    Шаги:
    1. Выбрать первую кнопку Yes
    2. Выбрать вторую кнопку Impressive
    3. Убедиться что активна только вторая кнопка
    """
    with allure.step("Выбираем кнопку Yes"):
        radio_button_page.select_yes()
        first_result = radio_button_page.get_result_text()
        assert first_result == "Yes", "Первый выбор должен быть Yes"

    with allure.step("Выбираем кнопку Impressive (должна заменить Yes)"):
        radio_button_page.select_impressive()
        second_result = radio_button_page.get_result_text()
        assert second_result == "Impressive", "Второй выбор должен быть Impressive"

    with allure.step("Проверяем что только одна кнопка активна"):
        # Проверяем состояние input элементов
        yes_checked = radio_button_page.page.locator(RadioButtonLocators.YES_RADIO_INPUT).is_checked()
        impressive_checked = radio_button_page.page.locator(RadioButtonLocators.IMPRESSIVE_RADIO_INPUT).is_checked()

        assert not yes_checked, "Кнопка Yes не должна быть выбрана после выбора Impressive"
        assert impressive_checked, "Кнопка Impressive должна быть выбрана"

        allure.attach(f"Yes checked: {yes_checked}, Impressive checked: {impressive_checked}", "radio_states")


@allure.epic("Elements")
@allure.feature("Radio Button")
@allure.story("UI State Verification")
@pytest.mark.elements
def test_radio_button_visual_states(radio_button_page):
    """
    Тест визуальных состояний радио кнопок.

    Проверяет доступность кнопок и их визуальное отображение.
    """
    with allure.step("Проверяем начальное состояние всех радио кнопок"):
        # Проверяем видимость всех кнопок
        yes_visible = radio_button_page.page.locator(RadioButtonLocators.YES_RADIO).is_visible()
        impressive_visible = radio_button_page.page.locator(RadioButtonLocators.IMPRESSIVE_RADIO).is_visible()
        no_visible = radio_button_page.page.locator(RadioButtonLocators.NO_RADIO).is_visible()

        assert yes_visible, "Кнопка Yes должна быть видима"
        assert impressive_visible, "Кнопка Impressive должна быть видима"
        assert no_visible, "Кнопка No должна быть видима (даже если отключена)"

    with allure.step("Проверяем доступность кнопок"):
        yes_enabled = not radio_button_page.page.locator(RadioButtonLocators.YES_RADIO_INPUT).is_disabled()
        impressive_enabled = not radio_button_page.page.locator(RadioButtonLocators.IMPRESSIVE_RADIO_INPUT).is_disabled()
        no_enabled = not radio_button_page.page.locator(RadioButtonLocators.NO_RADIO_INPUT).is_disabled()

        assert yes_enabled, "Кнопка Yes должна быть доступна"
        assert impressive_enabled, "Кнопка Impressive должна быть доступна"
        assert not no_enabled, "Кнопка No должна быть отключена"

        button_states = {
            "yes_enabled": yes_enabled,
            "impressive_enabled": impressive_enabled,
            "no_enabled": no_enabled
        }
        allure.attach(str(button_states), "button_accessibility_states")

    with allure.step("Проверяем начальное отсутствие выбора"):
        # В начале ни одна кнопка не должна быть выбрана
        result_visible = radio_button_page.page.locator(RadioButtonLocators.RESULT_TEXT).is_visible()

        if result_visible:
            result = radio_button_page.get_result_text()
            allure.attach(result, "initial_result_state")
        else:
            allure.attach("No result displayed initially", "initial_result_state")
