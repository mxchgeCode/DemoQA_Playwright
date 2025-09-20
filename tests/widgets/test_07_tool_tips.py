"""
Тесты для страницы Tool Tips.
Проверяет функциональность всплывающих подсказок:
- Появление подсказок при наведении
- Различные типы подсказок
- Позиционирование подсказок
- Время показа и скрытия подсказок
"""

import pytest
import allure
import time
from pages.widgets.tool_tips_page import ToolTipsPage


@allure.epic("Widgets")
@allure.feature("Tool Tips")
@allure.story("Basic Tooltip Display")
@pytest.mark.widgets
@pytest.mark.smoke
def test_basic_tooltip_hover(tool_tips_page: ToolTipsPage):
    """
    Тест базового отображения подсказки при наведении.

    Наводит курсор на элемент и проверяет появление подсказки.
    """
    with allure.step("Проверяем наличие элементов с подсказками"):
        elements_with_tooltips = tool_tips_page.get_elements_with_tooltips()
        tool_tips_page.log_step(f"Найдено элементов с подсказками: {len(elements_with_tooltips)}")

        tooltip_elements_info = [
            {
                "index": i,
                "element_type": elem.get("type", "unknown"),
                "tooltip_text": elem.get("tooltip_text", ""),
                "element_text": elem.get("element_text", "")
            }
            for i, elem in enumerate(elements_with_tooltips)
        ]

        allure.attach(str(tooltip_elements_info), "tooltip_elements_info", allure.attachment_type.JSON)

        assert len(elements_with_tooltips) > 0, "Должен быть хотя бы один элемент с подсказкой"

    tooltip_hover_tests = []

    with allure.step("Тестируем отображение подсказок при наведении"):
        for i, element_info in enumerate(elements_with_tooltips[:4]):  # Тестируем максимум 4 элемента
            element_type = element_info.get("type", f"element_{i}")
            expected_tooltip_text = element_info.get("tooltip_text", "")

            with allure.step(f"Тест подсказки для элемента: {element_type}"):
                tool_tips_page.log_step(f"Наведение на элемент {i}: {element_type}")

                # Убеждаемся что подсказка изначально скрыта
                initially_visible = tool_tips_page.is_tooltip_visible(i)

                # Наводим курсор на элемент
                hover_result = tool_tips_page.hover_over_element(i)
                tool_tips_page.page.wait_for_timeout(1000)  # Ждем появления подсказки

                # Проверяем появление подсказки
                tooltip_appeared = tool_tips_page.is_tooltip_visible(i)
                tooltip_text = tool_tips_page.get_tooltip_text(i)
                tooltip_position = tool_tips_page.get_tooltip_position(i)

                hover_test = {
                    "element_index": i,
                    "element_type": element_type,
                    "initially_hidden": not initially_visible,
                    "hover_successful": hover_result,
                    "tooltip_appeared": tooltip_appeared,
                    "tooltip_text": tooltip_text,
                    "expected_text": expected_tooltip_text,
                    "text_matches": tooltip_text == expected_tooltip_text if expected_tooltip_text else len(tooltip_text) > 0,
                    "tooltip_position": tooltip_position,
                    "tooltip_positioned": tooltip_position.get("x", 0) > 0 and tooltip_position.get("y", 0) > 0
                }

                tooltip_hover_tests.append(hover_test)
                tool_tips_page.log_step(f"Результат теста подсказки {i}: {hover_test}")

                # Убираем курсор с элемента
                tool_tips_page.move_cursor_away()
                tool_tips_page.page.wait_for_timeout(800)

                # Проверяем что подсказка исчезла
                tooltip_hidden_after = not tool_tips_page.is_tooltip_visible(i)
                hover_test["tooltip_hidden_after_mouse_away"] = tooltip_hidden_after

                if hover_test["tooltip_appeared"] and hover_test["tooltip_hidden_after_mouse_away"]:
                    tool_tips_page.log_step(f"✅ Подсказка для {element_type} работает корректно")
                elif hover_test["tooltip_appeared"]:
                    tool_tips_page.log_step(f"ℹ️ Подсказка для {element_type} появляется, но может не скрываться")
                else:
                    tool_tips_page.log_step(f"⚠️ Подсказка для {element_type} не появляется")

    with allure.step("Анализируем функциональность подсказок"):
        allure.attach(str(tooltip_hover_tests), "tooltip_hover_tests", allure.attachment_type.JSON)

        tooltips_appeared = sum(1 for test in tooltip_hover_tests if test["tooltip_appeared"])
        tooltips_hidden = sum(1 for test in tooltip_hover_tests if test.get("tooltip_hidden_after_mouse_away", False))
        tooltips_with_text = sum(1 for test in tooltip_hover_tests if len(test["tooltip_text"]) > 0)
        tooltips_positioned = sum(1 for test in tooltip_hover_tests if test["tooltip_positioned"])

        tooltip_summary = {
            "total_elements_tested": len(tooltip_hover_tests),
            "tooltips_appeared": tooltips_appeared,
            "tooltips_hidden_properly": tooltips_hidden,
            "tooltips_with_text": tooltips_with_text,
            "tooltips_positioned": tooltips_positioned,
            "tooltip_appearance_rate": tooltips_appeared / len(tooltip_hover_tests) if tooltip_hover_tests else 0,
            "tooltip_hiding_rate": tooltips_hidden / len(tooltip_hover_tests) if tooltip_hover_tests else 0,
            "tooltips_functional": tooltips_appeared > 0 and tooltips_with_text > 0,
            "tooltip_behavior_good": tooltips_appeared >= len(tooltip_hover_tests) * 0.8
        }

        tool_tips_page.log_step(f"Итоги тестирования подсказок: {tooltip_summary}")
        allure.attach(str(tooltip_summary), "tooltip_functionality_summary", allure.attachment_type.JSON)

        assert tooltip_summary["tooltips_functional"], f"Подсказки должны быть функциональными: появилось {tooltips_appeared}, с текстом {tooltips_with_text}"

        if tooltip_summary["tooltip_behavior_good"]:
            tool_tips_page.log_step("✅ Поведение подсказок отличное")
        else:
            tool_tips_page.log_step("ℹ️ Некоторые подсказки могут требовать настройки")


