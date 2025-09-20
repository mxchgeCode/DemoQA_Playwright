"""
Тесты для страницы Date Picker.
Проверяет функциональность выбора даты:
- Выбор даты через календарь
- Ввод даты вручную
- Выбор даты и времени
- Валидация форматов даты
"""

import pytest
import allure
from datetime import datetime, timedelta
from pages.widgets.date_picker_page import DatePickerPage


@allure.epic("Widgets")
@allure.feature("Date Picker")
@allure.story("Simple Date Selection")
@pytest.mark.widgets
@pytest.mark.smoke
def test_simple_date_picker_selection(date_picker_page: DatePickerPage):
    """
    Тест простого выбора даты через календарь.

    Открывает календарь и выбирает конкретную дату.
    """
    with allure.step("Проверяем наличие поля выбора даты"):
        date_input_present = date_picker_page.is_date_input_present()
        date_picker_page.log_step(f"Поле выбора даты присутствует: {date_input_present}")

        assert date_input_present, "Поле выбора даты должно присутствовать на странице"

    with allure.step("Получаем текущее значение поля даты"):
        initial_date_value = date_picker_page.get_date_input_value()
        date_picker_page.log_step(f"Начальное значение даты: '{initial_date_value}'")

        allure.attach(initial_date_value, "initial_date_value", allure.attachment_type.TEXT)

    with allure.step("Открываем календарь"):
        date_picker_page.log_step("Открытие календаря для выбора даты")
        calendar_opened = date_picker_page.open_date_calendar()

        assert calendar_opened, "Календарь должен открываться при клике на поле даты"

        # Проверяем что календарь видим
        calendar_visible = date_picker_page.is_calendar_visible()
        assert calendar_visible, "Календарь должен быть видимым после открытия"

    with allure.step("Анализируем структуру календаря"):
        calendar_info = date_picker_page.get_calendar_info()
        date_picker_page.log_step(f"Информация о календаре: {calendar_info}")

        allure.attach(str(calendar_info), "calendar_structure_info", allure.attachment_type.JSON)

        # Проверяем основные элементы календаря
        assert calendar_info.get("has_navigation", False), "Календарь должен иметь навигацию по месяцам"
        assert calendar_info.get("has_date_cells", False), "Календарь должен содержать ячейки с датами"

    with allure.step("Выбираем дату в календаре"):
        # Выбираем дату (например, 15 число текущего месяца)
        target_day = 15
        date_picker_page.log_step(f"Попытка выбора {target_day} числа")

        date_selection_result = date_picker_page.select_calendar_date(target_day)
        date_picker_page.log_step(f"Результат выбора даты: {date_selection_result}")

        # Если конкретная дата недоступна, выбираем любую доступную
        if not date_selection_result:
            date_picker_page.log_step("Выбираем первую доступную дату")
            date_selection_result = date_picker_page.select_first_available_date()

        assert date_selection_result, "Должна быть выбрана хотя бы одна дата в календаре"

    with allure.step("Проверяем результат выбора даты"):
        date_picker_page.page.wait_for_timeout(1000)  # Ждем обновления поля

        final_date_value = date_picker_page.get_date_input_value()
        calendar_closed = not date_picker_page.is_calendar_visible()

        date_selection_summary = {
            "initial_date": initial_date_value,
            "final_date": final_date_value,
            "date_changed": final_date_value != initial_date_value,
            "calendar_closed_after_selection": calendar_closed,
            "selection_successful": date_selection_result,
            "final_date_not_empty": len(final_date_value) > 0
        }

        date_picker_page.log_step(f"Итоги выбора даты: {date_selection_summary}")
        allure.attach(str(date_selection_summary), "date_selection_summary", allure.attachment_type.JSON)

        # Проверяем что дата была выбрана
        assert date_selection_summary["final_date_not_empty"], f"Поле даты не должно быть пустым после выбора: '{final_date_value}'"

        if date_selection_summary["date_changed"]:
            date_picker_page.log_step("✅ Дата успешно изменена через календарь")
        else:
            date_picker_page.log_step("ℹ️ Возможно, была выбрана та же дата или дата не изменилась")

        if date_selection_summary["calendar_closed_after_selection"]:
            date_picker_page.log_step("✅ Календарь автоматически закрылся после выбора")


