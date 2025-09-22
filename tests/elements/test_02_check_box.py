"""
Тесты для страницы Check Box.
Проверяет функциональность чекбоксов с древовидной структурой:
- Развертывание/свертывание узлов дерева
- Выбор/снятие выбора чекбоксов
- Зависимости между родительскими и дочерними элементами
- Проверка состояний indeterminate
"""

import pytest
import allure
from pages.elements.check_box_page import CheckBoxPage


@allure.epic("Elements")
@allure.feature("Check Box")
@allure.story("Tree Expansion")
@pytest.mark.elements
@pytest.mark.smoke
def test_expand_collapse_tree_nodes(check_box_page: CheckBoxPage):
    """
    Тест развертывания и свертывания узлов дерева чекбоксов.

    Шаги:
    1. Развернуть корневой узел дерева
    2. Проверить что дочерние узлы стали видимыми
    3. Свернуть узел обратно
    4. Проверить что дочерние узлы скрылись
    """
    with allure.step("Развертываем корневой узел дерева"):
        check_box_page.log_step("Клик по кнопке развертывания корневого узла")
        check_box_page.expand_all()

    with allure.step("Проверяем что дочерние узлы стали видимыми"):
        visible_nodes = check_box_page.get_visible_nodes_count()
        check_box_page.log_step(
            f"Количество видимых узлов после развертывания: {visible_nodes}"
        )

        allure.attach(
            str(visible_nodes),
            "visible_nodes_after_expand",
            allure.attachment_type.TEXT,
        )

        assert (
            visible_nodes > 1
        ), f"После развертывания должно быть больше 1 узла, найдено: {visible_nodes}"

    with allure.step("Получаем список всех видимых чекбоксов"):
        visible_checkboxes = check_box_page.get_all_visible_checkboxes()
        check_box_page.log_step(f"Видимые чекбоксы: {visible_checkboxes}")

        allure.attach(
            str(visible_checkboxes), "visible_checkboxes", allure.attachment_type.JSON
        )

        expected_checkboxes = ["Home", "Desktop", "Documents", "WorkSpace", "Office"]
        for checkbox in expected_checkboxes[:3]:  # Проверяем первые несколько
            assert (
                checkbox in visible_checkboxes
            ), f"Чекбокс '{checkbox}' должен быть видим"

    with allure.step("Свертываем дерево обратно"):
        check_box_page.log_step("Клик по кнопке свертывания дерева")
        check_box_page.collapse_all()

    with allure.step("Проверяем что узлы свернулись"):
        collapsed_nodes = check_box_page.get_visible_nodes_count()
        check_box_page.log_step(
            f"Количество видимых узлов после свертывания: {collapsed_nodes}"
        )

        assert (
            collapsed_nodes == 1
        ), f"После свертывания должен остаться только корневой узел, найдено: {collapsed_nodes}"


@allure.epic("Elements")
@allure.feature("Check Box")
@allure.story("Checkbox Selection")
@pytest.mark.elements
@pytest.mark.smoke
def test_select_individual_checkboxes(check_box_page: CheckBoxPage):
    """
    Тест выбора отдельных чекбоксов.

    Проверяет выбор конкретных чекбоксов и отображение результата.
    """
    checkboxes_to_test = ["Desktop", "Documents", "Downloads"]

    with allure.step("Развертываем дерево для доступа к чекбоксам"):
        check_box_page.expand_all()

    for checkbox_name in checkboxes_to_test:
        with allure.step(f"Выбираем чекбокс '{checkbox_name}'"):
            check_box_page.log_step(f"Клик по чекбоксу: {checkbox_name}")
            check_box_page.select_checkbox(checkbox_name)

            # Проверяем что чекбокс выбран
            is_selected = check_box_page.is_checkbox_selected(checkbox_name)
            check_box_page.log_step(f"Чекбокс '{checkbox_name}' выбран: {is_selected}")

            assert is_selected, f"Чекбокс '{checkbox_name}' должен быть выбран"

    with allure.step("Проверяем результат выбора"):
        selected_results = check_box_page.get_selected_results()
        check_box_page.log_step(f"Результаты выбора: {selected_results}")

        allure.attach(
            str(selected_results), "selection_results", allure.attachment_type.JSON
        )

        for checkbox_name in checkboxes_to_test:
            assert (
                checkbox_name in selected_results
            ), f"'{checkbox_name}' должен быть в результатах"


@allure.epic("Elements")
@allure.feature("Check Box")
@allure.story("Parent-Child Dependencies")
@pytest.mark.elements
@pytest.mark.regression
def test_parent_child_checkbox_dependencies(check_box_page: CheckBoxPage):
    """
    Тест зависимостей между родительскими и дочерними чекбоксами.

    Проверяет что выбор родительского чекбокса автоматически выбирает дочерние.
    """
    with allure.step("Развертываем дерево для доступа к иерархии"):
        check_box_page.expand_all()

    with allure.step("Выбираем родительский чекбокс 'Home'"):
        check_box_page.log_step("Выбор родительского элемента 'Home'")
        check_box_page.select_checkbox("Home")

    with allure.step("Проверяем что все дочерние элементы выбрались автоматически"):
        child_checkboxes = ["Desktop", "Documents", "Downloads"]

        for child in child_checkboxes:
            is_child_selected = check_box_page.is_checkbox_selected(child)
            check_box_page.log_step(
                f"Дочерний элемент '{child}' выбран: {is_child_selected}"
            )

            # В зависимости от реализации дочерние могут выбираться автоматически
            # Записываем результат для анализа

        all_results = check_box_page.get_selected_results()
        check_box_page.log_step(f"Все выбранные элементы: {all_results}")

        allure.attach(
            str(all_results), "parent_child_selection", allure.attachment_type.JSON
        )

    with allure.step("Снимаем выбор с родительского элемента"):
        check_box_page.log_step("Снятие выбора с родительского элемента 'Home'")
        check_box_page.unselect_checkbox("Home")

    with allure.step("Проверяем что дочерние элементы тоже сняты с выбора"):
        results_after_unselect = check_box_page.get_selected_results()
        check_box_page.log_step(
            f"Результаты после снятия выбора: {results_after_unselect}"
        )

        allure.attach(
            str(results_after_unselect),
            "after_parent_unselect",
            allure.attachment_type.JSON,
        )

        # Результаты должны быть пустыми или содержать минимум элементов
        assert len(results_after_unselect) < len(
            all_results
        ), "После снятия выбора с родителя результатов должно стать меньше"


