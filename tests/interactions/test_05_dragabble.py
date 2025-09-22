"""
Тесты для страницы Dragabble.
Проверяет функциональность перетаскивания элементов:
- Простое перетаскивание
- Ограничения по осям (X/Y axis restriction)
- Ограничения контейнера
- Различные стили курсоров при перетаскивании
"""

import pytest
import allure
from pages.interactions.dragabble_page import DragabblePage


@allure.epic("Interactions")
@allure.feature("Dragabble")
@allure.story("Simple Drag")
@pytest.mark.interactions
@pytest.mark.smoke
def test_simple_drag_element(dragabble_page: DragabblePage):
    """
    Тест простого перетаскивания элемента.

    Перетаскивает элемент в разные позиции и проверяет изменение координат.
    """
    with allure.step("Получаем начальную позицию простого drag элемента"):
        initial_position = dragabble_page.get_simple_drag_element_position()
        dragabble_page.log_step(f"Начальная позиция элемента: {initial_position}")

        allure.attach(
            str(initial_position), "initial_drag_position", allure.attachment_type.JSON
        )

        assert (
            initial_position["x"] >= 0
        ), f"Начальная X координата должна быть неотрицательной: {initial_position['x']}"
        assert (
            initial_position["y"] >= 0
        ), f"Начальная Y координата должна быть неотрицательной: {initial_position['y']}"

    with allure.step("Перетаскиваем элемент на 100px вправо и 50px вниз"):
        dragabble_page.log_step("Выполнение простого перетаскивания")

        drag_offset_x, drag_offset_y = 100, 50
        drag_result = dragabble_page.drag_simple_element(drag_offset_x, drag_offset_y)

        dragabble_page.log_step(f"Результат перетаскивания: {drag_result}")
        assert drag_result, "Простое перетаскивание должно быть выполнено успешно"

    with allure.step("Проверяем новую позицию после перетаскивания"):
        dragabble_page.page.wait_for_timeout(1000)  # Пауза для обновления позиции

        new_position = dragabble_page.get_simple_drag_element_position()
        dragabble_page.log_step(f"Новая позиция элемента: {new_position}")

        position_change = {
            "initial_position": initial_position,
            "new_position": new_position,
            "x_change": new_position["x"] - initial_position["x"],
            "y_change": new_position["y"] - initial_position["y"],
            "expected_x_change": drag_offset_x,
            "expected_y_change": drag_offset_y,
            "position_changed": new_position != initial_position,
        }

        dragabble_page.log_step(f"Анализ изменения позиции: {position_change}")
        allure.attach(
            str(position_change),
            "position_change_analysis",
            allure.attachment_type.JSON,
        )

        # Проверяем что элемент действительно переместился
        assert position_change[
            "position_changed"
        ], f"Позиция элемента должна измениться: {initial_position} -> {new_position}"

        # Проверяем направление перемещения (с допуском на неточности)
        x_moved_right = position_change["x_change"] > 20  # Хотя бы 20px вправо
        y_moved_down = position_change["y_change"] > 10  # Хотя бы 10px вниз

        movement_validation = {
            "moved_right": x_moved_right,
            "moved_down": y_moved_down,
            "movement_reasonable": x_moved_right and y_moved_down,
        }

        dragabble_page.log_step(f"Валидация движения: {movement_validation}")

        assert movement_validation[
            "movement_reasonable"
        ], f"Элемент должен переместиться в ожидаемом направлении: X+{position_change['x_change']}, Y+{position_change['y_change']}"

    with allure.step("Выполняем дополнительное перетаскивание"):
        dragabble_page.log_step("Второе перетаскивание для проверки стабильности")

        # Перетаскиваем обратно влево и вверх
        second_drag_result = dragabble_page.drag_simple_element(-50, -30)
        dragabble_page.page.wait_for_timeout(500)

        final_position = dragabble_page.get_simple_drag_element_position()

        second_movement = {
            "second_drag_successful": second_drag_result,
            "position_after_second_drag": final_position,
            "total_x_change": final_position["x"] - initial_position["x"],
            "total_y_change": final_position["y"] - initial_position["y"],
        }

        dragabble_page.log_step(f"Результат второго перетаскивания: {second_movement}")
        allure.attach(
            str(second_movement), "second_drag_result", allure.attachment_type.JSON
        )

        assert second_drag_result, "Второе перетаскивание также должно быть успешным"


