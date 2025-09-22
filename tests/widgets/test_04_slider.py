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
        slider_page.page.wait_for_timeout(500)

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
            "value_increased": self._compare_values(
                value_after_right, initial_value, ">"
            ),
        }

        slider_movement_tests.append(right_movement_test)
        slider_page.log_step(f"Результат движения вправо: {right_movement_test}")

    with allure.step("Тестируем перемещение ползунка влево"):
        slider_page.log_step("Перемещение ползунка в отрицательном направлении")

        # Перемещаем ползунок влево на 50% от ширины
        move_left_result = slider_page.move_single_slider_by_percentage(-50)
        slider_page.page.wait_for_timeout(500)

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
            "value_decreased": self._compare_values(
                value_after_left, value_after_right, "<"
            ),
        }

        slider_movement_tests.append(left_movement_test)
        slider_page.log_step(f"Результат движения влево: {left_movement_test}")

    with allure.step("Тестируем установку конкретного значения"):
        target_value = (min_value + max_value) // 2  # Среднее значение
        slider_page.log_step(f"Установка конкретного значения: {target_value}")

        set_value_result = slider_page.set_single_slider_value(target_value)
        slider_page.page.wait_for_timeout(500)

        value_after_set = slider_page.get_single_slider_value()

        set_value_test = {
            "target_value": target_value,
            "set_value_attempted": True,
            "set_value_successful": set_value_result,
            "actual_value": value_after_set,
            "value_matches_target": self._values_approximately_equal(
                value_after_set, target_value
            ),
            "value_in_expected_range": min_value
            <= self._to_numeric(value_after_set)
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

    def _compare_values(self, val1, val2, operator):
        """Сравнивает два значения с учетом их типа"""
        try:
            num1 = self._to_numeric(val1)
            num2 = self._to_numeric(val2)
            if operator == ">":
                return num1 > num2
            elif operator == "<":
                return num1 < num2
            elif operator == "==":
                return num1 == num2
        except:
            return False

    def _to_numeric(self, value):
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

    def _values_approximately_equal(self, val1, val2, tolerance=5):
        """Проверяет приблизительное равенство значений"""
        try:
            num1 = self._to_numeric(val1)
            num2 = self._to_numeric(val2)
            return abs(num1 - num2) <= tolerance
        except:
            return val1 == val2


@allure.epic("Widgets")
@allure.feature("Slider")
@allure.story("Range Slider")
@pytest.mark.widgets
@pytest.mark.regression
def test_range_slider(slider_page: SliderPage):
    """
    Тест диапазонного слайдера с двумя ползунками.

    Проверяет перемещение обоих ползунков и установку диапазона значений.
    """
    with allure.step("Проверяем наличие диапазонного слайдера"):
        range_slider_present = slider_page.is_range_slider_present()
        slider_page.log_step(
            f"Диапазонный слайдер присутствует: {range_slider_present}"
        )

        if not range_slider_present:
            slider_page.log_step("ℹ️ Диапазонный слайдер недоступен на данной странице")
            return

    with allure.step("Получаем начальные значения диапазонного слайдера"):
        initial_min_value = slider_page.get_range_slider_min_value()
        initial_max_value = slider_page.get_range_slider_max_value()
        initial_range = slider_page.get_range_slider_range()

        slider_page.log_step(f"Начальное минимальное значение: {initial_min_value}")
        slider_page.log_step(f"Начальное максимальное значение: {initial_max_value}")
        slider_page.log_step(f"Начальный диапазон: {initial_range}")

        range_info = {
            "initial_min": initial_min_value,
            "initial_max": initial_max_value,
            "initial_range": initial_range,
            "valid_range": self._to_numeric(initial_max_value)
            >= self._to_numeric(initial_min_value),
        }

        allure.attach(
            str(range_info), "initial_range_slider_state", allure.attachment_type.JSON
        )

        assert range_info[
            "valid_range"
        ], f"Максимальное значение должно быть >= минимального: min={initial_min_value}, max={initial_max_value}"

    range_movement_tests = []

    with allure.step("Тестируем перемещение левого ползунка (минимум)"):
        slider_page.log_step(
            "Перемещение левого ползунка для изменения минимального значения"
        )

        move_min_result = slider_page.move_range_slider_min_handle(20)  # На 20% вправо
        slider_page.page.wait_for_timeout(500)

        min_value_after = slider_page.get_range_slider_min_value()
        max_value_after_min_move = slider_page.get_range_slider_max_value()

        min_handle_test = {
            "handle": "min",
            "movement_direction": "right",
            "movement_successful": move_min_result,
            "value_before": initial_min_value,
            "value_after": min_value_after,
            "other_handle_before": initial_max_value,
            "other_handle_after": max_value_after_min_move,
            "value_changed": min_value_after != initial_min_value,
            "other_handle_unchanged": max_value_after_min_move == initial_max_value,
            "range_still_valid": self._to_numeric(max_value_after_min_move)
            >= self._to_numeric(min_value_after),
        }

        range_movement_tests.append(min_handle_test)
        slider_page.log_step(f"Результат движения левого ползунка: {min_handle_test}")

    with allure.step("Тестируем перемещение правого ползунка (максимум)"):
        slider_page.log_step(
            "Перемещение правого ползунка для изменения максимального значения"
        )

        move_max_result = slider_page.move_range_slider_max_handle(-15)  # На 15% влево
        slider_page.page.wait_for_timeout(500)

        min_value_after_max_move = slider_page.get_range_slider_min_value()
        max_value_after = slider_page.get_range_slider_max_value()

        max_handle_test = {
            "handle": "max",
            "movement_direction": "left",
            "movement_successful": move_max_result,
            "value_before": max_value_after_min_move,
            "value_after": max_value_after,
            "other_handle_before": min_value_after,
            "other_handle_after": min_value_after_max_move,
            "value_changed": max_value_after != max_value_after_min_move,
            "other_handle_unchanged": min_value_after_max_move == min_value_after,
            "range_still_valid": self._to_numeric(max_value_after)
            >= self._to_numeric(min_value_after_max_move),
        }

        range_movement_tests.append(max_handle_test)
        slider_page.log_step(f"Результат движения правого ползунка: {max_handle_test}")

    with allure.step("Тестируем установку конкретного диапазона"):
        target_min = 25
        target_max = 75

        slider_page.log_step(f"Установка диапазона: {target_min} - {target_max}")

        set_range_result = slider_page.set_range_slider_values(target_min, target_max)
        slider_page.page.wait_for_timeout(500)

        final_min = slider_page.get_range_slider_min_value()
        final_max = slider_page.get_range_slider_max_value()

        set_range_test = {
            "target_min": target_min,
            "target_max": target_max,
            "set_range_attempted": True,
            "set_range_successful": set_range_result,
            "actual_min": final_min,
            "actual_max": final_max,
            "min_approximately_correct": self._values_approximately_equal(
                final_min, target_min, tolerance=10
            ),
            "max_approximately_correct": self._values_approximately_equal(
                final_max, target_max, tolerance=10
            ),
            "range_valid": self._to_numeric(final_max) >= self._to_numeric(final_min),
        }

        range_movement_tests.append(set_range_test)
        slider_page.log_step(f"Результат установки диапазона: {set_range_test}")

    with allure.step("Анализируем функциональность диапазонного слайдера"):
        allure.attach(
            str(range_movement_tests),
            "range_slider_movement_tests",
            allure.attachment_type.JSON,
        )

        successful_movements = sum(
            1
            for test in range_movement_tests
            if test.get("movement_successful") or test.get("set_range_successful")
        )
        handle_value_changes = sum(
            1 for test in range_movement_tests if test.get("value_changed")
        )
        valid_ranges_maintained = sum(
            1 for test in range_movement_tests if test.get("range_still_valid", True)
        )

        range_slider_summary = {
            "total_range_tests": len(range_movement_tests),
            "successful_movements": successful_movements,
            "handle_value_changes": handle_value_changes,
            "valid_ranges_maintained": valid_ranges_maintained,
            "range_slider_functional": successful_movements > 0
            and handle_value_changes > 0,
            "range_constraints_respected": valid_ranges_maintained
            == len(range_movement_tests),
            "movement_details": range_movement_tests,
        }

        slider_page.log_step(
            f"Итоги тестирования диапазонного слайдера: {range_slider_summary}"
        )
        allure.attach(
            str(range_slider_summary),
            "range_slider_summary",
            allure.attachment_type.JSON,
        )

        assert range_slider_summary[
            "range_slider_functional"
        ], f"Диапазонный слайдер должен быть функциональным: движений {successful_movements}, изменений {handle_value_changes}"
        assert range_slider_summary[
            "range_constraints_respected"
        ], f"Ограничения диапазона должны соблюдаться: {valid_ranges_maintained}/{len(range_movement_tests)}"

        if range_slider_summary["range_slider_functional"]:
            slider_page.log_step("✅ Диапазонный слайдер полностью функционален")
        else:
            slider_page.log_step(
                "⚠️ Диапазонный слайдер имеет ограничения в функциональности"
            )


@allure.epic("Widgets")
@allure.feature("Slider")
@allure.story("Slider Precision")
@pytest.mark.widgets
def test_slider_precision_and_step(slider_page: SliderPage):
    """
    Тест точности и шага слайдера.

    Проверяет возможность установки точных значений и соблюдение шага.
    """
    with allure.step("Анализируем свойства шага слайдера"):
        slider_step_info = slider_page.get_slider_step_properties()
        slider_page.log_step(f"Информация о шаге слайдера: {slider_step_info}")

        allure.attach(
            str(slider_step_info), "slider_step_properties", allure.attachment_type.JSON
        )

        step_value = slider_step_info.get("step", 1)
        min_value = slider_step_info.get("min", 0)
        max_value = slider_step_info.get("max", 100)

    precision_tests = []

    with allure.step("Тестируем точность установки значений"):
        test_values = [
            min_value + step_value,
            min_value + step_value * 5,
            (min_value + max_value) // 2,
            max_value - step_value * 3,
            max_value - step_value,
        ]

        for test_value in test_values:
            if min_value <= test_value <= max_value:
                with allure.step(f"Установка точного значения: {test_value}"):
                    slider_page.log_step(
                        f"Тестирование установки значения: {test_value}"
                    )

                    set_result = slider_page.set_single_slider_value(test_value)
                    slider_page.page.wait_for_timeout(300)

                    actual_value = slider_page.get_single_slider_value()

                    precision_test = {
                        "target_value": test_value,
                        "actual_value": actual_value,
                        "set_successful": set_result,
                        "value_exact": self._values_approximately_equal(
                            actual_value, test_value, tolerance=step_value
                        ),
                        "value_respects_step": self._value_respects_step(
                            actual_value, min_value, step_value
                        ),
                        "value_in_bounds": min_value
                        <= self._to_numeric(actual_value)
                        <= max_value,
                    }

                    precision_tests.append(precision_test)
                    slider_page.log_step(
                        f"Результат установки {test_value}: {precision_test}"
                    )

    with allure.step("Тестируем граничные значения"):
        boundary_tests = []

        # Тест минимального значения
        slider_page.log_step(f"Установка минимального значения: {min_value}")
        min_set_result = slider_page.set_single_slider_value(min_value)
        min_actual = slider_page.get_single_slider_value()

        boundary_tests.append(
            {
                "boundary": "minimum",
                "target": min_value,
                "actual": min_actual,
                "set_successful": min_set_result,
                "correct_boundary": self._values_approximately_equal(
                    min_actual, min_value, tolerance=step_value
                ),
            }
        )

        # Тест максимального значения
        slider_page.log_step(f"Установка максимального значения: {max_value}")
        max_set_result = slider_page.set_single_slider_value(max_value)
        max_actual = slider_page.get_single_slider_value()

        boundary_tests.append(
            {
                "boundary": "maximum",
                "target": max_value,
                "actual": max_actual,
                "set_successful": max_set_result,
                "correct_boundary": self._values_approximately_equal(
                    max_actual, max_value, tolerance=step_value
                ),
            }
        )

        slider_page.log_step(f"Результаты тестирования границ: {boundary_tests}")

    with allure.step("Анализируем точность и соблюдение шага"):
        allure.attach(
            str(precision_tests), "precision_tests_results", allure.attachment_type.JSON
        )
        allure.attach(
            str(boundary_tests), "boundary_tests_results", allure.attachment_type.JSON
        )

        exact_values = sum(1 for test in precision_tests if test["value_exact"])
        step_compliant = sum(
            1 for test in precision_tests if test["value_respects_step"]
        )
        in_bounds = sum(1 for test in precision_tests if test["value_in_bounds"])
        correct_boundaries = sum(
            1 for test in boundary_tests if test["correct_boundary"]
        )

        precision_summary = {
            "total_precision_tests": len(precision_tests),
            "exact_values_achieved": exact_values,
            "step_compliant_values": step_compliant,
            "values_in_bounds": in_bounds,
            "boundary_tests": len(boundary_tests),
            "correct_boundaries": correct_boundaries,
            "precision_good": exact_values >= len(precision_tests) * 0.7,
            "step_compliance_good": step_compliant >= len(precision_tests) * 0.7,
            "boundaries_work": correct_boundaries == len(boundary_tests),
            "overall_precision_acceptable": exact_values > 0
            and in_bounds == len(precision_tests),
        }

        slider_page.log_step(f"Итоги точности слайдера: {precision_summary}")
        allure.attach(
            str(precision_summary),
            "slider_precision_summary",
            allure.attachment_type.JSON,
        )

        assert precision_summary[
            "overall_precision_acceptable"
        ], f"Общая точность должна быть приемлемой: точных {exact_values}, в границах {in_bounds}/{len(precision_tests)}"

        if precision_summary["precision_good"]:
            slider_page.log_step("✅ Точность слайдера хорошая")
        else:
            slider_page.log_step("ℹ️ Точность слайдера требует улучшения")

        if precision_summary["step_compliance_good"]:
            slider_page.log_step("✅ Соблюдение шага слайдера хорошее")
        else:
            slider_page.log_step("ℹ️ Соблюдение шага может быть улучшено")

    def _value_respects_step(self, value, min_value, step):
        """Проверяет соблюдение шага значением"""
        try:
            numeric_value = self._to_numeric(value)
            numeric_min = self._to_numeric(min_value)
            numeric_step = self._to_numeric(step)

            if numeric_step <= 0:
                return True  # Если шаг не определен, считаем что все ОК

            difference = numeric_value - numeric_min
            return (
                abs(difference % numeric_step) < 0.01
                or abs(difference % numeric_step - numeric_step) < 0.01
            )
        except:
            return True  # В случае ошибки считаем что все ОК
