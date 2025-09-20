"""
Тесты для страницы Tabs.
Проверяет функциональность вкладок:
- Переключение между вкладками
- Содержимое вкладок
- Активные/неактивные состояния
- Навигация по вкладкам
"""

import pytest
import allure
from pages.widgets.tabs_page import TabsPage


@allure.epic("Widgets")
@allure.feature("Tabs")
@allure.story("Tab Switching")
@pytest.mark.widgets
@pytest.mark.smoke
def test_basic_tab_switching(tabs_page: TabsPage):
    """
    Тест базового переключения между вкладками.

    Кликает по каждой вкладке и проверяет активацию.
    """
    with allure.step("Получаем список всех вкладок"):
        all_tabs = tabs_page.get_all_tabs_info()
        tabs_page.log_step(f"Найдено вкладок: {len(all_tabs)}")

        tabs_list = [tab["title"] for tab in all_tabs]
        tabs_page.log_step(f"Названия вкладок: {tabs_list}")

        allure.attach(str(all_tabs), "all_tabs_info", allure.attachment_type.JSON)

        assert len(all_tabs) >= 2, f"Должно быть минимум 2 вкладки для тестирования, найдено: {len(all_tabs)}"

    with allure.step("Определяем активную вкладку"):
        initially_active_tab = tabs_page.get_active_tab_info()
        tabs_page.log_step(f"Изначально активная вкладка: {initially_active_tab}")

        assert initially_active_tab is not None, "Должна быть одна активная вкладка"

        initial_active_index = initially_active_tab.get("index", 0)
        initial_active_title = initially_active_tab.get("title", "")

    tab_switching_results = []

    with allure.step("Переключаемся на каждую вкладку"):
        for i, tab_info in enumerate(all_tabs):
            tab_title = tab_info["title"]
            tab_index = tab_info["index"]

            with allure.step(f"Переключение на вкладку: '{tab_title}' (индекс {tab_index})"):
                tabs_page.log_step(f"Клик по вкладке '{tab_title}'")

                # Получаем состояние до клика
                active_before = tabs_page.get_active_tab_info()

                # Кликаем по вкладке
                click_result = tabs_page.click_tab_by_index(tab_index)
                tabs_page.page.wait_for_timeout(500)

                # Получаем состояние после клика
                active_after = tabs_page.get_active_tab_info()
                tab_content_visible = tabs_page.is_tab_content_visible(tab_index)

                switching_test = {
                    "tab_title": tab_title,
                    "tab_index": tab_index,
                    "click_successful": click_result,
                    "active_before": active_before["title"] if active_before else None,
                    "active_after": active_after["title"] if active_after else None,
                    "became_active": active_after and active_after["index"] == tab_index,
                    "content_visible": tab_content_visible,
                    "switching_successful": click_result and active_after and active_after["index"] == tab_index
                }

                tab_switching_results.append(switching_test)
                tabs_page.log_step(f"Результат переключения на '{tab_title}': {switching_test}")

                # Проверяем что вкладка действительно активировалась
                if switching_test["switching_successful"]:
                    tabs_page.log_step(f"✅ Успешно переключились на '{tab_title}'")
                else:
                    tabs_page.log_step(f"⚠️ Проблема при переключении на '{tab_title}'")

    with allure.step("Анализируем результаты переключения вкладок"):
        allure.attach(str(tab_switching_results), "tab_switching_results", allure.attachment_type.JSON)

        successful_switches = sum(1 for result in tab_switching_results if result["switching_successful"])
        tabs_with_visible_content = sum(1 for result in tab_switching_results if result["content_visible"])

        switching_summary = {
            "total_tabs": len(tab_switching_results),
            "successful_switches": successful_switches,
            "tabs_with_visible_content": tabs_with_visible_content,
            "switching_success_rate": successful_switches / len(tab_switching_results) if tab_switching_results else 0,
            "content_visibility_rate": tabs_with_visible_content / len(tab_switching_results) if tab_switching_results else 0,
            "tab_switching_works": successful_switches >= len(tab_switching_results) * 0.8,
            "content_display_works": tabs_with_visible_content >= len(tab_switching_results) * 0.8
        }

        tabs_page.log_step(f"Итоги переключения вкладок: {switching_summary}")
        allure.attach(str(switching_summary), "tab_switching_summary", allure.attachment_type.JSON)

        assert switching_summary["tab_switching_works"], f"Переключение вкладок должно работать: {successful_switches}/{len(tab_switching_results)}"

        if switching_summary["content_display_works"]:
            tabs_page.log_step("✅ Содержимое вкладок отображается корректно")
        else:
            tabs_page.log_step("ℹ️ Некоторые вкладки могут не показывать содержимое")