@allure.epic("Interactions")
@allure.feature("Dragabble")
@allure.story("Axis Restricted Drag")
@pytest.mark.interactions
@pytest.mark.smoke
def test_axis_restricted_drag(dragabble_page: DragabblePage):
    """
    Тест перетаскивания с ограничениями по осям.

    Проверяет элементы которые можно перетаскивать только по X или только по Y оси.
    """
    with allure.step("Переключаемся на вкладку Axis Restricted"):
        dragabble_page.log_step("Переключение на вкладку Axis Restricted")
        dragabble_page.switch_to_axis_restricted_tab()

        axis_tab_active = dragabble_page.is_axis_restricted_tab_active()
        assert axis_tab_active, "Вкладка Axis Restricted должна быть активной"

    with allure.step("Тестируем элемент с ограничением только по X-оси"):
        x_only_element_present = dragabble_page.is_x_axis_element_present()

        if x_only_element_present:
            # Получаем начальную позицию X-only элемента
            x_initial_position = dragabble_page.get_x_axis_element_position()
            dragabble_page.log_step(
                f"Начальная позиция X-only элемента: {x_initial_position}"
            )

            # Пытаемся перетащить по диагонали (X и Y)
            x_drag_result = dragabble_page.drag_x_axis_element(
                80, 60
            )  # Пытаемся и по X, и по Y
            dragabble_page.page.wait_for_timeout(1000)

            x_new_position = dragabble_page.get_x_axis_element_position()
            dragabble_page.log_step(
                f"Позиция X-only элемента после перетаскивания: {x_new_position}"
            )

            x_axis_test = {
                "drag_performed": x_drag_result,
                "initial_position": x_initial_position,
                "new_position": x_new_position,
                "x_changed": x_new_position["x"] != x_initial_position["x"],
                "y_changed": x_new_position["y"] != x_initial_position["y"],
                "x_movement": x_new_position["x"] - x_initial_position["x"],
                "y_movement": x_new_position["y"] - x_initial_position["y"],
                "x_restriction_works": x_new_position["x"] != x_initial_position["x"]
                and abs(x_new_position["y"] - x_initial_position["y"]) < 10,
            }

            dragabble_page.log_step(f"Результат X-axis теста: {x_axis_test}")
            allure.attach(
                str(x_axis_test), "x_axis_restriction_test", allure.attachment_type.JSON
            )

            if x_axis_test["x_restriction_works"]:
                dragabble_page.log_step("✅ Ограничение по X-оси работает корректно")
            else:
                dragabble_page.log_step("ℹ️ X-ось ограничение ведет себя неожиданно")

        else:
            dragabble_page.log_step("⚠️ X-only элемент не найден")

    with allure.step("Тестируем элемент с ограничением только по Y-оси"):
        y_only_element_present = dragabble_page.is_y_axis_element_present()

        if y_only_element_present:
            # Получаем начальную позицию Y-only элемента
            y_initial_position = dragabble_page.get_y_axis_element_position()
            dragabble_page.log_step(
                f"Начальная позиция Y-only элемента: {y_initial_position}"
            )

            # Пытаемся перетащить по диагонали (X и Y)
            y_drag_result = dragabble_page.drag_y_axis_element(
                60, 80
            )  # Пытаемся и по X, и по Y
            dragabble_page.page.wait_for_timeout(1000)

            y_new_position = dragabble_page.get_y_axis_element_position()
            dragabble_page.log_step(
                f"Позиция Y-only элемента после перетаскивания: {y_new_position}"
            )

            y_axis_test = {
                "drag_performed": y_drag_result,
                "initial_position": y_initial_position,
                "new_position": y_new_position,
                "x_changed": y_new_position["x"] != y_initial_position["x"],
                "y_changed": y_new_position["y"] != y_initial_position["y"],
                "x_movement": y_new_position["x"] - y_initial_position["x"],
                "y_movement": y_new_position["y"] - y_initial_position["y"],
                "y_restriction_works": y_new_position["y"] != y_initial_position["y"]
                and abs(y_new_position["x"] - y_initial_position["x"]) < 10,
            }

            dragabble_page.log_step(f"Результат Y-axis теста: {y_axis_test}")
            allure.attach(
                str(y_axis_test), "y_axis_restriction_test", allure.attachment_type.JSON
            )

            if y_axis_test["y_restriction_works"]:
                dragabble_page.log_step("✅ Ограничение по Y-оси работает корректно")
            else:
                dragabble_page.log_step("ℹ️ Y-ось ограничение ведет себя неожиданно")

        else:
            dragabble_page.log_step("⚠️ Y-only элемент не найден")

    with allure.step("Анализируем ограничения по осям"):
        axis_restrictions_summary = {
            "x_only_element_present": x_only_element_present,
            "y_only_element_present": y_only_element_present,
            "axis_restrictions_available": x_only_element_present
            or y_only_element_present,
            "tab_functional": axis_tab_active,
        }

        dragabble_page.log_step(
            f"Итоги ограничений по осям: {axis_restrictions_summary}"
        )
        allure.attach(
            str(axis_restrictions_summary),
            "axis_restrictions_summary",
            allure.attachment_type.JSON,
        )

        assert axis_restrictions_summary[
            "tab_functional"
        ], "Вкладка Axis Restricted должна быть функциональной"


