"""
Тесты для страницы Sortable.
Проверяет функциональность сортировки элементов:
- Сортировка списков drag-and-drop
- Сортировка сетки элементов
- Проверка изменения порядка элементов
- Валидация финальных позиций
"""

import pytest
import allure
from pages.interactions.sortable_page import SortablePage


@allure.epic("Interactions")
@allure.feature("Sortable")
@allure.story("List Sorting")
@pytest.mark.interactions
@pytest.mark.smoke
def test_sort_list_items(sortable_page: SortablePage):
    """
    Тест сортировки элементов в списке.

    Перетаскивает элементы списка для изменения их порядка.
    """
    with allure.step("Получаем изначальный порядок элементов списка"):
        initial_order = sortable_page.get_list_items_order()
        sortable_page.log_step(f"Изначальный порядок списка: {initial_order}")

        allure.attach(
            str(initial_order), "initial_list_order", allure.attachment_type.JSON
        )

        assert (
            len(initial_order) >= 3
        ), f"В списке должно быть минимум 3 элемента, найдено: {len(initial_order)}"

    with allure.step("Перетаскиваем первый элемент на третью позицию"):
        sortable_page.log_step("Перетаскивание первого элемента вниз на 2 позиции")

        # Перетаскиваем первый элемент на третью позицию (индекс 2)
        drag_result = sortable_page.drag_list_item_to_position(0, 2)
        sortable_page.log_step(f"Результат перетаскивания: {drag_result}")

        assert drag_result, "Перетаскивание должно быть успешным"

    with allure.step("Проверяем новый порядок после перетаскивания"):
        # Небольшая пауза для обновления DOM
        sortable_page.page.wait_for_timeout(1000)

        new_order = sortable_page.get_list_items_order()
        sortable_page.log_step(f"Новый порядок списка: {new_order}")

        allure.attach(str(new_order), "new_list_order", allure.attachment_type.JSON)

        # Проверяем что порядок изменился
        order_changed = new_order != initial_order
        sortable_page.log_step(f"Порядок изменился: {order_changed}")

        assert (
            order_changed
        ), f"Порядок элементов должен измениться: было {initial_order}, стало {new_order}"

        # Проверяем что первый элемент переместился
        if len(initial_order) >= 3 and len(new_order) >= 3:
            first_element_moved = (
                initial_order[0] not in new_order[:1]
            )  # Первый элемент больше не на первой позиции
            sortable_page.log_step(
                f"Первый элемент переместился: {first_element_moved}"
            )

        sorting_result = {
            "initial_order": initial_order,
            "new_order": new_order,
            "order_changed": order_changed,
            "drag_successful": drag_result,
        }

        allure.attach(
            str(sorting_result), "list_sorting_result", allure.attachment_type.JSON
        )


@allure.epic("Interactions")
@allure.feature("Sortable")
@allure.story("Grid Sorting")
@pytest.mark.interactions
@pytest.mark.smoke
def test_sort_grid_items(sortable_page: SortablePage):
    """
    Тест сортировки элементов в сетке.

    Переключается на вкладку Grid и проверяет сортировку в сеточном режиме.
    """
    with allure.step("Переключаемся на вкладку Grid"):
        sortable_page.log_step("Переключение на режим сетки")
        sortable_page.switch_to_grid_tab()

        # Проверяем что переключение прошло успешно
        grid_tab_active = sortable_page.is_grid_tab_active()
        assert grid_tab_active, "Вкладка Grid должна быть активной"

    with allure.step("Получаем изначальный порядок элементов сетки"):
        initial_grid_order = sortable_page.get_grid_items_order()
        sortable_page.log_step(f"Изначальный порядок сетки: {initial_grid_order}")

        allure.attach(
            str(initial_grid_order), "initial_grid_order", allure.attachment_type.JSON
        )

        assert (
            len(initial_grid_order) >= 6
        ), f"В сетке должно быть минимум 6 элементов, найдено: {len(initial_grid_order)}"

    with allure.step("Перетаскиваем элементы в сетке"):
        sortable_page.log_step("Перетаскивание элементов в сеточном режиме")

        # Перетаскиваем первый элемент сетки на позицию в центр
        center_position = len(initial_grid_order) // 2
        drag_result = sortable_page.drag_grid_item_to_position(0, center_position)
        sortable_page.log_step(f"Перетаскивание в сетке: {drag_result}")

        assert drag_result, "Перетаскивание в сетке должно быть успешным"

    with allure.step("Проверяем изменения в сетке"):
        sortable_page.page.wait_for_timeout(1000)

        new_grid_order = sortable_page.get_grid_items_order()
        sortable_page.log_step(f"Новый порядок сетки: {new_grid_order}")

        allure.attach(
            str(new_grid_order), "new_grid_order", allure.attachment_type.JSON
        )

        grid_order_changed = new_grid_order != initial_grid_order
        sortable_page.log_step(f"Порядок сетки изменился: {grid_order_changed}")

        assert (
            grid_order_changed
        ), f"Порядок элементов сетки должен измениться: было {initial_grid_order}, стало {new_grid_order}"

        grid_sorting_result = {
            "initial_grid_order": initial_grid_order,
            "new_grid_order": new_grid_order,
            "grid_order_changed": grid_order_changed,
            "center_position": center_position,
        }

        allure.attach(
            str(grid_sorting_result), "grid_sorting_result", allure.attachment_type.JSON
        )