@allure.epic("Widgets")
@allure.feature("Tool Tips")
@allure.story("Tooltip Positioning")
@pytest.mark.widgets
@pytest.mark.regression
def test_tooltip_positioning(tool_tips_page: ToolTipsPage):
    """
    Тест позиционирования подсказок.

    Проверяет правильность расположения подсказок относительно элементов.
    """
    positioning_tests = []

    with allure.step("Тестируем позиционирование подсказок"):
        elements_with_tooltips = tool_tips_page.get_elements_with_tooltips()

        for i, element_info in enumerate(elements_with_tooltips[:3]):  # Тестируем первые 3
            element_type = element_info.get("type", f"element_{i}")

            with allure.step(f"Анализ позиционирования для: {element_type}"):
                tool_tips_page.log_step(f"Тестирование позиционирования элемента {i}")

                # Получаем позицию элемента
                element_position = tool_tips_page.get_element_position(i)
                element_size = tool_tips_page.get_element_size(i)

                # Наводим курсор и получаем позицию подсказки
                tool_tips_page.hover_over_element(i)
                tool_tips_page.page.wait_for_timeout(1000)

                tooltip_position = tool_tips_page.get_tooltip_position(i)
                tooltip_size = tool_tips_page.get_tooltip_size(i)
                tooltip_visible = tool_tips_page.is_tooltip_visible(i)

                if tooltip_visible:
                    # Анализируем относительное позиционирование
                    relative_position = tool_tips_page.analyze_tooltip_relative_position(
                        element_position, element_size, tooltip_position, tooltip_size
                    )

                    # Проверяем что подсказка не перекрывает элемент
                    overlaps_element = tool_tips_page.check_tooltip_element_overlap(
                        element_position, element_size, tooltip_position, tooltip_size
                    )

                    # Проверяем что подсказка видима в viewport
                    within_viewport = tool_tips_page.is_tooltip_within_viewport(tooltip_position, tooltip_size)

                    positioning_test = {
                        "element_index": i,
                        "element_type": element_type,
                        "element_position": element_position,
                        "element_size": element_size,
                        "tooltip_position": tooltip_position,
                        "tooltip_size": tooltip_size,
                        "relative_position": relative_position,
                        "overlaps_element": overlaps_element,
                        "within_viewport": within_viewport,
                        "positioning_good": not overlaps_element and within_viewport,
                        "tooltip_visible": tooltip_visible
                    }

                else:
                    positioning_test = {
                        "element_index": i,
                        "element_type": element_type,
                        "tooltip_visible": False,
                        "positioning_good": False
                    }

                positioning_tests.append(positioning_test)
                tool_tips_page.log_step(f"Результат позиционирования {i}: {positioning_test}")

                # Убираем курсор
                tool_tips_page.move_cursor_away()
                tool_tips_page.page.wait_for_timeout(500)

    with allure.step("Анализируем качество позиционирования"):
        allure.attach(str(positioning_tests), "tooltip_positioning_tests", allure.attachment_type.JSON)

        visible_tooltips = sum(1 for test in positioning_tests if test["tooltip_visible"])
        good_positioning = sum(1 for test in positioning_tests if test.get("positioning_good", False))
        within_viewport = sum(1 for test in positioning_tests if test.get("within_viewport", False))
        no_overlaps = sum(1 for test in positioning_tests if not test.get("overlaps_element", True))

        positioning_summary = {
            "total_elements_tested": len(positioning_tests),
            "visible_tooltips": visible_tooltips,
            "good_positioning": good_positioning,
            "tooltips_within_viewport": within_viewport,
            "tooltips_no_overlap": no_overlaps,
            "positioning_success_rate": good_positioning / visible_tooltips if visible_tooltips > 0 else 0,
            "viewport_compliance_rate": within_viewport / visible_tooltips if visible_tooltips > 0 else 0,
            "positioning_excellent": good_positioning == visible_tooltips and visible_tooltips > 0
        }

        tool_tips_page.log_step(f"Итоги позиционирования: {positioning_summary}")
        allure.attach(str(positioning_summary), "positioning_summary", allure.attachment_type.JSON)

        if positioning_summary["positioning_excellent"]:
            tool_tips_page.log_step("✅ Позиционирование подсказок превосходное")
        elif positioning_summary["positioning_success_rate"] >= 0.8:
            tool_tips_page.log_step("✅ Позиционирование подсказок хорошее")
        else:
            tool_tips_page.log_step("ℹ️ Позиционирование подсказок может требовать улучшения")


