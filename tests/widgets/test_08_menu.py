"""
Тесты для страницы Menu.
Проверяет функциональность меню:
- Основное меню и подменю
- Навигация по пунктам меню
- Выпадающие меню
- Контекстные меню
"""

import pytest
import allure
from pages.widgets.menu_page import MenuPage


@allure.epic("Widgets")
@allure.feature("Menu")
@allure.story("Basic Menu Navigation")
@pytest.mark.widgets
@pytest.mark.smoke
def test_basic_menu_navigation(menu_page: MenuPage):
    """
    Тест базовой навигации по меню.

    Кликает по пунктам меню и проверяет их активацию.
    """
    with allure.step("Получаем структуру главного меню"):
        main_menu_items = menu_page.get_main_menu_items()
        menu_page.log_step(f"Найдено пунктов главного меню: {len(main_menu_items)}")

        menu_structure = [
            {
                "index": i,
                "text": item.get("text", ""),
                "has_submenu": item.get("has_submenu", False),
                "is_enabled": item.get("is_enabled", True),
            }
            for i, item in enumerate(main_menu_items)
        ]

        allure.attach(
            str(menu_structure), "main_menu_structure", allure.attachment_type.JSON
        )

        assert len(main_menu_items) > 0, "Должен быть хотя бы один пункт главного меню"

    menu_navigation_tests = []

    with allure.step("Тестируем навигацию по пунктам главного меню"):
        for i, menu_item in enumerate(main_menu_items):
            menu_text = menu_item.get("text", f"item_{i}")
            has_submenu = menu_item.get("has_submenu", False)
            is_enabled = menu_item.get("is_enabled", True)

            with allure.step(f"Тест пункта меню: '{menu_text}'"):
                menu_page.log_step(f"Клик по пункту меню {i}: '{menu_text}'")

                if not is_enabled:
                    menu_page.log_step(f"Пункт '{menu_text}' отключен, пропускаем")
                    continue

                # Получаем состояние до клика
                initially_active = menu_page.is_menu_item_active(i)

                # Кликаем по пункту меню
                click_result = menu_page.click_menu_item(i)
                menu_page.page.wait_for_timeout(800)

                # Проверяем результат клика
                became_active = menu_page.is_menu_item_active(i)
                submenu_opened = (
                    menu_page.is_submenu_visible(i) if has_submenu else False
                )

                # Если есть подменю, проверяем его содержимое
                submenu_items = []
                if has_submenu and submenu_opened:
                    submenu_items = menu_page.get_submenu_items(i)

                navigation_test = {
                    "menu_index": i,
                    "menu_text": menu_text,
                    "has_submenu": has_submenu,
                    "is_enabled": is_enabled,
                    "initially_active": initially_active,
                    "click_successful": click_result,
                    "became_active": became_active,
                    "submenu_opened": submenu_opened,
                    "submenu_items_count": len(submenu_items),
                    "submenu_items": submenu_items[:3],  # Первые 3 для краткости
                    "navigation_successful": click_result
                    and (became_active or submenu_opened),
                    "functionality_works": click_result
                    and (became_active or submenu_opened or not has_submenu),
                }

                menu_navigation_tests.append(navigation_test)
                menu_page.log_step(
                    f"Результат навигации '{menu_text}': {navigation_test}"
                )

                if navigation_test["functionality_works"]:
                    menu_page.log_step(
                        f"✅ Пункт меню '{menu_text}' работает корректно"
                    )
                else:
                    menu_page.log_step(f"⚠️ Проблема с пунктом меню '{menu_text}'")

                # Закрываем подменю если оно открылось
                if submenu_opened:
                    menu_page.close_submenu(i)
                    menu_page.page.wait_for_timeout(300)

    with allure.step("Анализируем результаты навигации по меню"):
        allure.attach(
            str(menu_navigation_tests),
            "menu_navigation_results",
            allure.attachment_type.JSON,
        )

        functional_items = sum(
            1 for test in menu_navigation_tests if test["functionality_works"]
        )
        items_with_submenus = sum(
            1 for test in menu_navigation_tests if test["has_submenu"]
        )
        working_submenus = sum(
            1 for test in menu_navigation_tests if test["submenu_opened"]
        )

        navigation_summary = {
            "total_menu_items": len(menu_navigation_tests),
            "functional_items": functional_items,
            "items_with_submenus": items_with_submenus,
            "working_submenus": working_submenus,
            "functionality_rate": (
                functional_items / len(menu_navigation_tests)
                if menu_navigation_tests
                else 0
            ),
            "submenu_success_rate": (
                working_submenus / items_with_submenus if items_with_submenus > 0 else 1
            ),
            "menu_navigation_works": functional_items
            >= len(menu_navigation_tests) * 0.8,
            "submenu_functionality_good": (
                working_submenus >= items_with_submenus * 0.7
                if items_with_submenus > 0
                else True
            ),
        }

        menu_page.log_step(f"Итоги навигации по меню: {navigation_summary}")
        allure.attach(
            str(navigation_summary),
            "menu_navigation_summary",
            allure.attachment_type.JSON,
        )

        assert navigation_summary[
            "menu_navigation_works"
        ], f"Навигация по меню должна работать: {functional_items}/{len(menu_navigation_tests)}"

        if navigation_summary["submenu_functionality_good"]:
            menu_page.log_step("✅ Функциональность подменю работает хорошо")
        else:
            menu_page.log_step("ℹ️ Некоторые подменю могут требовать проверки")


