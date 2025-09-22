"""
Тесты для страницы Auto Complete.
Проверяет функциональность автодополнения:
- Одиночное автодополнение
- Множественное автодополнение
- Поиск и фильтрация вариантов
- Выбор предложенных вариантов
"""

import pytest
import allure
from pages.widgets.auto_complete_page import AutoCompletePage


@allure.epic("Widgets")
@allure.feature("Auto Complete")
@allure.story("Single Auto Complete")
@pytest.mark.widgets
@pytest.mark.smoke
def test_single_auto_complete_functionality(auto_complete_page: AutoCompletePage):
    """
    Тест функциональности одиночного автодополнения.

    Проверяет ввод текста и появление вариантов автодополнения.
    """
    test_inputs = ["Red", "Bl", "Gre", "Yel"]  # Различные начала цветов

    with allure.step("Проверяем наличие поля одиночного автодополнения"):
        single_input_present = (
            auto_complete_page.is_single_auto_complete_input_present()
        )
        auto_complete_page.log_step(
            f"Поле одиночного автодополнения присутствует: {single_input_present}"
        )

        assert (
            single_input_present
        ), "Поле одиночного автодополнения должно присутствовать на странице"

    with allure.step("Очищаем поле и проверяем начальное состояние"):
        auto_complete_page.clear_single_input()
        initial_value = auto_complete_page.get_single_input_value()
        auto_complete_page.log_step(f"Начальное значение поля: '{initial_value}'")

        assert (
            len(initial_value) == 0
        ), f"Поле должно быть пустым изначально: '{initial_value}'"

    autocomplete_results = []

    for test_input in test_inputs:
        with allure.step(f"Тестируем автодополнение для ввода: '{test_input}'"):
            auto_complete_page.log_step(
                f"Ввод текста для автодополнения: '{test_input}'"
            )

            # Очищаем поле и вводим тестовый текст
            auto_complete_page.clear_single_input()
            auto_complete_page.type_in_single_input(test_input)

            # Ждем появления вариантов автодополнения
            auto_complete_page.page.wait_for_timeout(1500)

            # Проверяем появились ли варианты
            suggestions_visible = auto_complete_page.are_single_suggestions_visible()
            suggestions_list = auto_complete_page.get_single_suggestions_list()

            # Получаем текущее значение поля
            current_value = auto_complete_page.get_single_input_value()

            autocomplete_test = {
                "input_text": test_input,
                "current_field_value": current_value,
                "suggestions_visible": suggestions_visible,
                "suggestions_count": len(suggestions_list),
                "suggestions_list": suggestions_list[:5],  # Первые 5 для краткости
                "input_accepted": current_value == test_input,
                "autocomplete_triggered": suggestions_visible
                and len(suggestions_list) > 0,
            }

            autocomplete_results.append(autocomplete_test)
            auto_complete_page.log_step(
                f"Результат автодополнения для '{test_input}': {autocomplete_test}"
            )

            # Если есть предложения, пытаемся выбрать первое
            if suggestions_visible and len(suggestions_list) > 0:
                auto_complete_page.log_step(
                    f"Выбор первого предложения: '{suggestions_list[0]}'"
                )
                selection_result = auto_complete_page.select_first_single_suggestion()

                if selection_result:
                    final_value = auto_complete_page.get_single_input_value()
                    autocomplete_test["first_suggestion_selected"] = True
                    autocomplete_test["final_value_after_selection"] = final_value
                    auto_complete_page.log_step(
                        f"Значение после выбора: '{final_value}'"
                    )
                else:
                    autocomplete_test["first_suggestion_selected"] = False

    with allure.step("Анализируем результаты одиночного автодополнения"):
        allure.attach(
            str(autocomplete_results),
            "single_autocomplete_results",
            allure.attachment_type.JSON,
        )

        successful_autocompletes = sum(
            1 for result in autocomplete_results if result["autocomplete_triggered"]
        )
        successful_selections = sum(
            1
            for result in autocomplete_results
            if result.get("first_suggestion_selected", False)
        )

        single_autocomplete_summary = {
            "total_inputs_tested": len(autocomplete_results),
            "successful_autocompletes": successful_autocompletes,
            "successful_selections": successful_selections,
            "autocomplete_success_rate": (
                successful_autocompletes / len(autocomplete_results)
                if autocomplete_results
                else 0
            ),
            "selection_success_rate": (
                successful_selections / len(autocomplete_results)
                if autocomplete_results
                else 0
            ),
            "autocomplete_works": successful_autocompletes > 0,
            "selection_works": successful_selections > 0,
        }

        auto_complete_page.log_step(
            f"Итоги одиночного автодополнения: {single_autocomplete_summary}"
        )
        allure.attach(
            str(single_autocomplete_summary),
            "single_autocomplete_summary",
            allure.attachment_type.JSON,
        )

        assert single_autocomplete_summary[
            "autocomplete_works"
        ], f"Автодополнение должно работать хотя бы для одного ввода: {successful_autocompletes}/{len(autocomplete_results)}"

        if single_autocomplete_summary["selection_works"]:
            auto_complete_page.log_step(
                "✅ Выбор предложений одиночного автодополнения работает"
            )
        else:
            auto_complete_page.log_step(
                "ℹ️ Выбор предложений требует дополнительной проверки"
            )


