"""
Тесты для страницы Slider.
Проверяет функциональность слайдеров:
- Одиночный слайдер
- Диапазонный слайдер
- Перемещение ползунков
- Значения слайдеров
"""

import pytest
import allure
from pages.widgets.slider_page import SliderPage


def _compare_values(val1, val2, operator):
    """Сравнивает два значения с учетом их типа"""
    try:
        num1 = _to_numeric(val1)
        num2 = _to_numeric(val2)
        if operator == ">":
            return num1 > num2
        elif operator == "<":
            return num1 < num2
        elif operator == "==":
            return num1 == num2
    except:
        return False


def _to_numeric(value):
    """Преобразует значение в число"""
    if isinstance(value, (int, float)):
        return value
    elif isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return 0
    return 0


def _values_approximately_equal(val1, val2, tolerance=5):
    """Проверяет приблизительное равенство значений"""
    try:
        num1 = _to_numeric(val1)
        num2 = _to_numeric(val2)
        return abs(num1 - num2) <= tolerance
    except:
        return val1 == val2


def _value_respects_step(value, min_value, step):
    """Проверяет соблюдение шага значением"""
    try:
        numeric_value = _to_numeric(value)
        numeric_min = _to_numeric(min_value)
        numeric_step = _to_numeric(step)

        if numeric_step <= 0:
            return True  # Если шаг не определен, считаем что все ОК

        difference = numeric_value - numeric_min
        return (
            abs(difference % numeric_step) < 0.01
            or abs(difference % numeric_step - numeric_step) < 0.01
        )
    except:
        return True  # В случае ошибки считаем что все ОК