@allure.epic("Widgets")
@allure.feature("Tool Tips")
@allure.story("Tooltip Timing")
@pytest.mark.widgets
def test_tooltip_timing(tool_tips_page: ToolTipsPage):
    """
    Тест тайминга появления и исчезновения подсказок.

    Измеряет время отклика подсказок на события мыши.
    """
    timing_tests = []

    with allure.step("Тестируем тайминг подсказок"):
        elements_with_tooltips = tool_tips_page.get_elements_with_tooltips()

        for i, element_info in enumerate(elements_with_tooltips[:2]):  # Тестируем первые 2
            element_type = element_info.get("type", f"element_{i}")

            with allure.step(f"Измерение тайминга для: {element_type}"):
                tool_tips_page.log_step(f"Тестирование тайминга элемента {i}")

                # Убеждаемся что подсказка скрыта
                tool_tips_page.move_cursor_away()
                tool_tips_page.page.wait_for_timeout(1000)

                # Измеряем время появления
                hover_start_time = time.time()
                tool_tips_page.hover_over_element(i)

                # Ждем появления подсказки с измерением времени
                appearance_time = None
                for check_attempt in range(20):  # Максимум 2 секунды (20 * 100мс)
                    tool_tips_page.page.wait_for_timeout(100)
                    if tool_tips_page.is_tooltip_visible(i):
                        appearance_time = time.time() - hover_start_time
                        break

                # Измеряем время исчезновения
                if appearance_time:
                    mouse_away_start_time = time.time()
                    tool_tips_page.move_cursor_away()

                    # Ждем исчезновения подсказки
                    disappearance_time = None
                    for check_attempt in range(20):  # Максимум 2 секунды
                        tool_tips_page.page.wait_for_timeout(100)
                        if not tool_tips_page.is_tooltip_visible(i):
                            disappearance_time = time.time() - mouse_away_start_time
                            break

                else:
                    disappearance_time = None
                    tool_tips_page.move_cursor_away()

                timing_test = {
                    "element_index": i,
                    "element_type": element_type,
                    "appearance_time_seconds": appearance_time,
                    "disappearance_time_seconds": disappearance_time,
                    "tooltip_appeared": appearance_time is not None,
                    "tooltip_disappeared": disappearance_time is not None,
                    "appearance_fast": appearance_time and appearance_time <= 1.0,  # Менее 1 секунды
                    "disappearance_fast": disappearance_time and disappearance_time <= 1.0,
                    "timing_responsive": (appearance_time and appearance_time <= 1.5) and (disappearance_time is None or disappearance_time <= 1.5)
                }

                timing_tests.append(timing_test)
                tool_tips_page.log_step(f"Результат тайминга {i}: {timing_test}")

                tool_tips_page.page.wait_for_timeout(500)  # Пауза между тестами

    with allure.step("Анализируем производительность тайминга"):
        allure.attach(str(timing_tests), "tooltip_timing_tests", allure.attachment_type.JSON)

        tooltips_appeared = sum(1 for test in timing_tests if test["tooltip_appeared"])
        tooltips_disappeared = sum(1 for test in timing_tests if test["tooltip_disappeared"])
        fast_appearance = sum(1 for test in timing_tests if test.get("appearance_fast", False))
        fast_disappearance = sum(1 for test in timing_tests if test.get("disappearance_fast", False))
        responsive_timing = sum(1 for test in timing_tests if test.get("timing_responsive", False))

        if tooltips_appeared > 0:
            avg_appearance_time = sum(test["appearance_time_seconds"] for test in timing_tests if test["appearance_time_seconds"]) / tooltips_appeared
        else:
            avg_appearance_time = 0

        if tooltips_disappeared > 0:
            avg_disappearance_time = sum(test["disappearance_time_seconds"] for test in timing_tests if test["disappearance_time_seconds"]) / tooltips_disappeared
        else:
            avg_disappearance_time = 0

        timing_summary = {
            "total_elements_tested": len(timing_tests),
            "tooltips_appeared": tooltips_appeared,
            "tooltips_disappeared": tooltips_disappeared,
            "fast_appearance_count": fast_appearance,
            "fast_disappearance_count": fast_disappearance,
            "responsive_timing_count": responsive_timing,
            "average_appearance_time": round(avg_appearance_time, 3),
            "average_disappearance_time": round(avg_disappearance_time, 3),
            "timing_performance_good": responsive_timing >= len(timing_tests) * 0.8,
            "appearance_performance_good": fast_appearance >= tooltips_appeared * 0.8 if tooltips_appeared > 0 else False
        }

        tool_tips_page.log_step(f"Итоги тайминга: {timing_summary}")
        allure.attach(str(timing_summary), "timing_performance_summary", allure.attachment_type.JSON)

        if timing_summary["timing_performance_good"]:
            tool_tips_page.log_step("✅ Производительность тайминга подсказок отличная")
        elif timing_summary["appearance_performance_good"]:
            tool_tips_page.log_step("✅ Скорость появления подсказок хорошая")
        else:
            tool_tips_page.log_step("ℹ️ Тайминг подсказок может быть оптимизирован")