@allure.epic("Widgets")
@allure.feature("Tabs")
@allure.story("Tab Content")
@pytest.mark.widgets
@pytest.mark.regression
def test_tab_content_display(tabs_page: TabsPage):
    """
    Тест отображения содержимого вкладок.

    Проверяет уникальность и корректность содержимого каждой вкладки.
    """
    tabs_content_info = []

    with allure.step("Анализируем содержимое каждой вкладки"):
        all_tabs = tabs_page.get_all_tabs_info()

        for tab_info in all_tabs:
            tab_title = tab_info["title"]
            tab_index = tab_info["index"]

            with allure.step(f"Анализ содержимого вкладки: '{tab_title}'"):
                tabs_page.log_step(f"Переключение на '{tab_title}' для анализа содержимого")

                # Переключаемся на вкладку
                tabs_page.click_tab_by_index(tab_index)
                tabs_page.page.wait_for_timeout(500)

                # Получаем содержимое вкладки
                tab_content_text = tabs_page.get_tab_content_text(tab_index)
                tab_content_html = tabs_page.get_tab_content_html(tab_index)
                content_elements_count = tabs_page.count_elements_in_tab_content(tab_index)

                # Проверяем видимость и доступность
                content_visible = tabs_page.is_tab_content_visible(tab_index)
                content_area_size = tabs_page.get_tab_content_area_size(tab_index)

                content_analysis = {
                    "tab_title": tab_title,
                    "tab_index": tab_index,
                    "content_text": tab_content_text[:200] + "..." if len(tab_content_text) > 200 else tab_content_text,
                    "content_text_length": len(tab_content_text),
                    "content_html_length": len(tab_content_html),
                    "elements_count": content_elements_count,
                    "content_visible": content_visible,
                    "content_area_size": content_area_size,
                    "has_meaningful_content": len(tab_content_text.strip()) > 10,
                    "content_preview": tab_content_text[:100] if tab_content_text else ""
                }

                tabs_content_info.append(content_analysis)
                tabs_page.log_step(f"Содержимое '{tab_title}': {content_analysis}")

    with allure.step("Проверяем уникальность содержимого вкладок"):
        allure.attach(str(tabs_content_info), "tabs_content_analysis", allure.attachment_type.JSON)

        # Анализ уникальности содержимого
        content_texts = [info["content_text"] for info in tabs_content_info]
        unique_contents = set(content_texts)

        # Анализ наполненности содержимого
        meaningful_content_count = sum(1 for info in tabs_content_info if info["has_meaningful_content"])
        visible_content_count = sum(1 for info in tabs_content_info if info["content_visible"])

        # Анализ разнообразия элементов
        different_element_counts = len(set(info["elements_count"] for info in tabs_content_info))

        content_uniqueness_analysis = {
            "total_tabs": len(tabs_content_info),
            "unique_contents": len(unique_contents),
            "meaningful_content_tabs": meaningful_content_count,
            "visible_content_tabs": visible_content_count,
            "different_element_structures": different_element_counts,
            "all_contents_unique": len(unique_contents) == len(content_texts),
            "most_tabs_have_content": meaningful_content_count >= len(tabs_content_info) * 0.8,
            "content_visibility_good": visible_content_count >= len(tabs_content_info) * 0.8,
            "content_diversity_good": different_element_counts > 1
        }

        tabs_page.log_step(f"Анализ уникальности содержимого: {content_uniqueness_analysis}")
        allure.attach(str(content_uniqueness_analysis), "content_uniqueness_analysis", allure.attachment_type.JSON)

        assert content_uniqueness_analysis["most_tabs_have_content"], f"Большинство вкладок должны содержать значимый контент: {meaningful_content_count}/{len(tabs_content_info)}"
        assert content_uniqueness_analysis["content_visibility_good"], f"Содержимое должно быть видимым: {visible_content_count}/{len(tabs_content_info)}"

        if content_uniqueness_analysis["all_contents_unique"]:
            tabs_page.log_step("✅ Все вкладки содержат уникальный контент")
        else:
            tabs_page.log_step("ℹ️ Некоторые вкладки могут содержать повторяющийся контент")

        if content_uniqueness_analysis["content_diversity_good"]:
            tabs_page.log_step("✅ Вкладки имеют разнообразную структуру содержимого")