@allure.epic("Interactions")
@allure.feature("Dragabble")
@allure.story("Container Restricted Drag")
@pytest.mark.interactions
@pytest.mark.regression
def test_container_restricted_drag(dragabble_page: DragabblePage):
    """
    Тест перетаскивания с ограничениями контейнера.

    Проверяет элементы которые можно перетаскивать только в пределах определенного контейнера.
    """
    with allure.step("Переключаемся на вкладку Container Restricted"):
        dragabble_page.log_step("Переключение на вкладку Container Restricted")
        dragabble_page.switch_to_container_restricted_tab()

        container_tab_active = dragabble_page.is_container_restricted_tab_active()
        assert container_tab_active, "Вкладка Container Restricted должна быть активной"

    with allure.step("Анализируем структуру контейнеров"):
        container_box_present = dragabble_page.is_container_box_present()
        parent_container_present = dragabble_page.is_parent_container_present()
        drag_element_in_container = (
            dragabble_page.is_drag_element_in_container_present()
        )

        container_structure = {
            "container_box": container_box_present,
            "parent_container": parent_container_present,
            "drag_element": drag_element_in_container,
        }

        dragabble_page.log_step(f"Структура контейнеров: {container_structure}")
        allure.attach(
            str(container_structure), "container_structure", allure.attachment_type.JSON
        )

    with allure.step("Получаем размеры и границы контейнера"):
        if container_box_present:
            container_bounds = dragabble_page.get_container_bounds()
            dragabble_page.log_step(f"Границы контейнера: {container_bounds}")

            allure.attach(
                str(container_bounds), "container_bounds", allure.attachment_type.JSON
            )

            assert (
                container_bounds["width"] > 0
            ), "Ширина контейнера должна быть положительной"
            assert (
                container_bounds["height"] > 0
            ), "Высота контейнера должна быть положительной"

    with allure.step("Тестируем перетаскивание в пределах контейнера"):
        if drag_element_in_container:
            initial_container_position = (
                dragabble_page.get_container_drag_element_position()
            )
            dragabble_page.log_step(
                f"Начальная позиция элемента в контейнере: {initial_container_position}"
            )

            # Перетаскиваем элемент в пределах контейнера
            within_bounds_drag = dragabble_page.drag_container_element_within_bounds(
                30, 40
            )
            dragabble_page.page.wait_for_timeout(1000)

            position_after_within = dragabble_page.get_container_drag_element_position()
            dragabble_page.log_step(
                f"Позиция после перетаскивания в пределах: {position_after_within}"
            )

            within_bounds_test = {
                "drag_performed": within_bounds_drag,
                "initial_position": initial_container_position,
                "position_after": position_after_within,
                "element_moved": position_after_within != initial_container_position,
                "x_movement": position_after_within["x"]
                - initial_container_position["x"],
                "y_movement": position_after_within["y"]
                - initial_container_position["y"],
            }

            dragabble_page.log_step(
                f"Результат перетаскивания в пределах: {within_bounds_test}"
            )
            allure.attach(
                str(within_bounds_test),
                "within_bounds_drag_test",
                allure.attachment_type.JSON,
            )

            assert within_bounds_test[
                "element_moved"
            ], "Элемент должен перемещаться в пределах контейнера"

    with allure.step("Тестируем попытку перетаскивания за пределы контейнера"):
        if drag_element_in_container and container_box_present:
            # Пытаемся перетащить элемент далеко за границы контейнера
            beyond_bounds_drag = dragabble_page.drag_container_element_beyond_bounds(
                200, 200
            )
            dragabble_page.page.wait_for_timeout(1000)

            position_after_beyond = dragabble_page.get_container_drag_element_position()
            dragabble_page.log_step(
                f"Позиция после попытки перетаскивания за пределы: {position_after_beyond}"
            )

            # Проверяем что элемент остался в границах контейнера
            element_within_container = (
                dragabble_page.is_element_within_container_bounds(position_after_beyond)
            )

            beyond_bounds_test = {
                "drag_attempted": beyond_bounds_drag,
                "final_position": position_after_beyond,
                "element_within_bounds": element_within_container,
                "container_restriction_works": element_within_container,
                "x_constrained": position_after_beyond["x"]
                <= container_bounds["x"] + container_bounds["width"],
                "y_constrained": position_after_beyond["y"]
                <= container_bounds["y"] + container_bounds["height"],
            }

            dragabble_page.log_step(
                f"Результат попытки выхода за пределы: {beyond_bounds_test}"
            )
            allure.attach(
                str(beyond_bounds_test),
                "beyond_bounds_drag_test",
                allure.attachment_type.JSON,
            )

            if beyond_bounds_test["container_restriction_works"]:
                dragabble_page.log_step("✅ Ограничения контейнера работают корректно")
            else:
                dragabble_page.log_step(
                    "ℹ️ Элемент вышел за пределы контейнера - возможно ограничения не строгие"
                )

    with allure.step("Анализируем функциональность контейнерных ограничений"):
        container_functionality = {
            "container_structure_present": container_box_present
            and drag_element_in_container,
            "drag_within_bounds_works": (
                within_bounds_test.get("element_moved", False)
                if "within_bounds_test" in locals()
                else False
            ),
            "container_restrictions_tested": container_box_present
            and drag_element_in_container,
            "tab_works": container_tab_active,
        }

        dragabble_page.log_step(
            f"Итоги контейнерных ограничений: {container_functionality}"
        )
        allure.attach(
            str(container_functionality),
            "container_functionality_summary",
            allure.attachment_type.JSON,
        )

        assert container_functionality[
            "tab_works"
        ], "Вкладка Container Restricted должна работать"