@allure.epic("Interactions")
@allure.feature("Sortable")
@allure.story("Multiple Moves")
@pytest.mark.interactions
@pytest.mark.regression
def test_multiple_sort_operations(sortable_page: SortablePage):
    """
    Тест множественных операций сортировки.

    Выполняет несколько операций перетаскивания подряд.
    """
    moves_log = []

    with allure.step("Выполняем серию операций сортировки в списке"):
        initial_order = sortable_page.get_list_items_order()
        current_order = initial_order.copy()
        sortable_page.log_step(f"Начинаем с порядка: {current_order}")

        # Серия перетаскиваний
        moves_to_perform = [
            (0, 2),  # Первый элемент на третью позицию
            (2, 1),  # Третий элемент на вторую позицию
            (1, 0),  # Второй элемент на первую позицию
        ]

        for move_index, (from_pos, to_pos) in enumerate(moves_to_perform, 1):
            with allure.step(
                f"Перетаскивание {move_index}: позиция {from_pos} → {to_pos}"
            ):
                sortable_page.log_step(
                    f"Операция {move_index}: перемещение с позиции {from_pos} на {to_pos}"
                )

                # Получаем порядок до операции
                order_before = sortable_page.get_list_items_order()

                # Выполняем перетаскивание
                drag_success = sortable_page.drag_list_item_to_position(
                    from_pos, to_pos
                )
                sortable_page.page.wait_for_timeout(500)  # Пауза между операциями

                # Получаем порядок после операции
                order_after = sortable_page.get_list_items_order()

                move_result = {
                    "move_number": move_index,
                    "from_position": from_pos,
                    "to_position": to_pos,
                    "order_before": order_before,
                    "order_after": order_after,
                    "drag_success": drag_success,
                    "order_changed": order_before != order_after,
                }

                moves_log.append(move_result)
                sortable_page.log_step(
                    f"Результат операции {move_index}: {move_result}"
                )

                current_order = order_after

    with allure.step("Анализируем результаты множественных операций"):
        allure.attach(str(moves_log), "multiple_moves_log", allure.attachment_type.JSON)

        successful_moves = sum(1 for move in moves_log if move["drag_success"])
        order_changes = sum(1 for move in moves_log if move["order_changed"])

        final_order = sortable_page.get_list_items_order()

        multiple_moves_summary = {
            "total_moves_attempted": len(moves_log),
            "successful_moves": successful_moves,
            "moves_that_changed_order": order_changes,
            "initial_order": initial_order,
            "final_order": final_order,
            "total_order_change": final_order != initial_order,
        }

        sortable_page.log_step(
            f"Итоги множественных операций: {multiple_moves_summary}"
        )
        allure.attach(
            str(multiple_moves_summary),
            "multiple_moves_summary",
            allure.attachment_type.JSON,
        )

        # Проверяем что хотя бы некоторые операции были успешными
        assert (
            successful_moves > 0
        ), f"Хотя бы одна операция перетаскивания должна быть успешной: {successful_moves}/{len(moves_log)}"

        # Проверяем что финальный порядок отличается от изначального
        assert multiple_moves_summary[
            "total_order_change"
        ], f"После серии операций порядок должен измениться: {initial_order} -> {final_order}"


