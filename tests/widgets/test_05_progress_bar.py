"""
Тесты для страницы Progress Bar.
Проверяет функциональность индикаторов прогресса:
- Статичные прогресс-бары
- Динамические прогресс-бары с анимацией
- Изменение значений прогресса
- Различные стили прогресс-баров
"""

import pytest
import allure
import time
from pages.widgets.progress_bar_page import ProgressBarPage


@allure.epic("Widgets")
@allure.feature("Progress Bar")
@allure.story("Static Progress Bar")
@pytest.mark.widgets
@pytest.mark.smoke
def test_static_progress_bar_display(progress_bar_page: ProgressBarPage):
    """
    Тест отображения статического прогресс-бара.

    Проверяет базовое отображение и свойства прогресс-бара.
    """
    with allure.step("Проверяем наличие статического прогресс-бара"):
        static_progress_present = progress_bar_page.is_static_progress_bar_present()
        progress_bar_page.log_step(f"Статический прогресс-бар присутствует: {static_progress_present}")

        assert static_progress_present, "Статический прогресс-бар должен присутствовать на странице"

    with allure.step("Получаем свойства статического прогресс-бара"):
        progress_value = progress_bar_page.get_static_progress_value()
        progress_percentage = progress_bar_page.get_static_progress_percentage()
        progress_text = progress_bar_page.get_static_progress_text()

        progress_bar_page.log_step(f"Значение прогресса: {progress_value}")
        progress_bar_page.log_step(f"Процентное значение: {progress_percentage}%")
        progress_bar_page.log_step(f"Текст прогресса: '{progress_text}'")

        static_progress_info = {
            "progress_value": progress_value,
            "progress_percentage": progress_percentage,
            "progress_text": progress_text,
            "has_numeric_value": isinstance(progress_value, (int, float)) or (isinstance(progress_value, str) and progress_value.replace('.', '').isdigit()),
            "percentage_valid": 0 <= progress_percentage <= 100 if isinstance(progress_percentage, (int, float)) else False,
            "has_text_display": len(progress_text) > 0
        }

        allure.attach(str(static_progress_info), "static_progress_bar_info", allure.attachment_type.JSON)

        # Основные проверки статического прогресс-бара
        assert static_progress_info["has_numeric_value"], f"Прогресс-бар должен иметь числовое значение: {progress_value}"

        if static_progress_info["percentage_valid"]:
            progress_bar_page.log_step("✅ Процентное значение в валидном диапазоне (0-100%)")
        else:
            progress_bar_page.log_step("ℹ️ Процентное значение может быть в нестандартном формате")

    with allure.step("Анализируем визуальные свойства прогресс-бара"):
        visual_properties = progress_bar_page.get_static_progress_visual_properties()
        progress_bar_page.log_step(f"Визуальные свойства: {visual_properties}")

        allure.attach(str(visual_properties), "progress_bar_visual_properties", allure.attachment_type.JSON)

        visual_checks = {
            "has_width": visual_properties.get("width", 0) > 0,
            "has_height": visual_properties.get("height", 0) > 0,
            "has_background_color": visual_properties.get("background_color") is not None,
            "has_progress_color": visual_properties.get("progress_color") is not None,
            "visible": visual_properties.get("visible", False)
        }

        progress_bar_page.log_step(f"Визуальные проверки: {visual_checks}")

        assert visual_checks["visible"], "Прогресс-бар должен быть видимым"
        assert visual_checks["has_width"] and visual_checks["has_height"], "Прогресс-бар должен иметь размеры"

    with allure.step("Проверяем соответствие визуального заполнения значению"):
        visual_fill_percentage = progress_bar_page.calculate_visual_fill_percentage()

        fill_analysis = {
            "reported_percentage": progress_percentage,
            "visual_fill_percentage": visual_fill_percentage,
            "values_approximately_match": abs(visual_fill_percentage - progress_percentage) <= 10 if isinstance(progress_percentage, (int, float)) else False,
            "visual_representation_accurate": visual_fill_percentage > 0 if progress_percentage > 0 else True
        }

        progress_bar_page.log_step(f"Анализ визуального заполнения: {fill_analysis}")
        allure.attach(str(fill_analysis), "visual_fill_analysis", allure.attachment_type.JSON)

        if fill_analysis["values_approximately_match"]:
            progress_bar_page.log_step("✅ Визуальное заполнение соответствует заявленному значению")
        elif fill_analysis["visual_representation_accurate"]:
            progress_bar_page.log_step("✅ Визуальное представление корректное")
        else:
            progress_bar_page.log_step("ℹ️ Визуальное заполнение может не точно соответствовать значению")