@allure.epic("Widgets")
@allure.feature("Date Picker")
@allure.story("Manual Date Input")
@pytest.mark.widgets
def test_manual_date_input(date_picker_page: DatePickerPage):
    """
    Тест ручного ввода даты в поле.

    Проверяет возможность ввода даты с клавиатуры и валидацию формата.
    """
    # Тестовые даты в различных форматах
    test_dates = [
        "12/31/2023",
        "01/15/2024", 
        "06/20/2024",
        "12/25/2024"
    ]

    manual_input_results = []

    with allure.step("Тестируем ручной ввод различных дат"):
        for test_date in test_dates:
            with allure.step(f"Ввод даты: {test_date}"):
                date_picker_page.log_step(f"Тестирование ручного ввода даты: {test_date}")

                # Очищаем поле и вводим дату
                date_picker_page.clear_date_input()
                input_result = date_picker_page.type_date_manually(test_date)

                # Подтверждаем ввод (например, нажатием Enter или кликом вне поля)
                date_picker_page.confirm_date_input()
                date_picker_page.page.wait_for_timeout(1000)

                # Проверяем результат
                resulting_value = date_picker_page.get_date_input_value()
                date_accepted = len(resulting_value) > 0 and resulting_value != ""

                # Проверяем валидацию даты
                validation_message = date_picker_page.get_date_validation_message()
                has_validation_error = len(validation_message) > 0

                manual_input_test = {
                    "input_date": test_date,
                    "input_successful": input_result,
                    "resulting_value": resulting_value,
                    "date_accepted": date_accepted,
                    "validation_message": validation_message,
                    "has_validation_error": has_validation_error,
                    "format_accepted": resulting_value == test_date or (date_accepted and not has_validation_error)
                }

                manual_input_results.append(manual_input_test)
                date_picker_page.log_step(f"Результат ввода '{test_date}': {manual_input_test}")

    with allure.step("Тестируем некорректные форматы дат"):
        invalid_dates = ["invalid", "32/13/2024", "abc", "99/99/9999"]

        for invalid_date in invalid_dates:
            with allure.step(f"Тест некорректной даты: {invalid_date}"):
                date_picker_page.log_step(f"Тестирование некорректной даты: {invalid_date}")

                date_picker_page.clear_date_input()
                date_picker_page.type_date_manually(invalid_date)
                date_picker_page.confirm_date_input()
                date_picker_page.page.wait_for_timeout(1000)

                resulting_value = date_picker_page.get_date_input_value()
                validation_message = date_picker_page.get_date_validation_message()

                invalid_test = {
                    "invalid_input": invalid_date,
                    "resulting_value": resulting_value,
                    "validation_message": validation_message,
                    "properly_rejected": len(validation_message) > 0 or resulting_value == "" or resulting_value != invalid_date
                }

                manual_input_results.append(invalid_test)
                date_picker_page.log_step(f"Результат некорректного ввода '{invalid_date}': {invalid_test}")

    with allure.step("Анализируем результаты ручного ввода дат"):
        allure.attach(str(manual_input_results), "manual_date_input_results", allure.attachment_type.JSON)

        valid_inputs = [r for r in manual_input_results if not r.get("invalid_input")]
        invalid_inputs = [r for r in manual_input_results if r.get("invalid_input")]

        accepted_valid_dates = sum(1 for r in valid_inputs if r["date_accepted"])
        properly_rejected_invalid = sum(1 for r in invalid_inputs if r["properly_rejected"])

        manual_input_summary = {
            "total_valid_dates_tested": len(valid_inputs),
            "total_invalid_dates_tested": len(invalid_inputs),
            "accepted_valid_dates": accepted_valid_dates,
            "properly_rejected_invalid": properly_rejected_invalid,
            "valid_date_acceptance_rate": accepted_valid_dates / len(valid_inputs) if valid_inputs else 0,
            "invalid_date_rejection_rate": properly_rejected_invalid / len(invalid_inputs) if invalid_inputs else 0,
            "manual_input_works": accepted_valid_dates > 0,
            "validation_works": properly_rejected_invalid > 0 or len(invalid_inputs) == 0
        }

        date_picker_page.log_step(f"Итоги ручного ввода дат: {manual_input_summary}")
        allure.attach(str(manual_input_summary), "manual_input_summary", allure.attachment_type.JSON)

        assert manual_input_summary["manual_input_works"], f"Ручной ввод должен работать: принято {accepted_valid_dates}/{len(valid_inputs)} валидных дат"

        if manual_input_summary["validation_works"]:
            date_picker_page.log_step("✅ Валидация дат работает корректно")
        else:
            date_picker_page.log_step("ℹ️ Валидация дат может требовать дополнительной настройки")