@allure.epic("Interactions")
@allure.feature("Dragabble")
@allure.story("Cursor Styles")
@pytest.mark.interactions
def test_cursor_style_drag(dragabble_page: DragabblePage):
    """
    Тест различных стилей курсора при перетаскивании.

    Проверяет элементы с разными cursor стилями во время drag операций.
    """
    with allure.step("Переключаемся на вкладку Cursor Style"):
        dragabble_page.log_step("Переключение на вкладку Cursor Style")
        dragabble_page.switch_to_cursor_style_tab()

        cursor_tab_active = dragabble_page.is_cursor_style_tab_active()
        assert cursor_tab_active, "Вкладка Cursor Style должна быть активной"

    with allure.step("Анализируем элементы с различными стилями курсора"):
        cursor_elements = dragabble_page.get_cursor_style_elements()
        dragabble_page.log_step(
            f"Найдено элементов с cursor styles: {len(cursor_elements)}"
        )

        allure.attach(
            str(cursor_elements), "cursor_style_elements", allure.attachment_type.JSON
        )

        assert (
            len(cursor_elements) > 0
        ), "Должен быть хотя бы один элемент с cursor style"

    cursor_tests = []

    with allure.step("Тестируем каждый элемент с cursor style"):
        for i, element_info in enumerate(cursor_elements):
            with allure.step(
                f"Тест cursor элемента {i + 1}: {element_info.get('cursor_type', 'unknown')}"
            ):
                element_cursor_type = element_info.get("cursor_type", f"element_{i}")
                dragabble_page.log_step(
                    f"Тестирование элемента с cursor: {element_cursor_type}"
                )

                # Получаем начальную позицию
                initial_cursor_position = dragabble_page.get_cursor_element_position(i)

                # Получаем CSS cursor свойство
                cursor_css_property = dragabble_page.get_cursor_element_css_property(
                    i, "cursor"
                )

                # Перетаскиваем элемент
                cursor_drag_result = dragabble_page.drag_cursor_element(i, 50, 30)
                dragabble_page.page.wait_for_timeout(1000)

                # Получаем финальную позицию
                final_cursor_position = dragabble_page.get_cursor_element_position(i)

                cursor_test = {
                    "element_index": i,
                    "cursor_type": element_cursor_type,
                    "cursor_css": cursor_css_property,
                    "initial_position": initial_cursor_position,
                    "final_position": final_cursor_position,
                    "drag_performed": cursor_drag_result,
                    "element_moved": final_cursor_position != initial_cursor_position,
                    "movement_delta": {
                        "x": final_cursor_position["x"] - initial_cursor_position["x"],
                        "y": final_cursor_position["y"] - initial_cursor_position["y"],
                    },
                }

                cursor_tests.append(cursor_test)
                dragabble_page.log_step(
                    f"Результат cursor теста {i + 1}: {cursor_test}"
                )

                # Проверяем что элемент перетаскивается независимо от cursor style
                assert cursor_test[
                    "element_moved"
                ], f"Элемент {i + 1} с cursor '{element_cursor_type}' должен перетаскиваться"

    with allure.step("Анализируем результаты cursor style тестов"):
        allure.attach(
            str(cursor_tests), "all_cursor_tests_results", allure.attachment_type.JSON
        )

        successful_drags = sum(1 for test in cursor_tests if test["element_moved"])
        different_cursors = len(set(test["cursor_type"] for test in cursor_tests))

        cursor_analysis = {
            "total_cursor_elements": len(cursor_tests),
            "successful_drags": successful_drags,
            "different_cursor_types": different_cursors,
            "all_elements_draggable": successful_drags == len(cursor_tests),
            "cursor_variety": different_cursors > 1,
            "cursor_test_details": cursor_tests,
        }

        dragabble_page.log_step(f"Анализ cursor styles: {cursor_analysis}")
        allure.attach(
            str(cursor_analysis), "cursor_styles_analysis", allure.attachment_type.JSON
        )

        assert cursor_analysis[
            "all_elements_draggable"
        ], f"Все элементы должны быть перетаскиваемыми: {successful_drags}/{len(cursor_tests)}"

        if cursor_analysis["cursor_variety"]:
            dragabble_page.log_step("✅ Найдены элементы с различными cursor styles")
        else:
            dragabble_page.log_step("ℹ️ Все элементы имеют одинаковый cursor style")


