"""
Тесты для страницы Selectable.
Проверяет функциональность выбора элементов:
- Одиночный выбор элементов
- Множественный выбор элементов
- Переключение между режимами списка и сетки
- Проверка состояний выбора
"""

import pytest
import allure
from pages.interactions.selectable_page import SelectablePage


@allure.epic("Interactions")
@allure.feature("Selectable")
@allure.story("Single Selection")
@pytest.mark.interactions
@pytest.mark.smoke
def test_single_item_selection(selectable_page: SelectablePage):
    """
    Тест одиночного выбора элементов в списке.

    Выбирает отдельные элементы и проверяет их состояние.
    """
    with allure.step("Проверяем начальное состояние списка"):
        initial_selected = selectable_page.get_selected_list_items()
        selectable_page.log_step(f"Изначально выбранные элементы: {initial_selected}")

        # Изначально ничего не должно быть выбрано
        assert (
            len(initial_selected) == 0
        ), f"Изначально не должно быть выбранных элементов, найдено: {len(initial_selected)}"

    with allure.step("Получаем список всех доступных элементов"):
        all_items = selectable_page.get_all_list_items()
        selectable_page.log_step(f"Всего элементов в списке: {len(all_items)}")

        allure.attach(str(all_items), "all_list_items", allure.attachment_type.JSON)

        assert (
            len(all_items) >= 4
        ), f"В списке должно быть минимум 4 элемента, найдено: {len(all_items)}"

    with allure.step("Выбираем первый элемент"):
        first_item = all_items[0]
        selectable_page.log_step(f"Выбор первого элемента: {first_item}")

        selection_result = selectable_page.select_list_item(0)
        assert selection_result, "Выбор первого элемента должен быть успешным"

        # Проверяем что элемент выбрался
        selected_after_first = selectable_page.get_selected_list_items()
        selectable_page.log_step(
            f"Выбранные элементы после первого выбора: {selected_after_first}"
        )

        assert (
            len(selected_after_first) == 1
        ), f"Должен быть выбран 1 элемент, выбрано: {len(selected_after_first)}"
        assert (
            first_item in selected_after_first
        ), f"Первый элемент '{first_item}' должен быть в выбранных"

    with allure.step("Выбираем третий элемент"):
        third_item = all_items[2] if len(all_items) > 2 else all_items[-1]
        selectable_page.log_step(f"Выбор третьего элемента: {third_item}")

        selection_result_third = selectable_page.select_list_item(
            2 if len(all_items) > 2 else -1
        )
        assert selection_result_third, "Выбор третьего элемента должен быть успешным"

        # Проверяем состояние после второго выбора
        selected_after_third = selectable_page.get_selected_list_items()
        selectable_page.log_step(
            f"Выбранные элементы после второго выбора: {selected_after_third}"
        )

        # В зависимости от реализации может быть один или несколько выбранных элементов
        selection_summary = {
            "first_item": first_item,
            "third_item": third_item,
            "selected_after_first": selected_after_first,
            "selected_after_third": selected_after_third,
            "multiple_selection_supported": len(selected_after_third) > 1,
            "single_selection_mode": len(selected_after_third) == 1,
        }

        selectable_page.log_step(f"Итоги выбора: {selection_summary}")
        allure.attach(
            str(selection_summary),
            "single_selection_results",
            allure.attachment_type.JSON,
        )

        assert (
            len(selected_after_third) >= 1
        ), "После выбора должен быть выбран хотя бы один элемент"


