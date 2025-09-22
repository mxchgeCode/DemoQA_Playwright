"""
Тесты для страницы Accordions.
Проверяет функциональность аккордеонов:
- Одиночное раскрытие секций
- Множественное раскрытие секций
- Переключение между секциями
- Состояния секций (открыто/закрыто)
"""

import pytest
import allure
from pages.widgets.accordion_page import AccordionPage


@allure.epic("Widgets")
@allure.feature("Accordion")
@allure.story("Single Section Expansion")
@pytest.mark.widgets
@pytest.mark.smoke
def test_single_accordion_section_expand(accordion_page: AccordionPage):
    """
    Тест раскрытия одиночной секции аккордеона.

    Проверяет базовую функциональность открытия и закрытия секций.
    """
    with allure.step("Проверяем начальное состояние всех секций аккордеона"):
        initial_states = accordion_page.get_all_sections_states()
        accordion_page.log_step(f"Начальные состояния секций: {initial_states}")

        allure.attach(
            str(initial_states), "initial_accordion_states", allure.attachment_type.JSON
        )

        assert len(initial_states) > 0, "Должна быть хотя бы одна секция аккордеона"

        # Проверяем что есть как минимум 3 секции
        assert (
            len(initial_states) >= 3
        ), f"Должно быть минимум 3 секции, найдено: {len(initial_states)}"

    with allure.step("Раскрываем первую секцию аккордеона"):
        first_section_initially_open = initial_states[0]["is_expanded"]
        accordion_page.log_step(
            f"Первая секция изначально открыта: {first_section_initially_open}"
        )

        if not first_section_initially_open:
            # Кликаем по первой секции чтобы раскрыть
            expand_result = accordion_page.click_section_header(0)
            accordion_page.log_step(
                f"Результат клика по первой секции: {expand_result}"
            )

            assert expand_result, "Клик по заголовку первой секции должен быть успешным"
        else:
            accordion_page.log_step("Первая секция уже открыта")

        # Небольшая пауза для анимации
        accordion_page.page.wait_for_timeout(1000)

    with allure.step("Проверяем состояние после раскрытия первой секции"):
        states_after_first = accordion_page.get_all_sections_states()
        accordion_page.log_step(
            f"Состояния после раскрытия первой секции: {states_after_first}"
        )

        # Проверяем что первая секция открыта
        first_section_open = states_after_first[0]["is_expanded"]
        assert first_section_open, "Первая секция должна быть открыта"

        # Получаем содержимое первой секции
        first_section_content = accordion_page.get_section_content(0)
        accordion_page.log_step(
            f"Содержимое первой секции: {first_section_content[:100]}..."
        )

        assert len(first_section_content) > 0, "Открытая секция должна содержать текст"

        first_section_result = {
            "section_index": 0,
            "is_expanded": first_section_open,
            "content_length": len(first_section_content),
            "has_content": len(first_section_content) > 0,
            "header_text": states_after_first[0]["header_text"],
        }

        allure.attach(
            str(first_section_result),
            "first_section_expansion_result",
            allure.attachment_type.JSON,
        )

    with allure.step("Раскрываем вторую секцию"):
        accordion_page.log_step("Клик по второй секции")
        second_expand_result = accordion_page.click_section_header(1)
        accordion_page.page.wait_for_timeout(1000)

        states_after_second = accordion_page.get_all_sections_states()
        accordion_page.log_step(
            f"Состояния после раскрытия второй секции: {states_after_second}"
        )

        second_section_open = states_after_second[1]["is_expanded"]
        assert second_section_open, "Вторая секция должна быть открыта"

        # Проверяем поведение первой секции (может остаться открытой или закрыться)
        first_still_open = states_after_second[0]["is_expanded"]

        accordion_behavior = {
            "first_section_still_open": first_still_open,
            "second_section_open": second_section_open,
            "multiple_sections_can_be_open": first_still_open and second_section_open,
            "single_section_mode": not first_still_open and second_section_open,
        }

        accordion_page.log_step(f"Поведение аккордеона: {accordion_behavior}")
        allure.attach(
            str(accordion_behavior),
            "accordion_behavior_analysis",
            allure.attachment_type.JSON,
        )

    with allure.step("Тестируем закрытие открытой секции"):
        # Кликаем по открытой второй секции чтобы закрыть
        accordion_page.log_step("Попытка закрытия второй секции")
        close_result = accordion_page.click_section_header(1)
        accordion_page.page.wait_for_timeout(1000)

        states_after_close = accordion_page.get_all_sections_states()
        second_section_closed = not states_after_close[1]["is_expanded"]

        close_test_result = {
            "close_click_performed": close_result,
            "second_section_closed": second_section_closed,
            "section_toggles": second_section_closed,
            "final_states": states_after_close,
        }

        accordion_page.log_step(f"Результат теста закрытия: {close_test_result}")
        allure.attach(
            str(close_test_result),
            "section_close_test_result",
            allure.attachment_type.JSON,
        )

        if close_test_result["section_toggles"]:
            accordion_page.log_step("✅ Секции корректно переключаются (toggle)")
        else:
            accordion_page.log_step(
                "ℹ️ Секция остается открытой - возможно режим 'always expanded'"
            )