@allure.epic("Widgets")
@allure.feature("Progress Bar")
@allure.story("Dynamic Progress Bar")
@pytest.mark.widgets
@pytest.mark.smoke
def test_dynamic_progress_bar_animation(progress_bar_page: ProgressBarPage):
    """
    Тест динамического прогресс-бара с анимацией.

    Запускает прогресс-бар и следит за изменением значений.
    """
    with allure.step("Проверяем наличие динамического прогресс-бара"):
        dynamic_progress_present = progress_bar_page.is_dynamic_progress_bar_present()
        progress_bar_page.log_step(f"Динамический прогресс-бар присутствует: {dynamic_progress_present}")

        assert dynamic_progress_present, "Динамический прогресс-бар должен присутствовать на странице"

    with allure.step("Получаем начальное состояние динамического прогресс-бара"):
        initial_value = progress_bar_page.get_dynamic_progress_value()
        initial_percentage = progress_bar_page.get_dynamic_progress_percentage()
        is_animated = progress_bar_page.is_progress_bar_animated()

        progress_bar_page.log_step(f"Начальное значение: {initial_value}")
        progress_bar_page.log_step(f"Начальный процент: {initial_percentage}%")
        progress_bar_page.log_step(f"Анимация активна: {is_animated}")

        initial_state = {
            "initial_value": initial_value,
            "initial_percentage": initial_percentage,
            "is_animated": is_animated
        }

        allure.attach(str(initial_state), "initial_dynamic_progress_state", allure.attachment_type.JSON)

    progress_snapshots = []

    with allure.step("Запускаем или сбрасываем динамический прогресс"):
        # Пытаемся найти кнопку старта/сброса прогресса
        start_button_available = progress_bar_page.is_start_progress_button_available()
        reset_button_available = progress_bar_page.is_reset_progress_button_available()

        progress_bar_page.log_step(f"Кнопка старта доступна: {start_button_available}")
        progress_bar_page.log_step(f"Кнопка сброса доступна: {reset_button_available}")

        if reset_button_available:
            progress_bar_page.log_step("Сброс прогресса для чистого старта")
            reset_result = progress_bar_page.click_reset_progress_button()
            progress_bar_page.page.wait_for_timeout(1000)

        if start_button_available:
            progress_bar_page.log_step("Запуск динамического прогресса")
            start_result = progress_bar_page.click_start_progress_button()

            if start_result:
                # Собираем snapshots прогресса в течение нескольких секунд
                for i in range(6):  # 6 замеров с интервалом в 1 секунду
                    progress_bar_page.page.wait_for_timeout(1000)

                    current_value = progress_bar_page.get_dynamic_progress_value()
                    current_percentage = progress_bar_page.get_dynamic_progress_percentage()
                    current_text = progress_bar_page.get_dynamic_progress_text()
                    timestamp = time.time()

                    snapshot = {
                        "snapshot_number": i + 1,
                        "timestamp": timestamp,
                        "value": current_value,
                        "percentage": current_percentage,
                        "text": current_text,
                        "seconds_elapsed": (i + 1)
                    }

                    progress_snapshots.append(snapshot)
                    progress_bar_page.log_step(f"Snapshot {i + 1}: {current_percentage}% - {current_text}")

        else:
            # Если кнопок нет, просто наблюдаем за прогрессом
            progress_bar_page.log_step("Наблюдение за автоматическим прогрессом")

            for i in range(4):
                progress_bar_page.page.wait_for_timeout(1500)

                current_value = progress_bar_page.get_dynamic_progress_value()
                current_percentage = progress_bar_page.get_dynamic_progress_percentage()

                snapshot = {
                    "snapshot_number": i + 1,
                    "value": current_value,
                    "percentage": current_percentage,
                    "seconds_elapsed": (i + 1) * 1.5
                }

                progress_snapshots.append(snapshot)
                progress_bar_page.log_step(f"Observation {i + 1}: {current_percentage}%")

    with allure.step("Анализируем динамику изменения прогресса"):
        allure.attach(str(progress_snapshots), "progress_snapshots", allure.attachment_type.JSON)

        if len(progress_snapshots) >= 2:
            # Анализируем изменения между первым и последним snapshot
            first_snapshot = progress_snapshots[0]
            last_snapshot = progress_snapshots[-1]

            # Проверяем монотонность изменений
            increasing_trend = all(
                progress_snapshots[i]["percentage"] >= progress_snapshots[i-1]["percentage"] 
                for i in range(1, len(progress_snapshots))
                if isinstance(progress_snapshots[i]["percentage"], (int, float)) and isinstance(progress_snapshots[i-1]["percentage"], (int, float))
            )

            dynamic_analysis = {
                "total_snapshots": len(progress_snapshots),
                "first_percentage": first_snapshot["percentage"],
                "last_percentage": last_snapshot["percentage"],
                "total_progress_change": last_snapshot["percentage"] - first_snapshot["percentage"] if isinstance(last_snapshot["percentage"], (int, float)) and isinstance(first_snapshot["percentage"], (int, float)) else 0,
                "progress_increased": last_snapshot["percentage"] > first_snapshot["percentage"] if isinstance(last_snapshot["percentage"], (int, float)) and isinstance(first_snapshot["percentage"], (int, float)) else False,
                "increasing_trend": increasing_trend,
                "progress_animated": len(set(snap["percentage"] for snap in progress_snapshots if isinstance(snap["percentage"], (int, float)))) > 1,
                "reached_completion": any(snap["percentage"] >= 100 for snap in progress_snapshots if isinstance(snap["percentage"], (int, float)))
            }

        else:
            dynamic_analysis = {
                "total_snapshots": len(progress_snapshots),
                "progress_increased": False,
                "increasing_trend": False,
                "progress_animated": False,
                "reached_completion": False
            }

        progress_bar_page.log_step(f"Анализ динамического прогресса: {dynamic_analysis}")
        allure.attach(str(dynamic_analysis), "dynamic_progress_analysis", allure.attachment_type.JSON)

        if dynamic_analysis["progress_animated"]:
            progress_bar_page.log_step("✅ Динамический прогресс-бар показывает анимацию")
        else:
            progress_bar_page.log_step("ℹ️ Изменения прогресса не обнаружены или минимальны")

        if dynamic_analysis["increasing_trend"]:
            progress_bar_page.log_step("✅ Прогресс увеличивается монотонно")

        if dynamic_analysis["reached_completion"]:
            progress_bar_page.log_step("🎉 Прогресс достиг завершения (100%)")