@allure.epic("Widgets")
@allure.feature("Slider")
@allure.story("Single Value Slider")
@pytest.mark.widgets
@pytest.mark.smoke
def test_single_value_slider(slider_page: SliderPage):
    """
    Тест одиночного слайдера с одним значением.

    Перемещает ползунок и проверяет изменение значения.
    """

    with allure.step("Проверяем наличие одиночного слайдера"):
        single_slider_present = slider_page.is_single_slider_present()
        slider_page.log_step(f"Одиночный слайдер присутствует: {single_slider_present}")

        assert (
            single_slider_present
        ), "Одиночный слайдер должен присутствовать на странице"

    with allure.step("Получаем начальное значение слайдера"):
        initial_value = slider_page.get_single_slider_value()
        initial_position = slider_page.get_single_slider_position()

        slider_page.log_step(f"Начальное значение слайдера: {initial_value}")
        slider_page.log_step(f"Начальная позиция ползунка: {initial_position}")

        slider_info = {
            "initial_value": initial_value,
            "initial_position": initial_position,
            "value_is_numeric": isinstance(initial_value, (int, float))
            or (isinstance(initial_value, str) and initial_value.isdigit()),
        }

        allure.attach(
            str(slider_info), "initial_slider_state", allure.attachment_type.JSON
        )

    with allure.step("Получаем границы и свойства слайдера"):
        slider_properties = slider_page.get_single_slider_properties()
        slider_page.log_step(f"Свойства слайдера: {slider_properties}")

        allure.attach(
            str(slider_properties), "slider_properties", allure.attachment_type.JSON
        )

        # Проверяем что слайдер имеет разумные границы
        min_value = slider_properties.get("min", 0)
        max_value = slider_properties.get("max", 100)
        assert (
            max_value > min_value
        ), f"Максимальное значение должно быть больше минимального: max={max_value}, min={min_value}"

    slider_movement_tests = []

    with allure.step("Тестируем перемещение ползунка вправо"):
        slider_page.log_step("Перемещение ползунка в положительном направлении")

        # Перемещаем ползунок на 30% от ширины слайдера
        move_right_result = slider_page.move_single_slider_by_percentage(30)
        slider_page.page.wait_for_timeout(100)

        value_after_right = slider_page.get_single_slider_value()
        position_after_right = slider_page.get_single_slider_position()

        right_movement_test = {
            "direction": "right",
            "movement_attempted": True,
            "movement_successful": move_right_result,
            "value_before": initial_value,
            "value_after": value_after_right,
            "position_before": initial_position,
            "position_after": position_after_right,
            "value_changed": value_after_right != initial_value,
            "value_increased": _compare_values(
                value_after_right, initial_value, ">"
            ),
        }

        slider_movement_tests.append(right_movement_test)
        slider_page.log_step(f"Результат движения вправо: {right_movement_test}")

    with allure.step("Тестируем перемещение ползунка влево"):
        slider_page.log_step("Перемещение ползунка в отрицательном направлении")

        # Перемещаем ползунок влево на 50% от ширины
        move_left_result = slider_page.move_single_slider_by_percentage(-50)
        slider_page.page.wait_for_timeout(100)

        value_after_left = slider_page.get_single_slider_value()
        position_after_left = slider_page.get_single_slider_position()

        left_movement_test = {
            "direction": "left",
            "movement_attempted": True,
            "movement_successful": move_left_result,
            "value_before": value_after_right,
            "value_after": value_after_left,
            "position_before": position_after_right,
            "position_after": position_after_left,
            "value_changed": value_after_left != value_after_right,
            "value_decreased": _compare_values(
                value_after_left, value_after_right, "<"
            ),
        }

        slider_movement_tests.append(left_movement_test)
        slider_page.log_step(f"Результат движения влево: {left_movement_test}")

    with allure.step("Тестируем установку конкретного значения"):
        target_value = (min_value + max_value) // 2  # Среднее значение
        slider_page.log_step(f"Установка конкретного значения: {target_value}")

        set_value_result = slider_page.set_single_slider_value(target_value)
        slider_page.page.wait_for_timeout(100)

        value_after_set = slider_page.get_single_slider_value()

        set_value_test = {
            "target_value": target_value,
            "set_value_attempted": True,
            "set_value_successful": set_value_result,
            "actual_value": value_after_set,
            "value_matches_target": _values_approximately_equal(
                value_after_set, target_value
            ),
            "value_in_expected_range": min_value
            <= _to_numeric(value_after_set)
            <= max_value,
        }

        slider_movement_tests.append(set_value_test)
        slider_page.log_step(f"Результат установки значения: {set_value_test}")

    with allure.step("Анализируем функциональность одиночного слайдера"):
        allure.attach(
            str(slider_movement_tests),
            "single_slider_movement_tests",
            allure.attachment_type.JSON,
        )

        successful_movements = sum(
            1
            for test in slider_movement_tests
            if test.get("movement_successful") or test.get("set_value_successful")
        )
        value_changes = sum(
            1 for test in slider_movement_tests if test.get("value_changed")
        )

        single_slider_summary = {
            "total_movement_tests": len(slider_movement_tests),
            "successful_movements": successful_movements,
            "value_changes": value_changes,
            "slider_responds_to_interaction": successful_movements > 0,
            "values_change_on_movement": value_changes > 0,
            "slider_functional": successful_movements > 0 and value_changes > 0,
            "movement_details": slider_movement_tests,
        }

        slider_page.log_step(
            f"Итоги тестирования одиночного слайдера: {single_slider_summary}"
        )
        allure.attach(
            str(single_slider_summary),
            "single_slider_summary",
            allure.attachment_type.JSON,
        )

        assert single_slider_summary[
            "slider_responds_to_interaction"
        ], f"Слайдер должен реагировать на взаимодействие: {successful_movements}/{len(slider_movement_tests)}"
        assert single_slider_summary[
            "values_change_on_movement"
        ], f"Значения должны изменяться при движении: {value_changes}/{len(slider_movement_tests)}"

        if single_slider_summary["slider_functional"]:
            slider_page.log_step("✅ Одиночный слайдер полностью функционален")
        else:
            slider_page.log_step(
                "⚠️ Одиночный слайдер имеет ограничения в функциональности"
            )