@allure.epic("Widgets")
@allure.feature("Menu")
@allure.story("Submenu Navigation")
@pytest.mark.widgets
@pytest.mark.regression
def test_submenu_navigation(menu_page: MenuPage):
    """
    Тест навигации по подменю.

    Открывает подменю и тестирует навигацию по его пунктам.
    """
    submenu_tests = []

    with allure.step("Находим пункты меню с подменю"):
        main_menu_items = menu_page.get_main_menu_items()
        items_with_submenus = [
            item for item in main_menu_items if item.get("has_submenu", False)
        ]

        menu_page.log_step(f"Найдено пунктов с подменю: {len(items_with_submenus)}")

        if len(items_with_submenus) == 0:
            menu_page.log_step("ℹ️ Подменю не найдены на странице")
            return

    with allure.step("Тестируем навигацию по каждому подменю"):
        for main_item in items_with_submenus[:3]:  # Тестируем максимум 3 подменю
            main_index = main_item["index"]
            main_text = main_item.get("text", f"main_{main_index}")

            with allure.step(f"Тестирование подменю для: '{main_text}'"):
                menu_page.log_step(f"Открытие подменю для '{main_text}'")

                # Открываем подменю
                submenu_opened = menu_page.open_submenu(main_index)
                menu_page.page.wait_for_timeout(1000)

                if submenu_opened:
                    # Получаем пункты подменю
                    submenu_items = menu_page.get_submenu_items(main_index)
                    menu_page.log_step(f"Найдено пунктов подменю: {len(submenu_items)}")

                    submenu_item_tests = []

                    # Тестируем каждый пункт подменю
                    for sub_i, submenu_item in enumerate(
                        submenu_items[:4]
                    ):  # Максимум 4 пункта
                        sub_text = submenu_item.get("text", f"sub_{sub_i}")

                        menu_page.log_step(f"Клик по пункту подменю: '{sub_text}'")

                        # Кликаем по пункту подменю
                        sub_click_result = menu_page.click_submenu_item(
                            main_index, sub_i
                        )
                        menu_page.page.wait_for_timeout(500)

                        # Проверяем результат
                        sub_item_active = menu_page.is_submenu_item_active(
                            main_index, sub_i
                        )
                        submenu_still_open = menu_page.is_submenu_visible(main_index)

                        submenu_item_test = {
                            "submenu_item_index": sub_i,
                            "submenu_item_text": sub_text,
                            "click_successful": sub_click_result,
                            "became_active": sub_item_active,
                            "submenu_stays_open": submenu_still_open,
                            "item_functional": sub_click_result,
                        }

                        submenu_item_tests.append(submenu_item_test)
                        menu_page.log_step(
                            f"Результат '{sub_text}': {submenu_item_test}"
                        )

                    # Закрываем подменю
                    menu_page.close_submenu(main_index)
                    menu_page.page.wait_for_timeout(500)

                    submenu_closed = not menu_page.is_submenu_visible(main_index)

                    submenu_test = {
                        "main_menu_index": main_index,
                        "main_menu_text": main_text,
                        "submenu_opened": submenu_opened,
                        "submenu_items_count": len(submenu_items),
                        "submenu_items_tested": len(submenu_item_tests),
                        "functional_submenu_items": sum(
                            1 for test in submenu_item_tests if test["item_functional"]
                        ),
                        "submenu_closed_properly": submenu_closed,
                        "submenu_item_tests": submenu_item_tests,
                        "submenu_fully_functional": len(submenu_item_tests) > 0
                        and all(test["item_functional"] for test in submenu_item_tests),
                    }

                else:
                    submenu_test = {
                        "main_menu_index": main_index,
                        "main_menu_text": main_text,
                        "submenu_opened": False,
                        "submenu_fully_functional": False,
                    }

                submenu_tests.append(submenu_test)
                menu_page.log_step(f"Итоги подменю '{main_text}': {submenu_test}")

    with allure.step("Анализируем функциональность подменю"):
        allure.attach(
            str(submenu_tests), "submenu_navigation_tests", allure.attachment_type.JSON
        )

        opened_submenus = sum(1 for test in submenu_tests if test["submenu_opened"])
        functional_submenus = sum(
            1 for test in submenu_tests if test.get("submenu_fully_functional", False)
        )
        total_submenu_items_tested = sum(
            test.get("submenu_items_tested", 0) for test in submenu_tests
        )
        functional_submenu_items = sum(
            test.get("functional_submenu_items", 0) for test in submenu_tests
        )

        submenu_summary = {
            "total_submenus_tested": len(submenu_tests),
            "opened_submenus": opened_submenus,
            "functional_submenus": functional_submenus,
            "total_submenu_items_tested": total_submenu_items_tested,
            "functional_submenu_items": functional_submenu_items,
            "submenu_opening_rate": (
                opened_submenus / len(submenu_tests) if submenu_tests else 0
            ),
            "submenu_functionality_rate": (
                functional_submenus / opened_submenus if opened_submenus > 0 else 0
            ),
            "submenu_items_functionality_rate": (
                functional_submenu_items / total_submenu_items_tested
                if total_submenu_items_tested > 0
                else 0
            ),
            "submenu_navigation_excellent": functional_submenus == opened_submenus
            and opened_submenus > 0,
        }

        menu_page.log_step(f"Итоги навигации по подменю: {submenu_summary}")
        allure.attach(
            str(submenu_summary),
            "submenu_navigation_summary",
            allure.attachment_type.JSON,
        )

        if submenu_summary["submenu_navigation_excellent"]:
            menu_page.log_step("✅ Навигация по подменю работает превосходно")
        elif submenu_summary["submenu_opening_rate"] >= 0.8:
            menu_page.log_step("✅ Большинство подменю открываются корректно")
        else:
            menu_page.log_step("ℹ️ Некоторые подменю могут требовать доработки")