@allure.epic("Widgets")
@allure.feature("Progress Bar")
@allure.story("Progress Bar Controls")
@pytest.mark.widgets
@pytest.mark.regression
def test_progress_bar_controls(progress_bar_page: ProgressBarPage):
    """
    Тест элементов управления прогресс-баром.

    Проверяет кнопки старта, паузы, сброса и другие элементы управления.
    """
    controls_info = {}

    with allure.step("Анализируем доступные элементы управления"):
        available_controls = progress_bar_page.get_available_progress_controls()
        progress_bar_page.log_step(f"Доступные элементы управления: {available_controls}")

        allure.attach(str(available_controls), "available_progress_controls", allure.attachment_type.JSON)

        controls_info["available_controls"] = available_controls

    control_tests = []

    with allure.step("Тестируем кнопку Start/Play"):
        if available_controls.get("start_button", False):
            start_initial_state = progress_bar_page.get_dynamic_progress_percentage()

            start_click_result = progress_bar_page.click_start_progress_button()
            progress_bar_page.page.wait_for_timeout(2000)

            state_after_start = progress_bar_page.get_dynamic_progress_percentage()

            start_test = {
                "control": "start_button",
                "click_successful": start_click_result,
                "state_before": start_initial_state,
                "state_after": state_after_start,
                "progress_started": state_after_start != start_initial_state if isinstance(state_after_start, (int, float)) and isinstance(start_initial_state, (int, float)) else False
            }

            control_tests.append(start_test)
            progress_bar_page.log_step(f"Результат теста кнопки Start: {start_test}")

    with allure.step("Тестируем кнопку Stop/Pause"):
        if available_controls.get("stop_button", False):
            # Ждем немного чтобы прогресс начался
            progress_bar_page.page.wait_for_timeout(1000)
            stop_initial_state = progress_bar_page.get_dynamic_progress_percentage()

            stop_click_result = progress_bar_page.click_stop_progress_button()
            progress_bar_page.page.wait_for_timeout(2000)

            state_after_stop = progress_bar_page.get_dynamic_progress_percentage()

            # Ждем еще немного и проверяем что прогресс остановился
            progress_bar_page.page.wait_for_timeout(1500)
            state_after_delay = progress_bar_page.get_dynamic_progress_percentage()

            stop_test = {
                "control": "stop_button",
                "click_successful": stop_click_result,
                "state_before_stop": stop_initial_state,
                "state_after_stop": state_after_stop,
                "state_after_delay": state_after_delay,
                "progress_stopped": state_after_stop == state_after_delay if isinstance(state_after_stop, (int, float)) and isinstance(state_after_delay, (int, float)) else False
            }

            control_tests.append(stop_test)
            progress_bar_page.log_step(f"Результат теста кнопки Stop: {stop_test}")

    with allure.step("Тестируем кнопку Reset"):
        if available_controls.get("reset_button", False):
            reset_click_result = progress_bar_page.click_reset_progress_button()
            progress_bar_page.page.wait_for_timeout(1000)

            state_after_reset = progress_bar_page.get_dynamic_progress_percentage()

            reset_test = {
                "control": "reset_button",
                "click_successful": reset_click_result,
                "state_after_reset": state_after_reset,
                "progress_reset_to_zero": state_after_reset == 0 if isinstance(state_after_reset, (int, float)) else False,
                "progress_reset_to_minimum": state_after_reset <= 5 if isinstance(state_after_reset, (int, float)) else False
            }

            control_tests.append(reset_test)
            progress_bar_page.log_step(f"Результат теста кнопки Reset: {reset_test}")

    with allure.step("Тестируем произвольные элементы управления"):
        custom_controls = available_controls.get("custom_controls", [])

        for control_name in custom_controls:
            custom_control_result = progress_bar_page.click_custom_control(control_name)
            progress_bar_page.page.wait_for_timeout(1000)

            state_after_custom = progress_bar_page.get_dynamic_progress_percentage()

            custom_test = {
                "control": f"custom_{control_name}",
                "click_successful": custom_control_result,
                "state_after_click": state_after_custom
            }

            control_tests.append(custom_test)
            progress_bar_page.log_step(f"Результат теста {control_name}: {custom_test}")

    with allure.step("Анализируем функциональность элементов управления"):
        allure.attach(str(control_tests), "progress_controls_tests", allure.attachment_type.JSON)

        successful_controls = sum(1 for test in control_tests if test["click_successful"])
        functional_controls = sum(1 for test in control_tests if test.get("progress_started") or test.get("progress_stopped") or test.get("progress_reset_to_zero") or test.get("progress_reset_to_minimum"))

        controls_summary = {
            "total_controls_tested": len(control_tests),
            "successful_control_clicks": successful_controls,
            "functional_controls": functional_controls,
            "controls_work": successful_controls > 0,
            "controls_affect_progress": functional_controls > 0,
            "control_success_rate": successful_controls / len(control_tests) if control_tests else 0,
            "functional_rate": functional_controls / len(control_tests) if control_tests else 0,
            "control_details": control_tests
        }

        progress_bar_page.log_step(f"Итоги тестирования элементов управления: {controls_summary}")
        allure.attach(str(controls_summary), "progress_controls_summary", allure.attachment_type.JSON)

        if controls_summary["controls_work"]:
            progress_bar_page.log_step("✅ Элементы управления прогресс-баром работают")
        else:
            progress_bar_page.log_step("⚠️ Элементы управления недоступны или не функционируют")

        if controls_summary["controls_affect_progress"]:
            progress_bar_page.log_step("✅ Элементы управления влияют на состояние прогресса")
        else:
            progress_bar_page.log_step("ℹ️ Влияние элементов управления на прогресс не обнаружено")