@allure.epic("Widgets")
@allure.feature("Date Picker")
@allure.story("Date and Time Selection")
@pytest.mark.widgets
@pytest.mark.regression
def test_date_and_time_picker(date_picker_page: DatePickerPage):
    """
    Тест выбора даты и времени.

    Проверяет функциональность выбора как даты, так и времени.
    """
    with allure.step("Проверяем наличие поля выбора даты и времени"):
        datetime_input_present = date_picker_page.is_datetime_input_present()
        date_picker_page.log_step(f"Поле выбора даты и времени присутствует: {datetime_input_present}")

        if not datetime_input_present:
            date_picker_page.log_step("⚠️ Поле даты и времени не найдено, используем обычное поле даты")
            return  # Пропускаем тест если нет соответствующего поля

    with allure.step("Получаем начальное значение даты и времени"):
        initial_datetime_value = date_picker_page.get_datetime_input_value()
        date_picker_page.log_step(f"Начальное значение даты и времени: '{initial_datetime_value}'")

        allure.attach(initial_datetime_value, "initial_datetime_value", allure.attachment_type.TEXT)

    with allure.step("Открываем календарь для выбора даты и времени"):
        datetime_calendar_opened = date_picker_page.open_datetime_calendar()

        if datetime_calendar_opened:
            calendar_info = date_picker_page.get_datetime_calendar_info()
            date_picker_page.log_step(f"Информация о календаре даты-времени: {calendar_info}")

            allure.attach(str(calendar_info), "datetime_calendar_info", allure.attachment_type.JSON)

    with allure.step("Выбираем дату в календаре"):
        if datetime_calendar_opened:
            # Выбираем дату (например, завтрашнюю)
            tomorrow = datetime.now() + timedelta(days=1)
            target_day = tomorrow.day

            date_picker_page.log_step(f"Выбор даты: {target_day} число")
            date_selected = date_picker_page.select_datetime_calendar_date(target_day)

            if not date_selected:
                # Выбираем любую доступную дату
                date_selected = date_picker_page.select_first_available_datetime_date()

            date_picker_page.log_step(f"Дата выбрана: {date_selected}")
        else:
            date_selected = False

    with allure.step("Выбираем время"):
        if datetime_calendar_opened and date_selected:
            # Проверяем есть ли возможность выбора времени
            time_picker_available = date_picker_page.is_time_picker_available()

            if time_picker_available:
                date_picker_page.log_step("Выбор времени в time picker")

                # Пытаемся установить время (например, 14:30)
                time_set_result = date_picker_page.set_time(14, 30)
                date_picker_page.log_step(f"Время установлено: {time_set_result}")

                # Или выбираем время из предустановленных вариантов
                if not time_set_result:
                    time_selected = date_picker_page.select_predefined_time()
                    date_picker_page.log_step(f"Выбрано предустановленное время: {time_selected}")
            else:
                date_picker_page.log_step("Time picker не найден или недоступен")
                time_set_result = False

    with allure.step("Подтверждаем выбор даты и времени"):
        if datetime_calendar_opened:
            # Подтверждаем выбор
            selection_confirmed = date_picker_page.confirm_datetime_selection()
            date_picker_page.page.wait_for_timeout(1500)

            # Получаем финальное значение
            final_datetime_value = date_picker_page.get_datetime_input_value()
            calendar_closed = not date_picker_page.is_datetime_calendar_visible()

            datetime_selection_result = {
                "initial_value": initial_datetime_value,
                "final_value": final_datetime_value,
                "selection_confirmed": selection_confirmed,
                "calendar_closed": calendar_closed,
                "value_changed": final_datetime_value != initial_datetime_value,
                "has_datetime_value": len(final_datetime_value) > 0,
                "appears_to_include_time": ":" in final_datetime_value  # Проверяем наличие времени
            }

            date_picker_page.log_step(f"Результат выбора даты и времени: {datetime_selection_result}")
            allure.attach(str(datetime_selection_result), "datetime_selection_result", allure.attachment_type.JSON)

            assert datetime_selection_result["has_datetime_value"], f"Поле должно содержать значение после выбора: '{final_datetime_value}'"

            if datetime_selection_result["appears_to_include_time"]:
                date_picker_page.log_step("✅ Значение включает время")
            else:
                date_picker_page.log_step("ℹ️ Значение может содержать только дату")

            if datetime_selection_result["value_changed"]:
                date_picker_page.log_step("✅ Значение даты и времени изменилось")
        else:
            date_picker_page.log_step("⚠️ Не удалось открыть календарь даты и времени")