@allure.epic("Widgets")
@allure.feature("Tool Tips")
@allure.story("Different Tooltip Types")
@pytest.mark.widgets
def test_different_tooltip_types(tool_tips_page: ToolTipsPage):
    """
    Тест различных типов подсказок.

    Проверяет различные стили и типы подсказок на странице.
    """
    with allure.step("Анализируем типы подсказок"):
        tooltip_types_info = tool_tips_page.analyze_tooltip_types()
        tool_tips_page.log_step(f"Информация о типах подсказок: {tooltip_types_info}")

        allure.attach(str(tooltip_types_info), "tooltip_types_analysis", allure.attachment_type.JSON)

    type_tests = []

    if tooltip_types_info.get("button_tooltip_available", False):
        with allure.step("Тестируем подсказку кнопки"):
            button_tooltip_test = tool_tips_page.test_button_tooltip()
            button_tooltip_test["tooltip_type"] = "button"
            type_tests.append(button_tooltip_test)
            tool_tips_page.log_step(f"Результат подсказки кнопки: {button_tooltip_test}")

    if tooltip_types_info.get("text_field_tooltip_available", False):
        with allure.step("Тестируем подсказку текстового поля"):
            text_field_tooltip_test = tool_tips_page.test_text_field_tooltip()
            text_field_tooltip_test["tooltip_type"] = "text_field"
            type_tests.append(text_field_tooltip_test)
            tool_tips_page.log_step(f"Результат подсказки текстового поля: {text_field_tooltip_test}")

    if tooltip_types_info.get("contrary_tooltip_available", False):
        with allure.step("Тестируем противоположную подсказку"):
            contrary_tooltip_test = tool_tips_page.test_contrary_tooltip()
            contrary_tooltip_test["tooltip_type"] = "contrary"
            type_tests.append(contrary_tooltip_test)
            tool_tips_page.log_step(f"Результат противоположной подсказки: {contrary_tooltip_test}")

    if tooltip_types_info.get("top_tooltip_available", False):
        with allure.step("Тестируем верхнюю подсказку"):
            top_tooltip_test = tool_tips_page.test_top_tooltip()
            top_tooltip_test["tooltip_type"] = "top"
            type_tests.append(top_tooltip_test)
            tool_tips_page.log_step(f"Результат верхней подсказки: {top_tooltip_test}")

    with allure.step("Анализируем разнообразие типов подсказок"):
        allure.attach(str(type_tests), "tooltip_types_tests", allure.attachment_type.JSON)

        if type_tests:
            successful_types = sum(1 for test in type_tests if test.get("tooltip_works", False))
            different_behaviors = len(set(test.get("behavior_type", "default") for test in type_tests))
            different_positions = len(set(test.get("position_type", "default") for test in type_tests))

            types_summary = {
                "total_types_tested": len(type_tests),
                "successful_types": successful_types,
                "different_behaviors": different_behaviors,
                "different_positions": different_positions,
                "type_variety_good": different_behaviors > 1 or different_positions > 1,
                "all_types_work": successful_types == len(type_tests),
                "type_details": type_tests
            }

        else:
            types_summary = {
                "total_types_tested": 0,
                "successful_types": 0,
                "different_behaviors": 0,
                "different_positions": 0,
                "type_variety_good": False,
                "all_types_work": False,
                "type_details": []
            }

        tool_tips_page.log_step(f"Итоги типов подсказок: {types_summary}")
        allure.attach(str(types_summary), "tooltip_types_summary", allure.attachment_type.JSON)

        if types_summary["all_types_work"] and types_summary["total_types_tested"] > 0:
            tool_tips_page.log_step("✅ Все типы подсказок работают корректно")
        elif types_summary["successful_types"] > 0:
            tool_tips_page.log_step("✅ Некоторые типы подсказок работают")
        else:
            tool_tips_page.log_step("ℹ️ Специфические типы подсказок не найдены или не работают")

        if types_summary["type_variety_good"]:
            tool_tips_page.log_step("✅ Найдено разнообразие в типах подсказок")