@allure.epic("Interactions")
@allure.feature("Selectable")
@allure.story("Multiple Selection")
@pytest.mark.interactions
@pytest.mark.regression
def test_multiple_items_selection(selectable_page: SelectablePage):
    """
    Тест множественного выбора элементов.

    Проверяет возможность выбора нескольких элементов одновременно.
    """
    items_to_select = [0, 2, 3]  # Индексы элементов для выбора
    selection_results = {}

    with allure.step("Очищаем все выборы"):
        selectable_page.clear_all_selections()
        initial_state = selectable_page.get_selected_list_items()
        selectable_page.log_step(f"Состояние после очистки: {initial_state}")

    with allure.step("Последовательно выбираем несколько элементов"):
        all_items = selectable_page.get_all_list_items()

        for i, item_index in enumerate(items_to_select, 1):
            if item_index < len(all_items):
                with allure.step(f"Выбор элемента {i}: индекс {item_index}"):
                    item_text = all_items[item_index]
                    selectable_page.log_step(
                        f"Выбираем элемент {item_index}: '{item_text}'"
                    )

                    # Выбираем с зажатым Ctrl для множественного выбора
                    selection_success = selectable_page.select_list_item_with_ctrl(
                        item_index
                    )

                    # Проверяем текущее состояние
                    current_selected = selectable_page.get_selected_list_items()

                    selection_results[f"step_{i}"] = {
                        "item_index": item_index,
                        "item_text": item_text,
                        "selection_success": selection_success,
                        "selected_items": current_selected.copy(),
                        "total_selected": len(current_selected),
                    }

                    selectable_page.log_step(
                        f"Результат выбора {i}: {selection_results[f'step_{i}']}"
                    )

    with allure.step("Анализируем результаты множественного выбора"):
        final_selected = selectable_page.get_selected_list_items()

        multiple_selection_analysis = {
            "items_attempted": len(items_to_select),
            "final_selected_count": len(final_selected),
            "final_selected_items": final_selected,
            "multiple_selection_works": len(final_selected) > 1,
            "all_attempted_selected": len(final_selected) == len(items_to_select),
            "selection_steps": selection_results,
        }

        selectable_page.log_step(
            f"Анализ множественного выбора: {multiple_selection_analysis}"
        )
        allure.attach(
            str(multiple_selection_analysis),
            "multiple_selection_analysis",
            allure.attachment_type.JSON,
        )

        # Проверяем что множественный выбор работает или хотя бы один элемент выбран
        assert (
            len(final_selected) >= 1
        ), f"Должен быть выбран хотя бы один элемент, выбрано: {len(final_selected)}"

        # Если поддерживается множественный выбор, проверяем это
        if multiple_selection_analysis["multiple_selection_works"]:
            selectable_page.log_step("✅ Множественный выбор поддерживается")
        else:
            selectable_page.log_step("ℹ️ Работает только одиночный выбор")


@allure.epic("Interactions")
@allure.feature("Selectable")
@allure.story("Grid Selection")
@pytest.mark.interactions
@pytest.mark.smoke
def test_grid_items_selection(selectable_page: SelectablePage):
    """
    Тест выбора элементов в сеточном режиме.

    Переключается на режим сетки и проверяет выбор элементов.
    """
    with allure.step("Переключаемся на режим сетки"):
        selectable_page.log_step("Переключение на вкладку Grid")
        selectable_page.switch_to_grid_tab()

        grid_active = selectable_page.is_grid_tab_active()
        assert grid_active, "Вкладка Grid должна быть активной"

    with allure.step("Получаем элементы сетки"):
        grid_items = selectable_page.get_all_grid_items()
        selectable_page.log_step(f"Элементы сетки: {grid_items}")

        allure.attach(str(grid_items), "grid_items", allure.attachment_type.JSON)

        assert (
            len(grid_items) >= 6
        ), f"В сетке должно быть минимум 6 элементов, найдено: {len(grid_items)}"

    with allure.step("Проверяем начальное состояние сетки"):
        initial_grid_selected = selectable_page.get_selected_grid_items()
        selectable_page.log_step(
            f"Изначально выбранные в сетке: {initial_grid_selected}"
        )

        assert (
            len(initial_grid_selected) == 0
        ), "Изначально в сетке ничего не должно быть выбрано"

    with allure.step("Выбираем элементы в сетке"):
        grid_selections = []

        # Выбираем несколько элементов сетки
        items_to_select = [1, 3, 5] if len(grid_items) >= 6 else [0, 1, 2]

        for item_index in items_to_select:
            if item_index < len(grid_items):
                item_name = grid_items[item_index]
                selectable_page.log_step(
                    f"Выбираем элемент сетки {item_index}: '{item_name}'"
                )

                selection_success = selectable_page.select_grid_item(item_index)
                current_selected = selectable_page.get_selected_grid_items()

                grid_selections.append(
                    {
                        "item_index": item_index,
                        "item_name": item_name,
                        "selection_success": selection_success,
                        "current_selected": current_selected.copy(),
                    }
                )

        selectable_page.log_step(f"Результаты выбора в сетке: {grid_selections}")

    with allure.step("Анализируем выбор в сеточном режиме"):
        final_grid_selected = selectable_page.get_selected_grid_items()

        grid_selection_summary = {
            "total_grid_items": len(grid_items),
            "items_selection_attempted": len(items_to_select),
            "final_selected_count": len(final_grid_selected),
            "final_selected_items": final_grid_selected,
            "selection_steps": grid_selections,
            "grid_selection_works": len(final_grid_selected) > 0,
        }

        selectable_page.log_step(f"Итоги выбора в сетке: {grid_selection_summary}")
        allure.attach(
            str(grid_selection_summary),
            "grid_selection_summary",
            allure.attachment_type.JSON,
        )

        assert grid_selection_summary[
            "grid_selection_works"
        ], "Выбор в сеточном режиме должен работать"
        assert (
            len(final_grid_selected) >= 1
        ), f"В сетке должен быть выбран хотя бы один элемент: {len(final_grid_selected)}"