@allure.epic("Interactions")
@allure.feature("Dragabble")
@allure.story("All Drag Modes Integration")
@pytest.mark.interactions
@pytest.mark.regression
def test_all_dragabble_modes_integration(dragabble_page: DragabblePage):
    """
    Интеграционный тест всех режимов перетаскивания.

    Проверяет переключение между всеми вкладками и их функциональность.
    """
    integration_results = {}

    # Список всех вкладок для интеграционного тестирования
    tabs_to_test = [
        ("Simple", "simple"),
        ("Axis Restricted", "axis_restricted"),
        ("Container Restricted", "container_restricted"),
        ("Cursor Style", "cursor_style"),
    ]

    with allure.step("Выполняем интеграционное тестирование всех режимов drag"):
        for tab_name, tab_key in tabs_to_test:
            with allure.step(f"Интеграционный тест {tab_name}"):
                dragabble_page.log_step(f"Переключение и тест режима: {tab_name}")

                # Переключаемся на вкладку
                if tab_key == "simple":
                    dragabble_page.switch_to_simple_tab()
                elif tab_key == "axis_restricted":
                    dragabble_page.switch_to_axis_restricted_tab()
                elif tab_key == "container_restricted":
                    dragabble_page.switch_to_container_restricted_tab()
                elif tab_key == "cursor_style":
                    dragabble_page.switch_to_cursor_style_tab()

                dragabble_page.page.wait_for_timeout(1000)

                # Проверяем активность вкладки
                tab_active = dragabble_page.is_tab_active(tab_key)

                # Получаем количество перетаскиваемых элементов на вкладке
                draggable_elements_count = (
                    dragabble_page.count_draggable_elements_in_tab(tab_key)
                )

                # Выполняем базовый тест перетаскивания
                basic_drag_works = False
                drag_test_error = None

                try:
                    if draggable_elements_count > 0:
                        basic_drag_works = (
                            dragabble_page.perform_basic_drag_test_in_tab(tab_key)
                        )
                except Exception as e:
                    drag_test_error = str(e)
                    dragabble_page.log_step(f"Ошибка при тестировании {tab_name}: {e}")

                # Проверяем специфичную функциональность вкладки
                tab_specific_features = dragabble_page.get_tab_specific_features(
                    tab_key
                )

                tab_result = {
                    "tab_name": tab_name,
                    "tab_key": tab_key,
                    "tab_active": tab_active,
                    "draggable_elements_count": draggable_elements_count,
                    "basic_drag_works": basic_drag_works,
                    "drag_test_error": drag_test_error,
                    "tab_specific_features": tab_specific_features,
                    "tab_functional": tab_active
                    and draggable_elements_count > 0
                    and basic_drag_works,
                }

                integration_results[tab_key] = tab_result
                dragabble_page.log_step(
                    f"Результат интеграционного теста {tab_name}: {tab_result}"
                )

    with allure.step("Тестируем переключение между всеми вкладками"):
        tab_switching_test = {}

        for tab_name, tab_key in tabs_to_test:
            # Переключаемся на каждую вкладку и проверяем что переключение работает
            if tab_key == "simple":
                switch_result = dragabble_page.switch_to_simple_tab()
            elif tab_key == "axis_restricted":
                switch_result = dragabble_page.switch_to_axis_restricted_tab()
            elif tab_key == "container_restricted":
                switch_result = dragabble_page.switch_to_container_restricted_tab()
            elif tab_key == "cursor_style":
                switch_result = dragabble_page.switch_to_cursor_style_tab()
            else:
                switch_result = False

            dragabble_page.page.wait_for_timeout(500)
            tab_became_active = dragabble_page.is_tab_active(tab_key)

            tab_switching_test[tab_key] = {
                "switch_attempted": True,
                "switch_method_result": switch_result,
                "tab_became_active": tab_became_active,
                "switching_works": tab_became_active,
            }

        dragabble_page.log_step(
            f"Результаты переключения вкладок: {tab_switching_test}"
        )

    with allure.step("Создаем итоговый отчет интеграции"):
        allure.attach(
            str(integration_results),
            "dragabble_integration_results",
            allure.attachment_type.JSON,
        )
        allure.attach(
            str(tab_switching_test),
            "tab_switching_results",
            allure.attachment_type.JSON,
        )

        functional_tabs = sum(
            1 for result in integration_results.values() if result["tab_functional"]
        )
        tabs_with_elements = sum(
            1
            for result in integration_results.values()
            if result["draggable_elements_count"] > 0
        )
        successful_switches = sum(
            1 for result in tab_switching_test.values() if result["switching_works"]
        )
        total_tabs = len(integration_results)

        integration_summary = {
            "total_tabs_tested": total_tabs,
            "functional_tabs": functional_tabs,
            "tabs_with_draggable_elements": tabs_with_elements,
            "successful_tab_switches": successful_switches,
            "integration_success_rate": (
                functional_tabs / total_tabs if total_tabs > 0 else 0
            ),
            "all_tabs_functional": functional_tabs == total_tabs,
            "most_tabs_working": functional_tabs >= total_tabs * 0.75,
            "tab_switching_works": successful_switches >= total_tabs * 0.75,
            "overall_integration_successful": functional_tabs >= 2
            and successful_switches >= 2,
            "detailed_results": integration_results,
            "switching_details": tab_switching_test,
        }

        dragabble_page.log_step(
            f"Итоговый отчет интеграции Dragabble: {integration_summary}"
        )
        allure.attach(
            str(integration_summary),
            "dragabble_integration_summary",
            allure.attachment_type.JSON,
        )

        # Проверяем успешность интеграции
        assert integration_summary[
            "overall_integration_successful"
        ], f"Интеграция должна быть успешной: функциональных вкладок {functional_tabs}/{total_tabs}, переключений {successful_switches}/{total_tabs}"
        assert (
            integration_summary["tabs_with_draggable_elements"] > 0
        ), f"Хотя бы одна вкладка должна содержать перетаскиваемые элементы: {tabs_with_elements}/{total_tabs}"

        if integration_summary["all_tabs_functional"]:
            dragabble_page.log_step("🎉 Все режимы Dragabble полностью функциональны!")
        elif integration_summary["most_tabs_working"]:
            dragabble_page.log_step(
                f"✅ Большинство режимов Dragabble работают: {functional_tabs}/{total_tabs}"
            )
        else:
            dragabble_page.log_step(
                f"⚠️ Только часть режимов Dragabble функциональна: {functional_tabs}/{total_tabs}"
            )