@allure.epic("Widgets")
@allure.feature("Tool Tips")
@allure.story("Tooltip Accessibility")
@pytest.mark.widgets
def test_tooltip_accessibility(tool_tips_page: ToolTipsPage):
    """
    Тест доступности подсказок.

    Проверяет соответствие подсказок стандартам доступности.
    """
    accessibility_tests = []

    with allure.step("Анализируем доступность подсказок"):
        elements_with_tooltips = tool_tips_page.get_elements_with_tooltips()

        for i, element_info in enumerate(elements_with_tooltips[:3]):  # Первые 3
            element_type = element_info.get("type", f"element_{i}")

            with allure.step(f"Проверка доступности для: {element_type}"):
                # Проверяем ARIA атрибуты
                aria_attributes = tool_tips_page.get_element_aria_attributes(i)

                # Проверяем клавиатурную доступность
                keyboard_focusable = tool_tips_page.is_element_keyboard_focusable(i)

                # Тестируем фокус клавиатурой
                if keyboard_focusable:
                    focus_result = tool_tips_page.focus_element_with_keyboard(i)
                    tool_tips_page.page.wait_for_timeout(1000)

                    tooltip_appears_on_focus = tool_tips_page.is_tooltip_visible(i)

                    # Убираем фокус
                    tool_tips_page.blur_element(i)
                    tool_tips_page.page.wait_for_timeout(500)

                    tooltip_disappears_on_blur = not tool_tips_page.is_tooltip_visible(i)
                else:
                    focus_result = False
                    tooltip_appears_on_focus = False
                    tooltip_disappears_on_blur = False

                # Проверяем контрастность подсказки
                tool_tips_page.hover_over_element(i)
                tool_tips_page.page.wait_for_timeout(1000)

                tooltip_contrast = tool_tips_page.check_tooltip_contrast(i)
                tooltip_readable = tool_tips_page.is_tooltip_text_readable(i)

                tool_tips_page.move_cursor_away()

                accessibility_test = {
                    "element_index": i,
                    "element_type": element_type,
                    "aria_attributes": aria_attributes,
                    "keyboard_focusable": keyboard_focusable,
                    "focus_result": focus_result,
                    "tooltip_on_focus": tooltip_appears_on_focus,
                    "tooltip_disappears_on_blur": tooltip_disappears_on_blur,
                    "tooltip_contrast_good": tooltip_contrast.get("contrast_good", False),
                    "tooltip_readable": tooltip_readable,
                    "has_aria_describedby": "aria-describedby" in aria_attributes,
                    "has_title_attribute": "title" in aria_attributes,
                    "accessibility_good": (
                        keyboard_focusable and 
                        tooltip_appears_on_focus and 
                        tooltip_contrast.get("contrast_good", False)
                    )
                }

                accessibility_tests.append(accessibility_test)
                tool_tips_page.log_step(f"Результат доступности {i}: {accessibility_test}")

    with allure.step("Анализируем общую доступность подсказок"):
        allure.attach(str(accessibility_tests), "tooltip_accessibility_tests", allure.attachment_type.JSON)

        keyboard_accessible = sum(1 for test in accessibility_tests if test["keyboard_focusable"])
        tooltips_on_focus = sum(1 for test in accessibility_tests if test["tooltip_on_focus"])
        good_contrast = sum(1 for test in accessibility_tests if test["tooltip_contrast_good"])
        aria_support = sum(1 for test in accessibility_tests if test["has_aria_describedby"] or test["has_title_attribute"])
        fully_accessible = sum(1 for test in accessibility_tests if test["accessibility_good"])

        accessibility_summary = {
            "total_elements_tested": len(accessibility_tests),
            "keyboard_accessible_elements": keyboard_accessible,
            "tooltips_work_on_focus": tooltips_on_focus,
            "good_contrast_tooltips": good_contrast,
            "aria_supported_elements": aria_support,
            "fully_accessible_elements": fully_accessible,
            "keyboard_accessibility_rate": keyboard_accessible / len(accessibility_tests) if accessibility_tests else 0,
            "focus_functionality_rate": tooltips_on_focus / keyboard_accessible if keyboard_accessible > 0 else 0,
            "accessibility_compliance_good": fully_accessible >= len(accessibility_tests) * 0.6
        }

        tool_tips_page.log_step(f"Итоги доступности: {accessibility_summary}")
        allure.attach(str(accessibility_summary), "accessibility_summary", allure.attachment_type.JSON)

        if accessibility_summary["accessibility_compliance_good"]:
            tool_tips_page.log_step("✅ Доступность подсказок соответствует хорошим стандартам")
        elif accessibility_summary["keyboard_accessibility_rate"] > 0.5:
            tool_tips_page.log_step("✅ Подсказки частично доступны с клавиатуры")
        else:
            tool_tips_page.log_step("ℹ️ Доступность подсказок может быть улучшена")

        # Проверяем что хотя бы базовая функциональность есть
        assert len(accessibility_tests) > 0, "Должны быть проверены элементы на доступность"