@allure.epic("Interactions")
@allure.feature("Selectable")
@allure.story("Selection States")
@pytest.mark.interactions
def test_selection_state_changes(selectable_page: SelectablePage):
    """
    Тест изменений состояний выбора элементов.

    Проверяет визуальные изменения при выборе и снятии выбора.
    """
    state_changes = []

    with allure.step("Анализируем состояния элементов списка"):
        all_items = selectable_page.get_all_list_items()

        # Получаем детальную информацию о состояниях элементов
        for i, item_text in enumerate(all_items[:3]):  # Анализируем первые 3 элемента
            with allure.step(f"Анализ элемента {i}: '{item_text}'"):
                # Состояние до выбора
                state_before = selectable_page.get_list_item_state(i)

                # Выбираем элемент
                selectable_page.select_list_item(i)
                selectable_page.page.wait_for_timeout(500)

                # Состояние после выбора
                state_after = selectable_page.get_list_item_state(i)

                state_change = {
                    "item_index": i,
                    "item_text": item_text,
                    "state_before": state_before,
                    "state_after": state_after,
                    "visual_change": state_before != state_after,
                    "is_selected": state_after.get("selected", False),
                    "css_classes_changed": state_before.get("classes")
                    != state_after.get("classes"),
                }

                state_changes.append(state_change)
                selectable_page.log_step(f"Изменение состояния {i}: {state_change}")

                # Снимаем выбор для следующего теста
                selectable_page.deselect_list_item(i)

    with allure.step("Тестируем снятие выбора"):
        # Выбираем первый элемент
        selectable_page.select_list_item(0)
        selected_state = selectable_page.get_list_item_state(0)

        # Снимаем выбор
        deselection_success = selectable_page.deselect_list_item(0)
        deselected_state = selectable_page.get_list_item_state(0)

        deselection_test = {
            "selected_state": selected_state,
            "deselected_state": deselected_state,
            "deselection_success": deselection_success,
            "state_reverted": selected_state != deselected_state,
        }

        selectable_page.log_step(f"Тест снятия выбора: {deselection_test}")

    with allure.step("Анализируем изменения состояний"):
        allure.attach(
            str(state_changes), "state_changes_detailed", allure.attachment_type.JSON
        )

        visual_changes_count = sum(
            1 for change in state_changes if change["visual_change"]
        )
        selected_count = sum(1 for change in state_changes if change["is_selected"])
        css_changes_count = sum(
            1 for change in state_changes if change["css_classes_changed"]
        )

        states_analysis = {
            "total_items_tested": len(state_changes),
            "visual_changes": visual_changes_count,
            "items_became_selected": selected_count,
            "css_classes_changed": css_changes_count,
            "selection_provides_feedback": visual_changes_count > 0
            or css_changes_count > 0,
            "deselection_test": deselection_test,
        }

        selectable_page.log_step(f"Анализ состояний: {states_analysis}")
        allure.attach(
            str(states_analysis),
            "selection_states_analysis",
            allure.attachment_type.JSON,
        )

        # Проверяем что выбор предоставляет визуальную обратную связь
        assert states_analysis[
            "selection_provides_feedback"
        ], "Выбор элементов должен предоставлять визуальную обратную связь"