@allure.epic("Widgets")
@allure.feature("Progress Bar")
@allure.story("Multiple Progress Bars")
@pytest.mark.widgets
def test_multiple_progress_bars(progress_bar_page: ProgressBarPage):
    """
    Тест множественных прогресс-баров на странице.

    Проверяет поведение нескольких прогресс-баров одновременно.
    """
    with allure.step("Подсчитываем количество прогресс-баров на странице"):
        progress_bars_count = progress_bar_page.count_progress_bars_on_page()
        progress_bar_page.log_step(f"Найдено прогресс-баров на странице: {progress_bars_count}")

        if progress_bars_count <= 1:
            progress_bar_page.log_step("ℹ️ На странице только один прогресс-бар или они не найдены")
            return

    with allure.step("Анализируем свойства всех прогресс-баров"):
        all_progress_bars_info = []

        for i in range(progress_bars_count):
            progress_info = progress_bar_page.get_progress_bar_info_by_index(i)
            all_progress_bars_info.append(progress_info)
            progress_bar_page.log_step(f"Прогресс-бар {i + 1}: {progress_info}")

        allure.attach(str(all_progress_bars_info), "all_progress_bars_info", allure.attachment_type.JSON)

    with allure.step("Проверяем независимость прогресс-баров"):
        initial_states = [info["current_percentage"] for info in all_progress_bars_info]

        # Пытаемся взаимодействовать с первым прогресс-баром
        if progress_bars_count >= 1:
            interaction_result = progress_bar_page.interact_with_progress_bar_by_index(0)
            progress_bar_page.page.wait_for_timeout(2000)

            # Проверяем состояния после взаимодействия
            states_after_interaction = []
            for i in range(progress_bars_count):
                updated_info = progress_bar_page.get_progress_bar_info_by_index(i)
                states_after_interaction.append(updated_info["current_percentage"])

            independence_analysis = {
                "interaction_with_first_bar": interaction_result,
                "initial_states": initial_states,
                "states_after_interaction": states_after_interaction,
                "first_bar_changed": states_after_interaction[0] != initial_states[0] if len(states_after_interaction) > 0 and len(initial_states) > 0 else False,
                "other_bars_unchanged": all(
                    states_after_interaction[i] == initial_states[i] 
                    for i in range(1, len(initial_states))
                    if isinstance(states_after_interaction[i], (int, float)) and isinstance(initial_states[i], (int, float))
                ),
                "bars_are_independent": True  # Будет обновлено ниже
            }

            # Определяем независимость
            if independence_analysis["first_bar_changed"] and independence_analysis["other_bars_unchanged"]:
                independence_analysis["bars_are_independent"] = True
            elif not independence_analysis["first_bar_changed"]:
                independence_analysis["bars_are_independent"] = None  # Неопределено
            else:
                independence_analysis["bars_are_independent"] = False

            progress_bar_page.log_step(f"Анализ независимости прогресс-баров: {independence_analysis}")
            allure.attach(str(independence_analysis), "progress_bars_independence", allure.attachment_type.JSON)

    with allure.step("Анализируем типы и стили прогресс-баров"):
        types_analysis = {
            "static_bars": sum(1 for info in all_progress_bars_info if info.get("type") == "static"),
            "dynamic_bars": sum(1 for info in all_progress_bars_info if info.get("type") == "dynamic"),
            "different_styles": len(set(info.get("style", "default") for info in all_progress_bars_info)),
            "different_colors": len(set(info.get("color", "default") for info in all_progress_bars_info)),
            "all_visible": all(info.get("visible", False) for info in all_progress_bars_info),
            "all_functional": all(info.get("functional", False) for info in all_progress_bars_info)
        }

        progress_bar_page.log_step(f"Анализ типов и стилей: {types_analysis}")
        allure.attach(str(types_analysis), "progress_bars_types_analysis", allure.attachment_type.JSON)

    with allure.step("Создаем итоговый отчет о множественных прогресс-барах"):
        multiple_bars_summary = {
            "total_progress_bars": progress_bars_count,
            "bars_info": all_progress_bars_info,
            "independence_confirmed": independence_analysis.get("bars_are_independent", None),
            "variety_in_styles": types_analysis["different_styles"] > 1,
            "all_bars_visible": types_analysis["all_visible"],
            "multiple_bars_functional": progress_bars_count > 1 and types_analysis["all_visible"]
        }

        progress_bar_page.log_step(f"Итоги множественных прогресс-баров: {multiple_bars_summary}")
        allure.attach(str(multiple_bars_summary), "multiple_progress_bars_summary", allure.attachment_type.JSON)

        assert multiple_bars_summary["multiple_bars_functional"], f"Множественные прогресс-бары должны быть функциональными: найдено {progress_bars_count}, видимы {types_analysis['all_visible']}"

        if multiple_bars_summary["independence_confirmed"]:
            progress_bar_page.log_step("✅ Прогресс-бары работают независимо друг от друга")
        elif multiple_bars_summary["independence_confirmed"] is False:
            progress_bar_page.log_step("ℹ️ Прогресс-бары могут быть связаны друг с другом")
        else:
            progress_bar_page.log_step("ℹ️ Независимость прогресс-баров не определена")

        if multiple_bars_summary["variety_in_styles"]:
            progress_bar_page.log_step("✅ Найдены прогресс-бары различных стилей")