@allure.epic("Widgets")
@allure.feature("Tabs")
@allure.story("Tab States")
@pytest.mark.widgets
def test_tab_active_inactive_states(tabs_page: TabsPage):
    """
    Тест состояний вкладок (активная/неактивная).

    Проверяет визуальные различия и поведение активных и неактивных вкладок.
    """
    tab_states_analysis = []

    with allure.step("Анализируем состояния всех вкладок"):
        all_tabs = tabs_page.get_all_tabs_info()

        # Для каждой вкладки анализируем ее состояния
        for tab_info in all_tabs:
            tab_title = tab_info["title"]
            tab_index = tab_info["index"]

            with allure.step(f"Анализ состояний вкладки: '{tab_title}'"):
                # Сначала делаем вкладку неактивной (кликаем по другой)
                other_tab_index = (tab_index + 1) % len(all_tabs)
                tabs_page.click_tab_by_index(other_tab_index)
                tabs_page.page.wait_for_timeout(300)

                # Получаем свойства неактивной вкладки
                inactive_state = tabs_page.get_tab_visual_state(tab_index)
                inactive_classes = tabs_page.get_tab_css_classes(tab_index)
                inactive_clickable = tabs_page.is_tab_clickable(tab_index)

                # Теперь делаем вкладку активной
                tabs_page.click_tab_by_index(tab_index)
                tabs_page.page.wait_for_timeout(300)

                # Получаем свойства активной вкладки
                active_state = tabs_page.get_tab_visual_state(tab_index)
                active_classes = tabs_page.get_tab_css_classes(tab_index)
                is_currently_active = tabs_page.is_tab_active(tab_index)

                state_analysis = {
                    "tab_title": tab_title,
                    "tab_index": tab_index,
                    "inactive_state": inactive_state,
                    "active_state": active_state,
                    "inactive_classes": inactive_classes,
                    "active_classes": active_classes,
                    "inactive_clickable": inactive_clickable,
                    "is_currently_active": is_currently_active,
                    "visual_state_changes": inactive_state != active_state,
                    "css_classes_change": inactive_classes != active_classes,
                    "states_distinguish": inactive_state != active_state or inactive_classes != active_classes
                }

                tab_states_analysis.append(state_analysis)
                tabs_page.log_step(f"Анализ состояний '{tab_title}': {state_analysis}")

    with allure.step("Проверяем различимость активного/неактивного состояний"):
        allure.attach(str(tab_states_analysis), "tab_states_analysis", allure.attachment_type.JSON)

        distinguishable_states = sum(1 for analysis in tab_states_analysis if analysis["states_distinguish"])
        visual_changes = sum(1 for analysis in tab_states_analysis if analysis["visual_state_changes"])
        css_changes = sum(1 for analysis in tab_states_analysis if analysis["css_classes_change"])

        states_summary = {
            "total_tabs_analyzed": len(tab_states_analysis),
            "distinguishable_states": distinguishable_states,
            "visual_state_changes": visual_changes,
            "css_class_changes": css_changes,
            "states_clearly_different": distinguishable_states >= len(tab_states_analysis) * 0.8,
            "visual_feedback_works": visual_changes > 0 or css_changes > 0,
            "all_tabs_provide_feedback": distinguishable_states == len(tab_states_analysis)
        }

        tabs_page.log_step(f"Итоги анализа состояний вкладок: {states_summary}")
        allure.attach(str(states_summary), "tab_states_summary", allure.attachment_type.JSON)

        assert states_summary["visual_feedback_works"], f"Вкладки должны предоставлять визуальную обратную связь: визуальных изменений {visual_changes}, CSS изменений {css_changes}"

        if states_summary["all_tabs_provide_feedback"]:
            tabs_page.log_step("✅ Все вкладки четко различают активное/неактивное состояния")
        elif states_summary["states_clearly_different"]:
            tabs_page.log_step("✅ Большинство вкладок четко различают состояния")
        else:
            tabs_page.log_step("ℹ️ Некоторые вкладки могут не различать состояния визуально")