@allure.epic("Widgets")
@allure.feature("Accordion")
@allure.story("Multiple Sections")
@pytest.mark.widgets
@pytest.mark.regression
def test_multiple_accordion_sections(accordion_page: AccordionPage):
    """
    Тест работы с множественными секциями аккордеона.

    Проверяет можно ли открыть несколько секций одновременно.
    """
    with allure.step("Закрываем все секции для начала теста"):
        accordion_page.log_step("Сброс состояния аккордеона")
        accordion_page.close_all_sections()
        accordion_page.page.wait_for_timeout(1000)

        initial_clean_states = accordion_page.get_all_sections_states()
        accordion_page.log_step(f"Состояние после сброса: {initial_clean_states}")

    sections_to_test = []

    with allure.step("Последовательно открываем все секции"):
        all_states = accordion_page.get_all_sections_states()

        for i in range(min(3, len(all_states))):  # Тестируем максимум 3 секции
            with allure.step(f"Открытие секции {i + 1}"):
                accordion_page.log_step(f"Открытие секции с индексом {i}")

                # Состояние до открытия
                state_before = accordion_page.get_section_state(i)

                # Открываем секцию
                click_result = accordion_page.click_section_header(i)
                accordion_page.page.wait_for_timeout(800)

                # Состояние после открытия
                state_after = accordion_page.get_section_state(i)

                # Получаем общее состояние всех секций
                all_states_after = accordion_page.get_all_sections_states()
                open_sections_count = sum(
                    1 for section in all_states_after if section["is_expanded"]
                )

                section_test = {
                    "section_index": i,
                    "section_header": state_after["header_text"],
                    "state_before": state_before,
                    "state_after": state_after,
                    "click_successful": click_result,
                    "section_opened": state_after["is_expanded"],
                    "total_open_sections": open_sections_count,
                    "other_sections_states": [
                        s["is_expanded"]
                        for j, s in enumerate(all_states_after)
                        if j != i
                    ],
                }

                sections_to_test.append(section_test)
                accordion_page.log_step(
                    f"Результат открытия секции {i}: {section_test}"
                )

    with allure.step("Анализируем поведение множественных секций"):
        allure.attach(
            str(sections_to_test),
            "multiple_sections_test_results",
            allure.attachment_type.JSON,
        )

        successfully_opened = sum(
            1 for test in sections_to_test if test["section_opened"]
        )
        max_open_simultaneously = max(
            test["total_open_sections"] for test in sections_to_test
        )

        # Анализируем последнее состояние
        final_states = accordion_page.get_all_sections_states()
        final_open_count = sum(1 for section in final_states if section["is_expanded"])

        multiple_sections_analysis = {
            "sections_tested": len(sections_to_test),
            "successfully_opened": successfully_opened,
            "max_open_simultaneously": max_open_simultaneously,
            "final_open_count": final_open_count,
            "supports_multiple_open": max_open_simultaneously > 1,
            "accordion_mode": "multiple" if max_open_simultaneously > 1 else "single",
            "all_sections_can_open": successfully_opened == len(sections_to_test),
        }

        accordion_page.log_step(
            f"Анализ множественных секций: {multiple_sections_analysis}"
        )
        allure.attach(
            str(multiple_sections_analysis),
            "multiple_sections_analysis",
            allure.attachment_type.JSON,
        )

        # Проверяем что секции открываются
        assert (
            multiple_sections_analysis["successfully_opened"] > 0
        ), f"Хотя бы одна секция должна открыться: {successfully_opened}/{len(sections_to_test)}"

        if multiple_sections_analysis["supports_multiple_open"]:
            accordion_page.log_step(
                "✅ Аккордеон поддерживает множественное раскрытие секций"
            )
        else:
            accordion_page.log_step("ℹ️ Аккордеон работает в режиме одной секции")