@allure.epic("Widgets")
@allure.feature("Auto Complete")
@allure.story("Multiple Auto Complete")
@pytest.mark.widgets
@pytest.mark.smoke
def test_multiple_auto_complete_functionality(auto_complete_page: AutoCompletePage):
    """
    Тест функциональности множественного автодополнения.

    Проверяет возможность выбора нескольких значений с автодополнением.
    """
    test_colors = ["Red", "Blue", "Green", "Yellow"]

    with allure.step("Проверяем наличие поля множественного автодополнения"):
        multiple_input_present = (
            auto_complete_page.is_multiple_auto_complete_input_present()
        )
        auto_complete_page.log_step(
            f"Поле множественного автодополнения присутствует: {multiple_input_present}"
        )

        assert (
            multiple_input_present
        ), "Поле множественного автодополнения должно присутствовать на странице"

    with allure.step("Очищаем поле множественного автодополнения"):
        auto_complete_page.clear_multiple_input()
        initial_values = auto_complete_page.get_multiple_selected_values()
        auto_complete_page.log_step(f"Начальные выбранные значения: {initial_values}")

        assert (
            len(initial_values) == 0
        ), f"Поле должно быть пустым изначально: {initial_values}"

    multiple_selections = []

    for i, color in enumerate(test_colors):
        with allure.step(f"Добавляем цвет {i + 1}: '{color}'"):
            auto_complete_page.log_step(f"Попытка добавления цвета: '{color}'")

            # Вводим часть названия цвета
            color_prefix = color[:2]  # Первые 2 буквы
            auto_complete_page.type_in_multiple_input(color_prefix)
            auto_complete_page.page.wait_for_timeout(1000)

            # Проверяем появление предложений
            multiple_suggestions_visible = (
                auto_complete_page.are_multiple_suggestions_visible()
            )
            multiple_suggestions = auto_complete_page.get_multiple_suggestions_list()

            # Пытаемся найти и выбрать нужный цвет
            color_found_in_suggestions = color in multiple_suggestions

            if color_found_in_suggestions:
                selection_success = (
                    auto_complete_page.select_multiple_suggestion_by_text(color)
                )
            else:
                # Пытаемся выбрать первое предложение
                selection_success = (
                    auto_complete_page.select_first_multiple_suggestion()
                )

            auto_complete_page.page.wait_for_timeout(500)

            # Проверяем результат выбора
            current_selected_values = auto_complete_page.get_multiple_selected_values()

            selection_test = {
                "attempt_number": i + 1,
                "target_color": color,
                "color_prefix_typed": color_prefix,
                "suggestions_appeared": multiple_suggestions_visible,
                "suggestions_count": len(multiple_suggestions),
                "target_color_in_suggestions": color_found_in_suggestions,
                "selection_attempted": True,
                "selection_successful": selection_success,
                "current_selected_values": current_selected_values.copy(),
                "total_selected": len(current_selected_values),
                "value_added": len(current_selected_values) > len(multiple_selections),
            }

            multiple_selections.append(selection_test)
            auto_complete_page.log_step(
                f"Результат добавления '{color}': {selection_test}"
            )

            # Очищаем поле ввода для следующего элемента
            auto_complete_page.clear_multiple_input_text()

    with allure.step("Тестируем удаление выбранных значений"):
        current_values_before_removal = (
            auto_complete_page.get_multiple_selected_values()
        )
        auto_complete_page.log_step(
            f"Значения перед удалением: {current_values_before_removal}"
        )

        removal_tests = []

        # Пытаемся удалить первое значение если есть выбранные
        if len(current_values_before_removal) > 0:
            first_value_to_remove = current_values_before_removal[0]
            auto_complete_page.log_step(
                f"Попытка удаления первого значения: '{first_value_to_remove}'"
            )

            removal_success = auto_complete_page.remove_multiple_value_by_index(0)
            auto_complete_page.page.wait_for_timeout(500)

            values_after_removal = auto_complete_page.get_multiple_selected_values()

            removal_test = {
                "value_to_remove": first_value_to_remove,
                "removal_attempted": True,
                "removal_successful": removal_success,
                "values_before": current_values_before_removal.copy(),
                "values_after": values_after_removal.copy(),
                "value_actually_removed": first_value_to_remove
                not in values_after_removal,
                "count_decreased": len(values_after_removal)
                < len(current_values_before_removal),
            }

            removal_tests.append(removal_test)
            auto_complete_page.log_step(f"Результат удаления: {removal_test}")

    with allure.step("Анализируем результаты множественного автодополнения"):
        allure.attach(
            str(multiple_selections),
            "multiple_autocomplete_selections",
            allure.attachment_type.JSON,
        )
        allure.attach(
            str(removal_tests), "multiple_value_removals", allure.attachment_type.JSON
        )

        successful_additions = sum(
            1 for selection in multiple_selections if selection["value_added"]
        )
        suggestions_appeared_count = sum(
            1 for selection in multiple_selections if selection["suggestions_appeared"]
        )
        successful_removals = sum(
            1 for removal in removal_tests if removal["value_actually_removed"]
        )

        final_selected_values = auto_complete_page.get_multiple_selected_values()

        multiple_autocomplete_summary = {
            "colors_attempted": len(multiple_selections),
            "successful_additions": successful_additions,
            "suggestions_appeared_count": suggestions_appeared_count,
            "successful_removals": successful_removals,
            "final_selected_count": len(final_selected_values),
            "final_selected_values": final_selected_values,
            "multiple_selection_works": successful_additions > 1,
            "autocomplete_suggestions_work": suggestions_appeared_count > 0,
            "removal_functionality_works": successful_removals > 0
            or len(removal_tests) == 0,
        }

        auto_complete_page.log_step(
            f"Итоги множественного автодополнения: {multiple_autocomplete_summary}"
        )
        allure.attach(
            str(multiple_autocomplete_summary),
            "multiple_autocomplete_summary",
            allure.attachment_type.JSON,
        )

        assert multiple_autocomplete_summary[
            "autocomplete_suggestions_work"
        ], f"Должны появляться предложения автодополнения: {suggestions_appeared_count}/{len(multiple_selections)}"
        assert (
            multiple_autocomplete_summary["successful_additions"] > 0
        ), f"Должно быть добавлено хотя бы одно значение: {successful_additions}/{len(multiple_selections)}"

        if multiple_autocomplete_summary["multiple_selection_works"]:
            auto_complete_page.log_step(
                "✅ Множественное автодополнение работает корректно"
            )
        else:
            auto_complete_page.log_step(
                "ℹ️ Удалось добавить только одно значение - проверьте настройки множественного выбора"
            )