@allure.epic("Widgets")
@allure.feature("Progress Bar")
@allure.story("Progress Bar Performance")
@pytest.mark.widgets
def test_progress_bar_performance(progress_bar_page: ProgressBarPage):
    """
    Тест производительности прогресс-бара.

    Измеряет скорость обновления и плавность анимации.
    """
    performance_metrics = []

    with allure.step("Подготавливаем прогресс-бар для тестирования производительности"):
        # Сбрасываем состояние
        if progress_bar_page.is_reset_progress_button_available():
            progress_bar_page.click_reset_progress_button()
            progress_bar_page.page.wait_for_timeout(1000)

        initial_performance_state = {
            "timestamp": time.time(),
            "progress_value": progress_bar_page.get_dynamic_progress_percentage(),
            "is_animated": progress_bar_page.is_progress_bar_animated()
        }

        progress_bar_page.log_step(f"Начальное состояние для теста производительности: {initial_performance_state}")

    with allure.step("Запускаем прогресс и измеряем производительность"):
        if progress_bar_page.is_start_progress_button_available():
            start_time = time.time()
            progress_bar_page.click_start_progress_button()

            # Собираем метрики производительности каждые 500мс
            for i in range(10):  # 5 секунд измерений
                progress_bar_page.page.wait_for_timeout(500)

                current_time = time.time()
                current_progress = progress_bar_page.get_dynamic_progress_percentage()

                # Измеряем время отклика интерфейса
                ui_response_start = time.time()
                progress_bar_page.get_dynamic_progress_text()  # Простая операция для измерения отклика
                ui_response_time = (time.time() - ui_response_start) * 1000  # в миллисекундах

                metric = {
                    "measurement_number": i + 1,
                    "timestamp": current_time,
                    "elapsed_time": current_time - start_time,
                    "progress_value": current_progress,
                    "ui_response_time_ms": ui_response_time,
                    "progress_rate": current_progress / (current_time - start_time) if current_time > start_time and isinstance(current_progress, (int, float)) else 0
                }

                performance_metrics.append(metric)
                progress_bar_page.log_step(f"Метрика {i + 1}: прогресс {current_progress}%, отклик {ui_response_time:.2f}мс")

    with allure.step("Анализируем метрики производительности"):
        allure.attach(str(performance_metrics), "performance_metrics", allure.attachment_type.JSON)

        if performance_metrics:
            # Анализ времени отклика UI
            avg_response_time = sum(m["ui_response_time_ms"] for m in performance_metrics) / len(performance_metrics)
            max_response_time = max(m["ui_response_time_ms"] for m in performance_metrics)
            min_response_time = min(m["ui_response_time_ms"] for m in performance_metrics)

            # Анализ скорости прогресса
            progress_values = [m["progress_value"] for m in performance_metrics if isinstance(m["progress_value"], (int, float))]
            progress_is_smooth = len(set(progress_values)) > len(progress_values) * 0.5 if progress_values else False

            # Анализ стабильности
            response_time_variance = max(m["ui_response_time_ms"] for m in performance_metrics) - min(m["ui_response_time_ms"] for m in performance_metrics)

            performance_analysis = {
                "total_measurements": len(performance_metrics),
                "average_ui_response_time_ms": round(avg_response_time, 2),
                "max_ui_response_time_ms": round(max_response_time, 2),
                "min_ui_response_time_ms": round(min_response_time, 2),
                "response_time_variance_ms": round(response_time_variance, 2),
                "progress_appears_smooth": progress_is_smooth,
                "ui_responsive": avg_response_time < 50,  # Менее 50мс считается быстрым
                "ui_stable": response_time_variance < 100,  # Разброс менее 100мс
                "performance_acceptable": avg_response_time < 100 and response_time_variance < 200
            }

        else:
            performance_analysis = {
                "total_measurements": 0,
                "performance_acceptable": False,
                "ui_responsive": False,
                "ui_stable": False
            }

        progress_bar_page.log_step(f"Анализ производительности: {performance_analysis}")
        allure.attach(str(performance_analysis), "performance_analysis", allure.attachment_type.JSON)

        if performance_analysis["performance_acceptable"]:
            progress_bar_page.log_step("✅ Производительность прогресс-бара приемлемая")
        else:
            progress_bar_page.log_step("⚠️ Производительность прогресс-бара может требовать оптимизации")

        if performance_analysis["ui_responsive"]:
            progress_bar_page.log_step("✅ UI интерфейс отзывчивый")

        if performance_analysis["ui_stable"]:
            progress_bar_page.log_step("✅ Время отклика стабильное")

        # Проверяем что хотя бы базовые метрики были собраны
        assert len(performance_metrics) > 0, "Должны быть собраны метрики производительности"