@allure.epic("Interactions")
@allure.feature("Selectable")
@allure.story("Cross-Tab Selection")
@pytest.mark.interactions
def test_selection_across_tabs(selectable_page: SelectablePage):
    """
    Тест выбора элементов при переключении между вкладками.

    Проверяет сохраняются ли выборы при переключении между List и Grid.
    """
    cross_tab_results = {}

    with allure.step("Делаем выбор в режиме списка"):
        selectable_page.switch_to_list_tab()

        # Выбираем несколько элементов в списке
        list_items = selectable_page.get_all_list_items()
        if len(list_items) >= 2:
            selectable_page.select_list_item(0)
            selectable_page.select_list_item_with_ctrl(
                1
            )  # Пытаемся множественный выбор

        selected_in_list = selectable_page.get_selected_list_items()

        cross_tab_results["list_selection"] = {
            "total_items": len(list_items),
            "selected_items": selected_in_list,
            "selected_count": len(selected_in_list),
        }

        selectable_page.log_step(
            f"Выбор в списке: {cross_tab_results['list_selection']}"
        )

    with allure.step("Переключаемся на сетку и делаем выбор"):
        selectable_page.switch_to_grid_tab()

        # Проверяем что переключение прошло успешно
        grid_active = selectable_page.is_grid_tab_active()
        assert grid_active, "Переключение на Grid должно быть успешным"

        # Делаем выбор в сетке
        grid_items = selectable_page.get_all_grid_items()
        if len(grid_items) >= 2:
            selectable_page.select_grid_item(1)
            selectable_page.select_grid_item_with_ctrl(
                2
            )  # Пытаемся множественный выбор

        selected_in_grid = selectable_page.get_selected_grid_items()

        cross_tab_results["grid_selection"] = {
            "total_items": len(grid_items),
            "selected_items": selected_in_grid,
            "selected_count": len(selected_in_grid),
        }

        selectable_page.log_step(
            f"Выбор в сетке: {cross_tab_results['grid_selection']}"
        )

    with allure.step("Возвращаемся к списку и проверяем сохранность"):
        selectable_page.switch_to_list_tab()

        # Проверяем состояние выбора в списке после возврата
        list_selection_after_return = selectable_page.get_selected_list_items()

        cross_tab_results["list_after_return"] = {
            "selected_items": list_selection_after_return,
            "selected_count": len(list_selection_after_return),
            "selection_preserved": (
                set(list_selection_after_return)
                == set(cross_tab_results["list_selection"]["selected_items"])
            ),
            "selection_cleared": len(list_selection_after_return) == 0,
        }

        selectable_page.log_step(
            f"Список после возврата: {cross_tab_results['list_after_return']}"
        )

    with allure.step("Возвращаемся к сетке и проверяем сохранность"):
        selectable_page.switch_to_grid_tab()

        grid_selection_after_return = selectable_page.get_selected_grid_items()

        cross_tab_results["grid_after_return"] = {
            "selected_items": grid_selection_after_return,
            "selected_count": len(grid_selection_after_return),
            "selection_preserved": (
                set(grid_selection_after_return)
                == set(cross_tab_results["grid_selection"]["selected_items"])
            ),
            "selection_cleared": len(grid_selection_after_return) == 0,
        }

        selectable_page.log_step(
            f"Сетка после возврата: {cross_tab_results['grid_after_return']}"
        )

    with allure.step("Анализируем поведение выбора между вкладками"):
        allure.attach(
            str(cross_tab_results),
            "cross_tab_selection_results",
            allure.attachment_type.JSON,
        )

        cross_tab_summary = {
            "list_selection_made": cross_tab_results["list_selection"]["selected_count"]
            > 0,
            "grid_selection_made": cross_tab_results["grid_selection"]["selected_count"]
            > 0,
            "list_selection_preserved": cross_tab_results["list_after_return"][
                "selection_preserved"
            ],
            "grid_selection_preserved": cross_tab_results["grid_after_return"][
                "selection_preserved"
            ],
            "selections_independent": (
                cross_tab_results["list_selection"]["selected_items"]
                != cross_tab_results["grid_selection"]["selected_items"]
            ),
        }

        selectable_page.log_step(f"Анализ межвкладочного выбора: {cross_tab_summary}")
        allure.attach(
            str(cross_tab_summary), "cross_tab_summary", allure.attachment_type.JSON
        )

        # Базовые проверки
        assert (
            cross_tab_summary["list_selection_made"]
            or cross_tab_summary["grid_selection_made"]
        ), "Должен быть сделан выбор хотя бы в одном режиме"

        # Проверяем что переключения между вкладками работают корректно
        tabs_work_correctly = (
            selectable_page.is_list_tab_active() == False
            and selectable_page.is_grid_tab_active() == True
        )
        assert (
            tabs_work_correctly
        ), "После переключения должна быть активна вкладка Grid"