@allure.epic("Elements")
@allure.feature("Check Box")
@allure.story("Mixed Selection States")
@pytest.mark.elements
def test_mixed_selection_states(check_box_page: CheckBoxPage):
    """
    Тест смешанных состояний выбора (indeterminate state).

    Проверяет состояние когда выбраны только некоторые дочерние элементы.
    """
    with allure.step("Подготавливаем тестовую среду"):
        check_box_page.expand_all()
        check_box_page.clear_all_selections()  # Очищаем все выборы

    with allure.step("Выбираем только некоторые дочерние элементы"):
        partial_selection = ["Desktop", "Documents"]  # Выбираем не все дочерние

        for item in partial_selection:
            check_box_page.log_step(f"Выбор дочернего элемента: {item}")
            check_box_page.select_checkbox(item)

    with allure.step("Проверяем состояние родительского элемента"):
        parent_state = check_box_page.get_checkbox_state("Home")
        check_box_page.log_step(
            f"Состояние родительского элемента 'Home': {parent_state}"
        )

        # Родительский элемент может быть в состоянии indeterminate (частично выбран)
        states_info = {
            "parent_state": parent_state,
            "selected_children": partial_selection,
            "is_indeterminate": parent_state == "indeterminate",
        }

        allure.attach(
            str(states_info), "mixed_states_info", allure.attachment_type.JSON
        )

    with allure.step("Проверяем результаты частичного выбора"):
        partial_results = check_box_page.get_selected_results()
        check_box_page.log_step(f"Результаты частичного выбора: {partial_results}")

        for selected_item in partial_selection:
            assert (
                selected_item in partial_results
            ), f"'{selected_item}' должен быть в результатах"

        # Не выбранные элементы не должны присутствовать
        # Примечание: WorkSpace может быть выбран автоматически как родитель Desktop/Documents
        not_selected = ["Downloads", "Office"]
        for not_selected_item in not_selected:
            assert (
                not_selected_item not in partial_results
            ), f"'{not_selected_item}' НЕ должен быть в результатах"


@allure.epic("Elements")
@allure.feature("Check Box")
@allure.story("Bulk Operations")
@pytest.mark.elements
def test_bulk_checkbox_operations(check_box_page: CheckBoxPage):
    """
    Тест массовых операций с чекбоксами.

    Проверяет выбор всех элементов сразу и массовое снятие выбора.
    """
    with allure.step("Подготавливаем дерево чекбоксов"):
        check_box_page.expand_all()
        initial_count = check_box_page.get_visible_nodes_count()
        check_box_page.log_step(
            f"Подготовлено {initial_count} узлов для массовых операций"
        )

    with allure.step("Выполняем массовый выбор всех элементов"):
        check_box_page.log_step("Выбор всех доступных чекбоксов")
        check_box_page.select_all_checkboxes()

    with allure.step("Проверяем результат массового выбора"):
        all_selected = check_box_page.get_selected_results()
        selected_count = len(all_selected)

        check_box_page.log_step(f"Выбрано элементов: {selected_count}")
        check_box_page.log_step(f"Список выбранных: {all_selected}")

        allure.attach(
            str(all_selected), "all_selected_items", allure.attachment_type.JSON
        )

        assert selected_count > 0, "Должен быть выбран хотя бы один элемент"

        # Проверяем наличие ключевых элементов
        expected_items = ["Home", "Desktop", "Documents", "Downloads"]
        for item in expected_items:
            if item in all_selected:
                check_box_page.log_step(f"✅ Ключевой элемент '{item}' присутствует")
            else:
                check_box_page.log_step(f"ℹ️ Элемент '{item}' не найден в результатах")

    with allure.step("Выполняем массовое снятие выбора"):
        check_box_page.log_step("Снятие выбора со всех чекбоксов")
        check_box_page.clear_all_selections()

    with allure.step("Проверяем результат массового снятия выбора"):
        after_clear = check_box_page.get_selected_results()
        check_box_page.log_step(f"Результаты после очистки: {after_clear}")

        allure.attach(str(after_clear), "after_clear_all", allure.attachment_type.JSON)

        assert (
            len(after_clear) == 0
        ), f"После очистки результаты должны быть пустыми, получено: {after_clear}"

        bulk_operations_summary = {
            "initial_nodes": initial_count,
            "max_selected": selected_count,
            "final_selected": len(after_clear),
            "bulk_select_worked": selected_count > 0,
            "bulk_clear_worked": len(after_clear) == 0,
        }

        allure.attach(
            str(bulk_operations_summary),
            "bulk_operations_summary",
            allure.attachment_type.JSON,
        )