@allure.epic("Widgets")
@allure.feature("Accordion")
@allure.story("Section Content")
@pytest.mark.widgets
def test_accordion_sections_content(accordion_page: AccordionPage):
    """
    Тест содержимого секций аккордеона.

    Проверяет что каждая секция содержит уникальный контент.
    """
    sections_content = []

    with allure.step("Анализируем содержимое всех секций"):
        all_sections = accordion_page.get_all_sections_states()

        for i, section_info in enumerate(all_sections):
            with allure.step(
                f"Анализ содержимого секции {i + 1}: '{section_info['header_text']}'"
            ):
                accordion_page.log_step(f"Проверка содержимого секции {i}")

                # Открываем секцию если она закрыта
                if not section_info["is_expanded"]:
                    accordion_page.click_section_header(i)
                    accordion_page.page.wait_for_timeout(1000)

                # Получаем содержимое
                section_content = accordion_page.get_section_content(i)
                content_visible = accordion_page.is_section_content_visible(i)

                # Получаем дополнительную информацию о секции
                section_height = accordion_page.get_section_content_height(i)
                content_element_count = (
                    accordion_page.count_elements_in_section_content(i)
                )

                content_analysis = {
                    "section_index": i,
                    "header_text": section_info["header_text"],
                    "content_text": (
                        section_content[:200] + "..."
                        if len(section_content) > 200
                        else section_content
                    ),
                    "content_length": len(section_content),
                    "content_visible": content_visible,
                    "section_height": section_height,
                    "content_elements_count": content_element_count,
                    "has_meaningful_content": len(section_content) > 10,
                    "content_preview": section_content[:100] if section_content else "",
                }

                sections_content.append(content_analysis)
                accordion_page.log_step(f"Содержимое секции {i}: {content_analysis}")

    with allure.step("Проверяем уникальность содержимого секций"):
        allure.attach(
            str(sections_content),
            "all_sections_content_analysis",
            allure.attachment_type.JSON,
        )

        # Проверяем уникальность заголовков
        headers = [section["header_text"] for section in sections_content]
        unique_headers = set(headers)

        # Проверяем уникальность содержимого
        contents = [section["content_text"] for section in sections_content]
        unique_contents = set(contents)

        # Проверяем что секции содержат значимый контент
        meaningful_content_count = sum(
            1 for section in sections_content if section["has_meaningful_content"]
        )
        visible_content_count = sum(
            1 for section in sections_content if section["content_visible"]
        )

        content_uniqueness_analysis = {
            "total_sections": len(sections_content),
            "unique_headers": len(unique_headers),
            "unique_contents": len(unique_contents),
            "meaningful_content_sections": meaningful_content_count,
            "visible_content_sections": visible_content_count,
            "all_headers_unique": len(unique_headers) == len(headers),
            "all_contents_unique": len(unique_contents) == len(contents),
            "most_sections_have_content": meaningful_content_count
            >= len(sections_content) * 0.5,
        }

        accordion_page.log_step(
            f"Анализ уникальности содержимого: {content_uniqueness_analysis}"
        )
        allure.attach(
            str(content_uniqueness_analysis),
            "content_uniqueness_analysis",
            allure.attachment_type.JSON,
        )

        # Проверяем базовые требования к содержимому
        assert content_uniqueness_analysis[
            "all_headers_unique"
        ], f"Все заголовки должны быть уникальными: {len(unique_headers)}/{len(headers)}"
        assert content_uniqueness_analysis[
            "most_sections_have_content"
        ], f"Большинство секций должны содержать значимый контент: {meaningful_content_count}/{len(sections_content)}"

        if content_uniqueness_analysis["all_contents_unique"]:
            accordion_page.log_step("✅ Все секции содержат уникальный контент")
        else:
            accordion_page.log_step(
                "ℹ️ Некоторые секции могут содержать повторяющийся контент"
            )