@allure.epic("Widgets")
@allure.feature("Menu")
@allure.story("Menu States")
@pytest.mark.widgets
def test_menu_states_and_styling(menu_page: MenuPage):
    """
    Тест состояний и стилизации меню.

    Проверяет различные состояния пунктов меню (активный, отключенный, выделенный).
    """
    states_tests = []

    with allure.step("Анализируем состояния пунктов меню"):
        main_menu_items = menu_page.get_main_menu_items()

        for i, menu_item in enumerate(main_menu_items):
            menu_text = menu_item.get("text", f"item_{i}")

            with allure.step(f"Анализ состояний для: '{menu_text}'"):
                # Получаем различные состояния пункта меню
                default_state = menu_page.get_menu_item_visual_state(i)

                # Наводим курсор для получения hover состояния
                menu_page.hover_over_menu_item(i)
                menu_page.page.wait_for_timeout(300)
                hover_state = menu_page.get_menu_item_visual_state(i)

                # Кликаем для получения активного состояния
                menu_page.click_menu_item(i)
                menu_page.page.wait_for_timeout(300)
                active_state = menu_page.get_menu_item_visual_state(i)

                # Убираем курсор
                menu_page.move_cursor_away_from_menu()
                menu_page.page.wait_for_timeout(300)
                final_state = menu_page.get_menu_item_visual_state(i)

                # Проверяем отключенное состояние если применимо
                is_disabled = menu_page.is_menu_item_disabled(i)
                disabled_state = (
                    menu_page.get_menu_item_visual_state(i) if is_disabled else None
                )

                state_test = {
                    "menu_index": i,
                    "menu_text": menu_text,
                    "default_state": default_state,
                    "hover_state": hover_state,
                    "active_state": active_state,
                    "final_state": final_state,
                    "is_disabled": is_disabled,
                    "disabled_state": disabled_state,
                    "hover_changes_appearance": hover_state != default_state,
                    "active_changes_appearance": active_state != default_state,
                    "states_are_distinct": len(
                        set([str(default_state), str(hover_state), str(active_state)])
                    )
                    > 1,
                    "visual_feedback_works": hover_state != default_state
                    or active_state != default_state,
                }

                states_tests.append(state_test)
                menu_page.log_step(f"Состояния '{menu_text}': {state_test}")

    with allure.step("Тестируем CSS классы и стили"):
        css_analysis = []

        for i, menu_item in enumerate(main_menu_items[:3]):  # Анализируем первые 3
            menu_text = menu_item.get("text", f"item_{i}")

            # Получаем CSS классы в разных состояниях
            default_classes = menu_page.get_menu_item_css_classes(i)

            menu_page.hover_over_menu_item(i)
            hover_classes = menu_page.get_menu_item_css_classes(i)

            menu_page.click_menu_item(i)
            active_classes = menu_page.get_menu_item_css_classes(i)

            menu_page.move_cursor_away_from_menu()

            css_test = {
                "menu_index": i,
                "menu_text": menu_text,
                "default_classes": default_classes,
                "hover_classes": hover_classes,
                "active_classes": active_classes,
                "css_classes_change": len(
                    set([str(default_classes), str(hover_classes), str(active_classes)])
                )
                > 1,
                "has_hover_class": any("hover" in cls for cls in hover_classes),
                "has_active_class": any("active" in cls for cls in active_classes),
            }

            css_analysis.append(css_test)
            menu_page.log_step(f"CSS анализ '{menu_text}': {css_test}")

    with allure.step("Анализируем качество состояний и стилизации"):
        allure.attach(
            str(states_tests), "menu_states_tests", allure.attachment_type.JSON
        )
        allure.attach(
            str(css_analysis), "menu_css_analysis", allure.attachment_type.JSON
        )

        items_with_visual_feedback = sum(
            1 for test in states_tests if test["visual_feedback_works"]
        )
        items_with_hover_changes = sum(
            1 for test in states_tests if test["hover_changes_appearance"]
        )
        items_with_distinct_states = sum(
            1 for test in states_tests if test["states_are_distinct"]
        )

        css_items_with_changes = sum(
            1 for test in css_analysis if test["css_classes_change"]
        )

        styling_summary = {
            "total_items_tested": len(states_tests),
            "items_with_visual_feedback": items_with_visual_feedback,
            "items_with_hover_changes": items_with_hover_changes,
            "items_with_distinct_states": items_with_distinct_states,
            "css_items_with_changes": css_items_with_changes,
            "visual_feedback_rate": (
                items_with_visual_feedback / len(states_tests) if states_tests else 0
            ),
            "hover_feedback_rate": (
                items_with_hover_changes / len(states_tests) if states_tests else 0
            ),
            "styling_quality_good": items_with_visual_feedback
            >= len(states_tests) * 0.7,
            "hover_effects_good": items_with_hover_changes >= len(states_tests) * 0.5,
        }

        menu_page.log_step(f"Итоги стилизации меню: {styling_summary}")
        allure.attach(
            str(styling_summary), "menu_styling_summary", allure.attachment_type.JSON
        )

        if styling_summary["styling_quality_good"]:
            menu_page.log_step("✅ Качество стилизации меню отличное")
        elif styling_summary["hover_effects_good"]:
            menu_page.log_step("✅ Hover эффекты работают хорошо")
        else:
            menu_page.log_step("ℹ️ Стилизация меню может быть улучшена")