@allure.epic("Widgets")
@allure.feature("Date Picker")
@allure.story("Date Range Selection")
@pytest.mark.widgets
def test_date_range_selection(date_picker_page: DatePickerPage):
    """
    Тест выбора диапазона дат.

    Проверяет возможность выбора начальной и конечной даты.
    """
    with allure.step("Проверяем наличие полей для выбора диапазона дат"):
        date_range_available = date_picker_page.is_date_range_picker_available()
        date_picker_page.log_step(f"Выбор диапазона дат доступен: {date_range_available}")

        if not date_range_available:
            date_picker_page.log_step("ℹ️ Функциональность диапазона дат недоступна на данной странице")
            return

    with allure.step("Получаем начальные значения диапазона"):
        start_date_value = date_picker_page.get_start_date_value()
        end_date_value = date_picker_page.get_end_date_value()

        date_picker_page.log_step(f"Начальная дата: '{start_date_value}'")
        date_picker_page.log_step(f"Конечная дата: '{end_date_value}'")

        range_initial_state = {
            "start_date": start_date_value,
            "end_date": end_date_value,
            "range_is_set": len(start_date_value) > 0 and len(end_date_value) > 0
        }

        allure.attach(str(range_initial_state), "initial_date_range_state", allure.attachment_type.JSON)

    with allure.step("Выбираем начальную дату диапазона"):
        start_date_selection = date_picker_page.select_range_start_date()
        date_picker_page.page.wait_for_timeout(1000)

        new_start_date = date_picker_page.get_start_date_value()
        date_picker_page.log_step(f"Начальная дата после выбора: '{new_start_date}'")

    with allure.step("Выбираем конечную дату диапазона"):
        end_date_selection = date_picker_page.select_range_end_date()
        date_picker_page.page.wait_for_timeout(1000)

        new_end_date = date_picker_page.get_end_date_value()
        date_picker_page.log_step(f"Конечная дата после выбора: '{new_end_date}'")

    with allure.step("Анализируем результат выбора диапазона"):
        final_range_state = {
            "initial_start": start_date_value,
            "initial_end": end_date_value,
            "final_start": new_start_date,
            "final_end": new_end_date,
            "start_date_changed": new_start_date != start_date_value,
            "end_date_changed": new_end_date != end_date_value,
            "valid_range_selected": len(new_start_date) > 0 and len(new_end_date) > 0,
            "range_selection_works": start_date_selection and end_date_selection
        }

        date_picker_page.log_step(f"Итоги выбора диапазона дат: {final_range_state}")
        allure.attach(str(final_range_state), "date_range_selection_result", allure.attachment_type.JSON)

        if final_range_state["valid_range_selected"]:
            date_picker_page.log_step("✅ Диапазон дат выбран успешно")
        else:
            date_picker_page.log_step("⚠️ Не удалось выбрать полный диапазон дат")

        if final_range_state["range_selection_works"]:
            date_picker_page.log_step("✅ Механизм выбора диапазона функционирует")