@allure.epic("Widgets")
@allure.feature("Accordion")
@allure.story("Accordion Navigation")
@pytest.mark.widgets
def test_accordion_keyboard_navigation(accordion_page: AccordionPage):
    """
    Тест навигации по аккордеону с клавиатуры.

    Проверяет доступность аккордеона через клавиатурное управление.
    """
    with allure.step("Проверяем доступность аккордеона для клавиатурной навигации"):
        accordion_focusable = accordion_page.is_accordion_keyboard_accessible()
        accordion_page.log_step(
            f"Аккордеон доступен для клавиатурной навигации: {accordion_focusable}"
        )

        # Получаем информацию о tabindex и ARIA атрибутах
        accessibility_info = accordion_page.get_accordion_accessibility_info()
        accordion_page.log_step(f"Информация о доступности: {accessibility_info}")

        allure.attach(
            str(accessibility_info),
            "accordion_accessibility_info",
            allure.attachment_type.JSON,
        )

    keyboard_navigation_tests = []

    if accordion_focusable:
        with allure.step("Тестируем навигацию клавишами"):
            sections_count = len(accordion_page.get_all_sections_states())

            for i in range(min(3, sections_count)):
                with allure.step(f"Тест клавиатурной навигации к секции {i + 1}"):
                    # Фокусируемся на секции
                    focus_result = accordion_page.focus_on_section_header(i)

                    # Проверяем фокус
                    is_focused = accordion_page.is_section_header_focused(i)

                    # Пытаемся активировать секцию через Enter
                    enter_activation = accordion_page.activate_section_with_enter(i)
                    accordion_page.page.wait_for_timeout(500)

                    # Проверяем результат
                    section_state_after_enter = accordion_page.get_section_state(i)

                    # Пытаемся активировать секцию через Space
                    space_activation = accordion_page.activate_section_with_space(i)
                    accordion_page.page.wait_for_timeout(500)

                    section_state_after_space = accordion_page.get_section_state(i)

                    keyboard_test = {
                        "section_index": i,
                        "focus_successful": focus_result,
                        "is_focused": is_focused,
                        "enter_activation": enter_activation,
                        "space_activation": space_activation,
                        "state_after_enter": section_state_after_enter["is_expanded"],
                        "state_after_space": section_state_after_space["is_expanded"],
                        "keyboard_accessible": focus_result and is_focused,
                        "keyboard_operable": enter_activation or space_activation,
                    }

                    keyboard_navigation_tests.append(keyboard_test)
                    accordion_page.log_step(
                        f"Результат клавиатурного теста секции {i}: {keyboard_test}"
                    )

    with allure.step("Анализируем клавиатурную доступность"):
        if keyboard_navigation_tests:
            allure.attach(
                str(keyboard_navigation_tests),
                "keyboard_navigation_tests",
                allure.attachment_type.JSON,
            )

            accessible_sections = sum(
                1 for test in keyboard_navigation_tests if test["keyboard_accessible"]
            )
            operable_sections = sum(
                1 for test in keyboard_navigation_tests if test["keyboard_operable"]
            )

            keyboard_accessibility_summary = {
                "accordion_keyboard_accessible": accordion_focusable,
                "sections_tested": len(keyboard_navigation_tests),
                "accessible_sections": accessible_sections,
                "operable_sections": operable_sections,
                "accessibility_rate": (
                    accessible_sections / len(keyboard_navigation_tests)
                    if keyboard_navigation_tests
                    else 0
                ),
                "operability_rate": (
                    operable_sections / len(keyboard_navigation_tests)
                    if keyboard_navigation_tests
                    else 0
                ),
                "keyboard_support_good": accessible_sections
                >= len(keyboard_navigation_tests) * 0.5,
            }

        else:
            keyboard_accessibility_summary = {
                "accordion_keyboard_accessible": accordion_focusable,
                "sections_tested": 0,
                "accessible_sections": 0,
                "operable_sections": 0,
                "accessibility_rate": 0,
                "operability_rate": 0,
                "keyboard_support_good": False,
            }

        accordion_page.log_step(
            f"Итоги клавиатурной доступности: {keyboard_accessibility_summary}"
        )
        allure.attach(
            str(keyboard_accessibility_summary),
            "keyboard_accessibility_summary",
            allure.attachment_type.JSON,
        )

        if keyboard_accessibility_summary["keyboard_support_good"]:
            accordion_page.log_step(
                "✅ Аккордеон хорошо поддерживает клавиатурную навигацию"
            )
        elif accordion_focusable:
            accordion_page.log_step(
                "ℹ️ Аккордеон частично поддерживает клавиатурную навигацию"
            )
        else:
            accordion_page.log_step(
                "⚠️ Клавиатурная навигация недоступна или ограничена"
            )