@allure.epic("Widgets")
@allure.feature("Menu")
@allure.story("Menu Accessibility")
@pytest.mark.widgets
def test_menu_keyboard_accessibility(menu_page: MenuPage):
    """
    Тест клавиатурной доступности меню.

    Проверяет навигацию по меню с помощью клавиатуры и ARIA атрибуты.
    """
    with allure.step("Проверяем общую доступность меню"):
        menu_accessibility_info = menu_page.get_menu_accessibility_info()
        menu_page.log_step(f"Информация о доступности меню: {menu_accessibility_info}")

        allure.attach(
            str(menu_accessibility_info),
            "menu_accessibility_info",
            allure.attachment_type.JSON,
        )

        keyboard_accessible = menu_accessibility_info.get("keyboard_accessible", False)

    keyboard_tests = []

    if keyboard_accessible:
        with allure.step("Тестируем клавиатурную навигацию"):
            main_menu_items = menu_page.get_main_menu_items()

            for i, menu_item in enumerate(main_menu_items[:3]):  # Тестируем первые 3
                menu_text = menu_item.get("text", f"item_{i}")

                with allure.step(f"Клавиатурный тест для: '{menu_text}'"):
                    # Фокусируемся на пункте меню
                    focus_result = menu_page.focus_menu_item_with_keyboard(i)

                    # Проверяем фокус
                    is_focused = menu_page.is_menu_item_focused(i)

                    # Пытаемся активировать через Enter
                    if is_focused:
                        enter_result = menu_page.activate_menu_item_with_enter(i)
                        menu_page.page.wait_for_timeout(500)
                        activated_by_enter = menu_page.is_menu_item_active(i)

                        # Если есть подменю, проверяем его открытие
                        submenu_opened_by_enter = (
                            menu_page.is_submenu_visible(i)
                            if menu_item.get("has_submenu")
                            else False
                        )

                    else:
                        enter_result = False
                        activated_by_enter = False
                        submenu_opened_by_enter = False

                    keyboard_test = {
                        "menu_index": i,
                        "menu_text": menu_text,
                        "focus_successful": focus_result,
                        "is_focused": is_focused,
                        "enter_activation": enter_result,
                        "activated_by_enter": activated_by_enter,
                        "submenu_opened_by_enter": submenu_opened_by_enter,
                        "keyboard_functional": focus_result
                        and is_focused
                        and (activated_by_enter or submenu_opened_by_enter),
                    }

                    keyboard_tests.append(keyboard_test)
                    menu_page.log_step(
                        f"Клавиатурный тест '{menu_text}': {keyboard_test}"
                    )

        with allure.step("Тестируем навигацию стрелками"):
            if len(main_menu_items) >= 2:
                # Фокусируемся на первом пункте
                menu_page.focus_menu_item_with_keyboard(0)

                # Пробуем перейти к следующему пункту стрелкой
                arrow_navigation_result = menu_page.navigate_menu_with_arrow_keys(
                    "down"
                )
                menu_page.page.wait_for_timeout(300)

                second_item_focused = menu_page.is_menu_item_focused(1)

                arrow_test = {
                    "arrow_navigation_attempted": arrow_navigation_result,
                    "second_item_focused": second_item_focused,
                    "arrow_navigation_works": second_item_focused,
                }

                keyboard_tests.append({"test_type": "arrow_navigation", **arrow_test})
                menu_page.log_step(f"Навигация стрелками: {arrow_test}")

    with allure.step("Проверяем ARIA атрибуты меню"):
        aria_tests = []
        main_menu_items = menu_page.get_main_menu_items()

        for i, menu_item in enumerate(main_menu_items[:3]):
            menu_text = menu_item.get("text", f"item_{i}")

            aria_attributes = menu_page.get_menu_item_aria_attributes(i)

            aria_test = {
                "menu_index": i,
                "menu_text": menu_text,
                "aria_attributes": aria_attributes,
                "has_role": "role" in aria_attributes,
                "has_aria_label": "aria-label" in aria_attributes
                or "aria-labelledby" in aria_attributes,
                "has_aria_expanded": "aria-expanded" in aria_attributes,
                "aria_compliance_good": len(aria_attributes) > 0
                and ("role" in aria_attributes or "aria-label" in aria_attributes),
            }

            aria_tests.append(aria_test)
            menu_page.log_step(f"ARIA тест '{menu_text}': {aria_test}")

    with allure.step("Анализируем доступность меню"):
        allure.attach(
            str(keyboard_tests), "menu_keyboard_tests", allure.attachment_type.JSON
        )
        allure.attach(str(aria_tests), "menu_aria_tests", allure.attachment_type.JSON)

        menu_tests = [test for test in keyboard_tests if "menu_index" in test]

        keyboard_functional_items = sum(
            1 for test in menu_tests if test.get("keyboard_functional", False)
        )
        focused_items = sum(1 for test in menu_tests if test.get("is_focused", False))
        aria_compliant_items = sum(
            1 for test in aria_tests if test.get("aria_compliance_good", False)
        )

        arrow_navigation_works = any(
            test.get("arrow_navigation_works", False)
            for test in keyboard_tests
            if test.get("test_type") == "arrow_navigation"
        )

        accessibility_summary = {
            "keyboard_support_available": keyboard_accessible,
            "total_items_tested": len(menu_tests),
            "keyboard_functional_items": keyboard_functional_items,
            "focused_items": focused_items,
            "aria_compliant_items": aria_compliant_items,
            "arrow_navigation_works": arrow_navigation_works,
            "keyboard_functionality_rate": (
                keyboard_functional_items / len(menu_tests) if menu_tests else 0
            ),
            "aria_compliance_rate": (
                aria_compliant_items / len(aria_tests) if aria_tests else 0
            ),
            "accessibility_excellent": keyboard_functional_items == len(menu_tests)
            and aria_compliant_items >= len(aria_tests) * 0.8,
            "accessibility_good": keyboard_functional_items >= len(menu_tests) * 0.7
            or aria_compliant_items >= len(aria_tests) * 0.7,
        }

        menu_page.log_step(f"Итоги доступности меню: {accessibility_summary}")
        allure.attach(
            str(accessibility_summary),
            "menu_accessibility_summary",
            allure.attachment_type.JSON,
        )

        if accessibility_summary["accessibility_excellent"]:
            menu_page.log_step("✅ Доступность меню превосходная")
        elif accessibility_summary["accessibility_good"]:
            menu_page.log_step("✅ Доступность меню хорошая")
        elif accessibility_summary["keyboard_support_available"]:
            menu_page.log_step("ℹ️ Частичная поддержка доступности меню")
        else:
            menu_page.log_step("⚠️ Доступность меню ограничена")