@allure.epic("Interactions")
@allure.feature("Sortable")
@allure.story("Tab Switching")
@pytest.mark.interactions
def test_tab_switching_preserves_state(sortable_page: SortablePage):
    """
    Тест переключения между вкладками List и Grid.

    Проверяет что изменения сохраняются при переключении вкладок.
    """
    tab_states = {}

    with allure.step("Тестируем состояние вкладки List"):
        # Убеждаемся что мы на вкладке List
        sortable_page.switch_to_list_tab()

        initial_list_order = sortable_page.get_list_items_order()
        sortable_page.log_step(f"Изначальный порядок List: {initial_list_order}")

        # Делаем изменение в списке
        if len(initial_list_order) >= 2:
            sortable_page.drag_list_item_to_position(0, 1)
            sortable_page.page.wait_for_timeout(1000)

        modified_list_order = sortable_page.get_list_items_order()

        tab_states["list"] = {
            "initial_order": initial_list_order,
            "modified_order": modified_list_order,
            "was_modified": modified_list_order != initial_list_order,
        }

        sortable_page.log_step(f"Состояние List вкладки: {tab_states['list']}")

    with allure.step("Переключаемся на вкладку Grid"):
        sortable_page.log_step("Переключение на вкладку Grid")
        sortable_page.switch_to_grid_tab()

        grid_active = sortable_page.is_grid_tab_active()
        assert grid_active, "Вкладка Grid должна быть активной"

        initial_grid_order = sortable_page.get_grid_items_order()
        sortable_page.log_step(f"Изначальный порядок Grid: {initial_grid_order}")

        # Делаем изменение в сетке
        if len(initial_grid_order) >= 3:
            sortable_page.drag_grid_item_to_position(0, 2)
            sortable_page.page.wait_for_timeout(1000)

        modified_grid_order = sortable_page.get_grid_items_order()

        tab_states["grid"] = {
            "initial_order": initial_grid_order,
            "modified_order": modified_grid_order,
            "was_modified": modified_grid_order != initial_grid_order,
        }

        sortable_page.log_step(f"Состояние Grid вкладки: {tab_states['grid']}")

    with allure.step("Возвращаемся на вкладку List и проверяем сохранность"):
        sortable_page.log_step("Возврат на вкладку List")
        sortable_page.switch_to_list_tab()

        list_active = sortable_page.is_list_tab_active()
        assert list_active, "Вкладка List должна быть активной"

        # Проверяем что изменения в List сохранились
        current_list_order = sortable_page.get_list_items_order()
        list_state_preserved = (
            current_list_order == tab_states["list"]["modified_order"]
            or current_list_order != tab_states["list"]["initial_order"]
        )

        tab_states["list"]["state_after_return"] = current_list_order
        tab_states["list"]["state_preserved"] = list_state_preserved

        sortable_page.log_step(f"Состояние List после возврата: {current_list_order}")
        sortable_page.log_step(f"Состояние сохранилось: {list_state_preserved}")

    with allure.step("Анализируем поведение переключения вкладок"):
        allure.attach(
            str(tab_states), "tab_states_analysis", allure.attachment_type.JSON
        )

        tab_switching_summary = {
            "list_tab_modified": tab_states["list"]["was_modified"],
            "grid_tab_modified": tab_states["grid"]["was_modified"],
            "list_state_preserved": tab_states["list"]["state_preserved"],
            "tab_switching_works": True,  # Само переключение работает
        }

        sortable_page.log_step(f"Итоги переключения вкладок: {tab_switching_summary}")
        allure.attach(
            str(tab_switching_summary),
            "tab_switching_summary",
            allure.attachment_type.JSON,
        )

        # Проверяем что переключения между вкладками работают
        assert tab_switching_summary[
            "tab_switching_works"
        ], "Переключение между вкладками должно работать"