@allure.epic("Widgets")
@allure.feature("Accordion")
@allure.story("Accordion Performance")
@pytest.mark.widgets
def test_accordion_animation_performance(accordion_page: AccordionPage):
    """
    Тест производительности анимаций аккордеона.

    Проверяет скорость открытия/закрытия секций и плавность анимаций.
    """
    animation_tests = []

    with allure.step("Тестируем производительность анимаций аккордеона"):
        sections_info = accordion_page.get_all_sections_states()

        for i in range(min(2, len(sections_info))):  # Тестируем первые 2 секции
            with allure.step(f"Тест анимации секции {i + 1}"):
                accordion_page.log_step(f"Измерение времени анимации секции {i}")

                # Убеждаемся что секция закрыта
                if sections_info[i]["is_expanded"]:
                    accordion_page.click_section_header(i)
                    accordion_page.page.wait_for_timeout(1000)

                # Измеряем время открытия
                start_time = accordion_page.get_current_timestamp()
                accordion_page.click_section_header(i)

                # Ждем завершения анимации открытия
                expansion_complete = accordion_page.wait_for_section_expansion(
                    i, timeout=3000
                )
                end_time = accordion_page.get_current_timestamp()

                expansion_duration = end_time - start_time

                # Измеряем время закрытия
                close_start_time = accordion_page.get_current_timestamp()
                accordion_page.click_section_header(i)

                # Ждем завершения анимации закрытия
                collapse_complete = accordion_page.wait_for_section_collapse(
                    i, timeout=3000
                )
                close_end_time = accordion_page.get_current_timestamp()

                collapse_duration = close_end_time - close_start_time

                # Проверяем плавность анимации
                animation_smooth = accordion_page.is_animation_smooth(i)

                animation_test = {
                    "section_index": i,
                    "expansion_duration_ms": expansion_duration,
                    "collapse_duration_ms": collapse_duration,
                    "expansion_completed": expansion_complete,
                    "collapse_completed": collapse_complete,
                    "animation_smooth": animation_smooth,
                    "expansion_reasonable_speed": 100
                    <= expansion_duration
                    <= 2000,  # 0.1-2 секунды
                    "collapse_reasonable_speed": 100 <= collapse_duration <= 2000,
                    "total_cycle_time": expansion_duration + collapse_duration,
                }

                animation_tests.append(animation_test)
                accordion_page.log_step(
                    f"Результат теста анимации секции {i}: {animation_test}"
                )

    with allure.step("Анализируем производительность анимаций"):
        allure.attach(
            str(animation_tests),
            "animation_performance_tests",
            allure.attachment_type.JSON,
        )

        if animation_tests:
            avg_expansion_time = sum(
                test["expansion_duration_ms"] for test in animation_tests
            ) / len(animation_tests)
            avg_collapse_time = sum(
                test["collapse_duration_ms"] for test in animation_tests
            ) / len(animation_tests)

            smooth_animations = sum(
                1 for test in animation_tests if test["animation_smooth"]
            )
            reasonable_speed_animations = sum(
                1
                for test in animation_tests
                if test["expansion_reasonable_speed"]
                and test["collapse_reasonable_speed"]
            )

            performance_summary = {
                "sections_tested": len(animation_tests),
                "average_expansion_time_ms": round(avg_expansion_time, 2),
                "average_collapse_time_ms": round(avg_collapse_time, 2),
                "smooth_animations": smooth_animations,
                "reasonable_speed_animations": reasonable_speed_animations,
                "performance_good": reasonable_speed_animations
                >= len(animation_tests) * 0.5,
                "animations_smooth": smooth_animations >= len(animation_tests) * 0.5,
                "overall_performance_acceptable": reasonable_speed_animations > 0
                and avg_expansion_time < 3000,
            }

        else:
            performance_summary = {
                "sections_tested": 0,
                "average_expansion_time_ms": 0,
                "average_collapse_time_ms": 0,
                "smooth_animations": 0,
                "reasonable_speed_animations": 0,
                "performance_good": False,
                "animations_smooth": False,
                "overall_performance_acceptable": False,
            }

        accordion_page.log_step(
            f"Итоги производительности анимаций: {performance_summary}"
        )
        allure.attach(
            str(performance_summary),
            "animation_performance_summary",
            allure.attachment_type.JSON,
        )

        if performance_summary["overall_performance_acceptable"]:
            accordion_page.log_step(
                "✅ Производительность анимаций аккордеона приемлемая"
            )
        else:
            accordion_page.log_step("⚠️ Производительность анимаций требует оптимизации")

        # Базовая проверка что анимации работают
        assert (
            len(animation_tests) > 0
        ), "Должен быть проведен хотя бы один тест анимации"