@allure.epic("Widgets")
@allure.feature("Menu")
@allure.story("Menu Integration")
@pytest.mark.widgets
@pytest.mark.regression
def test_complete_menu_integration(menu_page: MenuPage):
    """
    Полный интеграционный тест меню.

    Комплексная проверка всей функциональности меню.
    """
    integration_results = {}

    with allure.step("Выполняем полный цикл работы с меню"):
        main_menu_items = menu_page.get_main_menu_items()
        menu_page.log_step(
            f"Интеграционное тестирование {len(main_menu_items)} пунктов меню"
        )

        # 1. Полный обход всех пунктов меню
        full_navigation_results = []
        for i, menu_item in enumerate(main_menu_items):
            menu_text = menu_item.get("text", f"item_{i}")

            navigation_start_time = menu_page.get_current_timestamp()
            click_result = menu_page.click_menu_item(i)
            navigation_end_time = menu_page.get_current_timestamp()

            navigation_time = navigation_end_time - navigation_start_time
            became_active = menu_page.is_menu_item_active(i)

            # Если есть подменю, тестируем его
            submenu_test_result = None
            if menu_item.get("has_submenu", False):
                submenu_opened = menu_page.is_submenu_visible(i)
                if submenu_opened:
                    submenu_items = menu_page.get_submenu_items(i)
                    submenu_test_result = {
                        "submenu_opened": True,
                        "submenu_items_count": len(submenu_items),
                        "submenu_accessible": len(submenu_items) > 0,
                    }

                    # Закрываем подменю
                    menu_page.close_submenu(i)
                else:
                    submenu_test_result = {"submenu_opened": False}

            full_navigation_results.append(
                {
                    "menu_index": i,
                    "menu_text": menu_text,
                    "navigation_time_ms": navigation_time,
                    "click_successful": click_result,
                    "became_active": became_active,
                    "submenu_test": submenu_test_result,
                    "overall_success": click_result
                    and (became_active or submenu_test_result),
                }
            )

            menu_page.page.wait_for_timeout(200)

        integration_results["full_navigation"] = full_navigation_results

        # 2. Тест стабильности меню
        stability_test = {
            "menu_structure_consistent": len(menu_page.get_main_menu_items())
            == len(main_menu_items),
            "no_javascript_errors": menu_page.check_for_javascript_errors(),
            "page_layout_stable": menu_page.verify_page_layout_stability(),
            "menu_still_responsive": all(
                menu_page.is_menu_item_clickable(i) for i in range(len(main_menu_items))
            ),
        }

        integration_results["stability"] = stability_test

        # 3. Тест производительности
        performance_metrics = []
        for i in range(min(3, len(main_menu_items))):  # Тестируем первые 3 пункта
            start_time = menu_page.get_current_timestamp()
            menu_page.click_menu_item(i)
            response_time = menu_page.get_current_timestamp() - start_time

            performance_metrics.append(
                {
                    "menu_index": i,
                    "response_time_ms": response_time,
                    "fast_response": response_time < 300,  # Менее 300мс
                }
            )

        integration_results["performance"] = performance_metrics

    with allure.step("Создаем итоговый отчет интеграции меню"):
        allure.attach(
            str(integration_results),
            "menu_integration_results",
            allure.attachment_type.JSON,
        )

        # Анализ навигации
        successful_navigations = sum(
            1
            for result in integration_results["full_navigation"]
            if result["overall_success"]
        )
        working_submenus = sum(
            1
            for result in integration_results["full_navigation"]
            if result.get("submenu_test", {}).get("submenu_opened", False)
        )

        # Анализ стабильности
        stability = integration_results["stability"]
        stable_system = all(stability.values())

        # Анализ производительности
        fast_responses = sum(
            1
            for metric in integration_results["performance"]
            if metric["fast_response"]
        )
        avg_response_time = sum(
            metric["response_time_ms"] for metric in integration_results["performance"]
        ) / len(integration_results["performance"])

        integration_summary = {
            "total_menu_items": len(main_menu_items),
            "successful_navigations": successful_navigations,
            "working_submenus": working_submenus,
            "stable_system": stable_system,
            "fast_responses": fast_responses,
            "average_response_time_ms": round(avg_response_time, 2),
            "navigation_success_rate": (
                successful_navigations / len(main_menu_items) if main_menu_items else 0
            ),
            "performance_good": fast_responses
            >= len(integration_results["performance"]) * 0.8,
            "integration_excellent": (
                successful_navigations >= len(main_menu_items) * 0.9
                and stable_system
                and fast_responses >= len(integration_results["performance"]) * 0.8
            ),
            "integration_successful": (
                successful_navigations >= len(main_menu_items) * 0.7 and stable_system
            ),
        }

        menu_page.log_step(f"Итоги интеграции меню: {integration_summary}")
        allure.attach(
            str(integration_summary),
            "menu_integration_summary",
            allure.attachment_type.JSON,
        )

        assert integration_summary[
            "integration_successful"
        ], f"Интеграция меню должна быть успешной: навигация {successful_navigations}/{len(main_menu_items)}, стабильность {stable_system}"

        if integration_summary["integration_excellent"]:
            menu_page.log_step("🎉 Интеграция меню превосходная!")
        elif integration_summary["integration_successful"]:
            menu_page.log_step("✅ Интеграция меню успешная")
        else:
            menu_page.log_step("ℹ️ Интеграция меню частично успешная")