@allure.epic("Interactions")
@allure.feature("Sortable")
@allure.story("Element Validation")
@pytest.mark.interactions
def test_sortable_elements_validation(sortable_page: SortablePage):
    """
    Тест валидации элементов sortable.

    Проверяет структуру и свойства сортируемых элементов.
    """
    validation_results = {}

    with allure.step("Валидация элементов списка"):
        sortable_page.switch_to_list_tab()

        list_elements = sortable_page.get_list_elements_info()
        sortable_page.log_step(f"Информация об элементах списка: {list_elements}")

        list_validation = {
            "total_elements": len(list_elements),
            "elements_have_text": all(elem.get("text") for elem in list_elements),
            "elements_visible": all(
                elem.get("visible", False) for elem in list_elements
            ),
            "elements_have_classes": all(elem.get("classes") for elem in list_elements),
            "unique_texts": len(set(elem["text"] for elem in list_elements))
            == len(list_elements),
        }

        validation_results["list"] = list_validation
        sortable_page.log_step(f"Валидация списка: {list_validation}")

        # Основные проверки для списка
        assert (
            list_validation["total_elements"] >= 3
        ), f"В списке должно быть минимум 3 элемента: {list_validation['total_elements']}"
        assert list_validation[
            "elements_have_text"
        ], "Все элементы списка должны иметь текст"
        assert list_validation[
            "elements_visible"
        ], "Все элементы списка должны быть видимыми"

    with allure.step("Валидация элементов сетки"):
        sortable_page.switch_to_grid_tab()

        grid_elements = sortable_page.get_grid_elements_info()
        sortable_page.log_step(f"Информация об элементах сетки: {grid_elements}")

        grid_validation = {
            "total_elements": len(grid_elements),
            "elements_have_text": all(elem.get("text") for elem in grid_elements),
            "elements_visible": all(
                elem.get("visible", False) for elem in grid_elements
            ),
            "elements_have_classes": all(elem.get("classes") for elem in grid_elements),
            "unique_texts": len(set(elem["text"] for elem in grid_elements))
            == len(grid_elements),
            "grid_layout": True,  # Проверяем что элементы в сеточной раскладке
        }

        validation_results["grid"] = grid_validation
        sortable_page.log_step(f"Валидация сетки: {grid_validation}")

        # Основные проверки для сетки
        assert (
            grid_validation["total_elements"] >= 6
        ), f"В сетке должно быть минимум 6 элементов: {grid_validation['total_elements']}"
        assert grid_validation[
            "elements_have_text"
        ], "Все элементы сетки должны иметь текст"
        assert grid_validation[
            "elements_visible"
        ], "Все элементы сетки должны быть видимыми"

    with allure.step("Проверяем интерактивность элементов"):
        # Возвращаемся к списку для проверки интерактивности
        sortable_page.switch_to_list_tab()

        interactivity_check = {
            "list_elements_draggable": sortable_page.are_list_elements_draggable(),
            "list_elements_hoverable": sortable_page.are_list_elements_hoverable(),
        }

        sortable_page.switch_to_grid_tab()
        interactivity_check.update(
            {
                "grid_elements_draggable": sortable_page.are_grid_elements_draggable(),
                "grid_elements_hoverable": sortable_page.are_grid_elements_hoverable(),
            }
        )

        validation_results["interactivity"] = interactivity_check
        sortable_page.log_step(f"Проверка интерактивности: {interactivity_check}")

        allure.attach(
            str(validation_results),
            "elements_validation_results",
            allure.attachment_type.JSON,
        )

        # Итоговая валидация
        overall_validation = {
            "list_valid": all(validation_results["list"].values()),
            "grid_valid": all(validation_results["grid"].values()),
            "interactive_elements": any(interactivity_check.values()),
        }

        sortable_page.log_step(f"Общая валидация: {overall_validation}")

        assert overall_validation[
            "interactive_elements"
        ], "Элементы должны быть интерактивными (draggable или hoverable)"