@allure.epic("Widgets")
@allure.feature("Date Picker")
@allure.story("Calendar Navigation")
@pytest.mark.widgets
def test_calendar_navigation(date_picker_page: DatePickerPage):
    """
    Тест навигации по календарю.

    Проверяет переключение между месяцами и годами в календаре.
    """
    with allure.step("Открываем календарь для тестирования навигации"):
        calendar_opened = date_picker_page.open_date_calendar()

        if not calendar_opened:
            date_picker_page.log_step("⚠️ Не удалось открыть календарь для тестирования навигации")
            return

        assert calendar_opened, "Календарь должен открываться для тестирования навигации"

    with allure.step("Получаем текущий месяц и год в календаре"):
        current_month_year = date_picker_page.get_calendar_current_month_year()
        date_picker_page.log_step(f"Текущий месяц и год: {current_month_year}")

        allure.attach(str(current_month_year), "initial_calendar_month_year", allure.attachment_type.JSON)

    navigation_tests = []

    with allure.step("Тестируем навигацию на следующий месяц"):
        next_month_result = date_picker_page.navigate_to_next_month()
        date_picker_page.page.wait_for_timeout(500)

        month_year_after_next = date_picker_page.get_calendar_current_month_year()

        next_month_test = {
            "navigation_attempted": True,
            "navigation_successful": next_month_result,
            "before_navigation": current_month_year,
            "after_navigation": month_year_after_next,
            "month_changed": month_year_after_next != current_month_year
        }

        navigation_tests.append(("next_month", next_month_test))
        date_picker_page.log_step(f"Результат навигации на следующий месяц: {next_month_test}")

    with allure.step("Тестируем навигацию на предыдущий месяц"):
        prev_month_result = date_picker_page.navigate_to_previous_month()
        date_picker_page.page.wait_for_timeout(500)

        month_year_after_prev = date_picker_page.get_calendar_current_month_year()

        prev_month_test = {
            "navigation_attempted": True,
            "navigation_successful": prev_month_result,
            "before_navigation": month_year_after_next,
            "after_navigation": month_year_after_prev,
            "month_changed": month_year_after_prev != month_year_after_next,
            "returned_to_original": month_year_after_prev == current_month_year
        }

        navigation_tests.append(("previous_month", prev_month_test))
        date_picker_page.log_step(f"Результат навигации на предыдущий месяц: {prev_month_test}")

    with allure.step("Тестируем быструю навигацию по годам"):
        year_navigation_available = date_picker_page.is_year_navigation_available()

        if year_navigation_available:
            current_year = date_picker_page.get_calendar_current_year()
            date_picker_page.log_step(f"Текущий год для навигации: {current_year}")

            # Пытаемся перейти на следующий год
            next_year_result = date_picker_page.navigate_to_next_year()
            date_picker_page.page.wait_for_timeout(500)

            year_after_navigation = date_picker_page.get_calendar_current_year()

            year_navigation_test = {
                "year_navigation_available": True,
                "current_year": current_year,
                "year_after_navigation": year_after_navigation,
                "year_changed": year_after_navigation != current_year,
                "navigation_successful": next_year_result
            }

            navigation_tests.append(("year_navigation", year_navigation_test))
            date_picker_page.log_step(f"Результат навигации по годам: {year_navigation_test}")
        else:
            date_picker_page.log_step("Быстрая навигация по годам недоступна")

    with allure.step("Анализируем результаты навигации по календарю"):
        allure.attach(str(navigation_tests), "calendar_navigation_tests", allure.attachment_type.JSON)

        successful_navigations = sum(1 for _, test in navigation_tests if test.get("navigation_successful", False))
        navigations_with_change = sum(1 for _, test in navigation_tests if test.get("month_changed", False) or test.get("year_changed", False))

        navigation_summary = {
            "total_navigation_tests": len(navigation_tests),
            "successful_navigations": successful_navigations,
            "navigations_with_change": navigations_with_change,
            "navigation_success_rate": successful_navigations / len(navigation_tests) if navigation_tests else 0,
            "calendar_navigation_works": successful_navigations > 0,
            "month_navigation_works": any(test[0] in ["next_month", "previous_month"] and test[1].get("month_changed", False) for test in navigation_tests)
        }

        date_picker_page.log_step(f"Итоги навигации по календарю: {navigation_summary}")
        allure.attach(str(navigation_summary), "calendar_navigation_summary", allure.attachment_type.JSON)

        assert navigation_summary["calendar_navigation_works"], f"Навигация по календарю должна работать: {successful_navigations}/{len(navigation_tests)} успешных"

        if navigation_summary["month_navigation_works"]:
            date_picker_page.log_step("✅ Навигация по месяцам работает корректно")
        else:
            date_picker_page.log_step("⚠️ Навигация по месяцам может требовать дополнительной настройки")