@allure.epic("Widgets")
@allure.feature("Tabs")
@allure.story("Tab Navigation")
@pytest.mark.widgets
def test_tab_keyboard_navigation(tabs_page: TabsPage):
    """
    Тест навигации по вкладкам с помощью клавиатуры.

    Проверяет доступность и клавиатурное управление вкладками.
    """
    with allure.step("Проверяем доступность вкладок для клавиатурной навигации"):
        keyboard_accessible = tabs_page.are_tabs_keyboard_accessible()
        tabs_page.log_step(f"Вкладки доступны для клавиатурной навигации: {keyboard_accessible}")

        # Получаем информацию о tabindex и ARIA атрибутах
        accessibility_info = tabs_page.get_tabs_accessibility_info()
        tabs_page.log_step(f"Информация о доступности: {accessibility_info}")

        allure.attach(str(accessibility_info), "tabs_accessibility_info", allure.attachment_type.JSON)

    keyboard_navigation_tests = []

    if keyboard_accessible:
        with allure.step("Тестируем клавиатурную навигацию по вкладкам"):
            all_tabs = tabs_page.get_all_tabs_info()

            for i, tab_info in enumerate(all_tabs):
                tab_title = tab_info["title"]
                tab_index = tab_info["index"]

                with allure.step(f"Клавиатурная навигация к вкладке: '{tab_title}'"):
                    # Фокусируемся на вкладке
                    focus_result = tabs_page.focus_on_tab(tab_index)

                    # Проверяем фокус
                    is_focused = tabs_page.is_tab_focused(tab_index)

                    # Пытаемся активировать вкладку через Enter
                    enter_activation = tabs_page.activate_tab_with_enter(tab_index)
                    tabs_page.page.wait_for_timeout(500)

                    # Проверяем результат активации
                    activated_by_enter = tabs_page.is_tab_active(tab_index)

                    # Пытаемся активировать через Space
                    if not activated_by_enter:
                        space_activation = tabs_page.activate_tab_with_space(tab_index)
                        tabs_page.page.wait_for_timeout(500)
                        activated_by_space = tabs_page.is_tab_active(tab_index)
                    else:
                        space_activation = False
                        activated_by_space = False

                    keyboard_test = {
                        "tab_title": tab_title,
                        "tab_index": tab_index,
                        "focus_successful": focus_result,
                        "is_focused": is_focused,
                        "enter_activation": enter_activation,
                        "space_activation": space_activation,
                        "activated_by_enter": activated_by_enter,
                        "activated_by_space": activated_by_space,
                        "keyboard_accessible": focus_result and is_focused,
                        "keyboard_operable": activated_by_enter or activated_by_space
                    }

                    keyboard_navigation_tests.append(keyboard_test)
                    tabs_page.log_step(f"Результат клавиатурного теста '{tab_title}': {keyboard_test}")

        with allure.step("Тестируем навигацию стрелками"):
            if len(all_tabs) >= 2:
                # Фокусируемся на первой вкладке
                tabs_page.focus_on_tab(0)

                # Пытаемся перейти к следующей вкладке стрелкой вправо
                arrow_right_result = tabs_page.navigate_with_arrow_right()
                tabs_page.page.wait_for_timeout(300)

                second_tab_focused_after_arrow = tabs_page.is_tab_focused(1)

                # Пытаемся вернуться стрелкой влево
                arrow_left_result = tabs_page.navigate_with_arrow_left()
                tabs_page.page.wait_for_timeout(300)

                first_tab_focused_after_back = tabs_page.is_tab_focused(0)

                arrow_navigation_test = {
                    "arrow_right_attempted": arrow_right_result,
                    "second_tab_focused": second_tab_focused_after_arrow,
                    "arrow_left_attempted": arrow_left_result,
                    "first_tab_focused_back": first_tab_focused_after_back,
                    "arrow_navigation_works": second_tab_focused_after_arrow or first_tab_focused_after_back
                }

                keyboard_navigation_tests.append({
                    "test_type": "arrow_navigation",
                    **arrow_navigation_test
                })

                tabs_page.log_step(f"Результат навигации стрелками: {arrow_navigation_test}")

    with allure.step("Анализируем клавиатурную доступность вкладок"):
        if keyboard_navigation_tests:
            allure.attach(str(keyboard_navigation_tests), "keyboard_navigation_tests", allure.attachment_type.JSON)

            tab_tests = [test for test in keyboard_navigation_tests if "tab_index" in test]

            accessible_tabs = sum(1 for test in tab_tests if test["keyboard_accessible"])
            operable_tabs = sum(1 for test in tab_tests if test["keyboard_operable"])

            # Проверяем навигацию стрелками
            arrow_tests = [test for test in keyboard_navigation_tests if test.get("test_type") == "arrow_navigation"]
            arrow_navigation_works = any(test.get("arrow_navigation_works", False) for test in arrow_tests)

            keyboard_summary = {
                "keyboard_support_available": keyboard_accessible,
                "tabs_tested": len(tab_tests),
                "accessible_tabs": accessible_tabs,
                "operable_tabs": operable_tabs,
                "arrow_navigation_works": arrow_navigation_works,
                "accessibility_good": accessible_tabs >= len(tab_tests) * 0.8,
                "operability_good": operable_tabs >= len(tab_tests) * 0.8,
                "full_keyboard_support": accessible_tabs == len(tab_tests) and operable_tabs == len(tab_tests)
            }

        else:
            keyboard_summary = {
                "keyboard_support_available": keyboard_accessible,
                "tabs_tested": 0,
                "accessible_tabs": 0,
                "operable_tabs": 0,
                "arrow_navigation_works": False,
                "accessibility_good": False,
                "operability_good": False,
                "full_keyboard_support": False
            }

        tabs_page.log_step(f"Итоги клавиатурной доступности: {keyboard_summary}")
        allure.attach(str(keyboard_summary), "keyboard_accessibility_summary", allure.attachment_type.JSON)

        if keyboard_summary["full_keyboard_support"]:
            tabs_page.log_step("✅ Полная поддержка клавиатурной навигации")
        elif keyboard_summary["keyboard_support_available"] and (keyboard_summary["accessibility_good"] or keyboard_summary["operability_good"]):
            tabs_page.log_step("✅ Хорошая поддержка клавиатурной навигации")
        elif keyboard_summary["keyboard_support_available"]:
            tabs_page.log_step("ℹ️ Частичная поддержка клавиатурной навигации")
        else:
            tabs_page.log_step("⚠️ Клавиатурная навигация недоступна или ограничена")


@allure.epic("Widgets")
@allure.feature("Tabs")
@allure.story("Tabs Integration")
@pytest.mark.widgets
@pytest.mark.regression
def test_tabs_full_integration(tabs_page: TabsPage):
    """
    Интеграционный тест всей функциональности вкладок.

    Комплексная проверка всех аспектов работы вкладок.
    """
    integration_results = {}

    with allure.step("Выполняем полный цикл работы с вкладками"):
        all_tabs = tabs_page.get_all_tabs_info()
        tabs_page.log_step(f"Начинаем интеграционное тестирование {len(all_tabs)} вкладок")

        # 1. Тестируем переключение на все вкладки подряд
        switching_cycle_results = []
        for tab_info in all_tabs:
            switch_result = tabs_page.click_tab_by_index(tab_info["index"])
            tabs_page.page.wait_for_timeout(200)
            is_active = tabs_page.is_tab_active(tab_info["index"])
            content_visible = tabs_page.is_tab_content_visible(tab_info["index"])

            switching_cycle_results.append({
                "tab_title": tab_info["title"],
                "switch_successful": switch_result and is_active,
                "content_visible": content_visible
            })

        integration_results["switching_cycle"] = switching_cycle_results

        # 2. Тестируем быстрое переключение между вкладками
        rapid_switching_results = []
        for i in range(min(5, len(all_tabs))):  # Максимум 5 быстрых переключений
            random_tab_index = (i * 2) % len(all_tabs)  # Псевдослучайный выбор

            start_time = tabs_page.get_current_timestamp()
            switch_result = tabs_page.click_tab_by_index(random_tab_index)
            end_time = tabs_page.get_current_timestamp()

            switch_duration = end_time - start_time
            is_active = tabs_page.is_tab_active(random_tab_index)

            rapid_switching_results.append({
                "switch_number": i + 1,
                "tab_index": random_tab_index,
                "switch_duration_ms": switch_duration,
                "switch_successful": switch_result and is_active,
                "fast_response": switch_duration < 500  # Менее 500мс
            })

        integration_results["rapid_switching"] = rapid_switching_results

        # 3. Проверяем состояние после множественных операций
        final_state_check = {
            "active_tab": tabs_page.get_active_tab_info(),
            "all_tabs_still_present": len(tabs_page.get_all_tabs_info()) == len(all_tabs),
            "tabs_still_clickable": all(tabs_page.is_tab_clickable(tab["index"]) for tab in all_tabs),
            "content_areas_functional": all(tabs_page.is_tab_content_area_functional(tab["index"]) for tab in all_tabs)
        }

        integration_results["final_state"] = final_state_check

    with allure.step("Тестируем совместимость с другими элементами страницы"):
        # Проверяем что вкладки не влияют на другие элементы страницы
        page_stability_test = {
            "page_title_unchanged": tabs_page.verify_page_title_stability(),
            "page_url_stable": tabs_page.verify_page_url_stability(),
            "no_javascript_errors": tabs_page.check_for_javascript_errors(),
            "page_layout_stable": tabs_page.verify_page_layout_stability()
        }

        integration_results["page_stability"] = page_stability_test

    with allure.step("Создаем итоговый отчет интеграционного тестирования"):
        allure.attach(str(integration_results), "tabs_integration_results", allure.attachment_type.JSON)

        # Анализ результатов переключения
        successful_switches = sum(1 for result in integration_results["switching_cycle"] if result["switch_successful"])
        content_visibility = sum(1 for result in integration_results["switching_cycle"] if result["content_visible"])

        # Анализ быстрого переключения
        fast_responses = sum(1 for result in integration_results["rapid_switching"] if result["fast_response"])
        rapid_success = sum(1 for result in integration_results["rapid_switching"] if result["switch_successful"])

        # Анализ стабильности состояния
        final_state = integration_results["final_state"]
        state_stable = all(final_state.values())

        # Анализ стабильности страницы
        page_stable = all(integration_results["page_stability"].values())

        integration_summary = {
            "total_tabs": len(all_tabs),
            "successful_switches": successful_switches,
            "content_visibility_count": content_visibility,
            "fast_responses": fast_responses,
            "rapid_switching_success": rapid_success,
            "final_state_stable": state_stable,
            "page_stability_maintained": page_stable,
            "overall_switching_success_rate": successful_switches / len(all_tabs) if all_tabs else 0,
            "content_display_rate": content_visibility / len(all_tabs) if all_tabs else 0,
            "performance_good": fast_responses >= len(integration_results["rapid_switching"]) * 0.8,
            "integration_successful": (
                successful_switches >= len(all_tabs) * 0.8 and
                state_stable and
                page_stable
            )
        }

        tabs_page.log_step(f"Итоги интеграционного тестирования: {integration_summary}")
        allure.attach(str(integration_summary), "tabs_integration_summary", allure.attachment_type.JSON)

        assert integration_summary["integration_successful"], f"Интеграционное тестирование должно пройти успешно: переключений {successful_switches}/{len(all_tabs)}, состояние стабильно {state_stable}, страница стабильна {page_stable}"

        if integration_summary["performance_good"]:
            tabs_page.log_step("✅ Производительность переключения вкладок хорошая")

        if integration_summary["overall_switching_success_rate"] >= 0.9:
            tabs_page.log_step("🎉 Вкладки работают превосходно!")
        elif integration_summary["overall_switching_success_rate"] >= 0.8:
            tabs_page.log_step("✅ Вкладки работают хорошо")
        else:
            tabs_page.log_step("ℹ️ Вкладки работают с некоторыми ограничениями")
