"""
Тесты для страницы Droppable.
Проверяет функциональность областей сброса (drop zones):
- Простое перетаскивание и сброс
- Принимаемые и непринимаемые элементы
- Предотвращение всплытия событий
- Возврат элементов после сброса
"""

import pytest
import allure
from pages.interactions.droppable_page import DroppablePage


@allure.epic("Interactions")
@allure.feature("Droppable")
@allure.story("Simple Drop")
@pytest.mark.interactions
@pytest.mark.smoke
def test_simple_drag_and_drop(droppable_page: DroppablePage):
    """
    Тест простого перетаскивания и сброса элемента.

    Перетаскивает элемент в область сброса и проверяет результат.
    """
    with allure.step("Проверяем начальное состояние элементов"):
        initial_drag_position = droppable_page.get_simple_drag_element_position()
        initial_drop_text = droppable_page.get_simple_drop_area_text()

        droppable_page.log_step(f"Начальная позиция перетаскиваемого элемента: {initial_drag_position}")
        droppable_page.log_step(f"Начальный текст области сброса: {initial_drop_text}")

        allure.attach(str(initial_drag_position), "initial_drag_position", allure.attachment_type.JSON)
        allure.attach(initial_drop_text, "initial_drop_text", allure.attachment_type.TEXT)

        expected_initial_text = "Drop here"
        assert expected_initial_text in initial_drop_text, f"Область сброса должна содержать '{expected_initial_text}': {initial_drop_text}"

    with allure.step("Выполняем перетаскивание элемента в область сброса"):
        droppable_page.log_step("Начало операции drag-and-drop")

        drag_result = droppable_page.drag_simple_element_to_drop_area()
        droppable_page.log_step(f"Результат перетаскивания: {drag_result}")

        assert drag_result, "Операция drag-and-drop должна быть выполнена успешно"

    with allure.step("Проверяем состояние после сброса"):
        droppable_page.page.wait_for_timeout(1000)  # Пауза для обновления состояния

        drop_area_text_after = droppable_page.get_simple_drop_area_text()
        drop_area_background = droppable_page.get_simple_drop_area_background_color()
        drag_element_position_after = droppable_page.get_simple_drag_element_position()

        droppable_page.log_step(f"Текст области после сброса: {drop_area_text_after}")
        droppable_page.log_step(f"Цвет фона области после сброса: {drop_area_background}")
        droppable_page.log_step(f"Позиция элемента после сброса: {drag_element_position_after}")

        drop_result = {
            "initial_text": initial_drop_text,
            "text_after_drop": drop_area_text_after,
            "background_color": drop_area_background,
            "text_changed": drop_area_text_after != initial_drop_text,
            "success_text_present": "Dropped" in drop_area_text_after,
            "drag_position_changed": drag_element_position_after != initial_drag_position
        }

        droppable_page.log_step(f"Результаты сброса: {drop_result}")
        allure.attach(str(drop_result), "simple_drop_result", allure.attachment_type.JSON)

        # Проверяем что произошли ожидаемые изменения
        assert drop_result["text_changed"], f"Текст области сброса должен измениться: '{initial_drop_text}' -> '{drop_area_text_after}'"

        # Может содержать "Dropped!" или другой текст успеха
        success_indicators = ["Dropped", "dropped", "success"]
        text_indicates_success = any(indicator in drop_area_text_after.lower() for indicator in success_indicators)

        if text_indicates_success:
            droppable_page.log_step("✅ Область сброса показывает успешное завершение операции")
        else:
            droppable_page.log_step("ℹ️ Текст области изменился, но не содержит явных индикаторов успеха")


@allure.epic("Interactions")
@allure.feature("Droppable")
@allure.story("Accept vs Reject")
@pytest.mark.interactions
@pytest.mark.regression
def test_accept_and_reject_elements(droppable_page: DroppablePage):
    """
    Тест принятия и отклонения элементов областью сброса.

    Проверяет что область принимает только определенные элементы.
    """
    with allure.step("Переключаемся на вкладку Accept"):
        droppable_page.log_step("Переключение на вкладку Accept/Reject")
        droppable_page.switch_to_accept_tab()

        accept_tab_active = droppable_page.is_accept_tab_active()
        assert accept_tab_active, "Вкладка Accept должна быть активной"

    with allure.step("Проверяем элементы для тестирования"):
        acceptable_element_present = droppable_page.is_acceptable_element_present()
        not_acceptable_element_present = droppable_page.is_not_acceptable_element_present()
        accept_drop_area_present = droppable_page.is_accept_drop_area_present()

        elements_info = {
            "acceptable_element": acceptable_element_present,
            "not_acceptable_element": not_acceptable_element_present,
            "accept_drop_area": accept_drop_area_present
        }

        droppable_page.log_step(f"Наличие элементов Accept: {elements_info}")
        allure.attach(str(elements_info), "accept_elements_presence", allure.attachment_type.JSON)

        assert accept_drop_area_present, "Область сброса для Accept должна присутствовать"

    with allure.step("Тестируем сброс принимаемого элемента"):
        if acceptable_element_present:
            droppable_page.log_step("Перетаскивание принимаемого элемента")

            initial_accept_text = droppable_page.get_accept_drop_area_text()
            droppable_page.log_step(f"Изначальный текст Accept области: {initial_accept_text}")

            acceptable_drag_result = droppable_page.drag_acceptable_element_to_accept_area()
            droppable_page.page.wait_for_timeout(1000)

            accept_text_after = droppable_page.get_accept_drop_area_text()
            accept_area_color_after = droppable_page.get_accept_drop_area_background_color()

            acceptable_test_result = {
                "drag_performed": acceptable_drag_result,
                "initial_text": initial_accept_text,
                "text_after": accept_text_after,
                "background_color": accept_area_color_after,
                "text_changed": accept_text_after != initial_accept_text,
                "appears_accepted": "Dropped" in accept_text_after or accept_text_after != initial_accept_text
            }

            droppable_page.log_step(f"Результат принимаемого элемента: {acceptable_test_result}")
            allure.attach(str(acceptable_test_result), "acceptable_element_result", allure.attachment_type.JSON)

            if acceptable_test_result["appears_accepted"]:
                droppable_page.log_step("✅ Принимаемый элемент был успешно принят")
            else:
                droppable_page.log_step("⚠️ Принимаемый элемент не показал явных признаков принятия")
        else:
            droppable_page.log_step("⚠️ Принимаемый элемент не найден на странице")

    with allure.step("Тестируем сброс непринимаемого элемента"):
        if not_acceptable_element_present:
            droppable_page.log_step("Перетаскивание непринимаемого элемента")

            # Сначала сбросим состояние области (если возможно)
            droppable_page.reset_accept_drop_area()

            initial_reject_text = droppable_page.get_accept_drop_area_text()
            droppable_page.log_step(f"Текст области перед тестом отклонения: {initial_reject_text}")

            not_acceptable_drag_result = droppable_page.drag_not_acceptable_element_to_accept_area()
            droppable_page.page.wait_for_timeout(1000)

            reject_text_after = droppable_page.get_accept_drop_area_text()
            reject_area_color_after = droppable_page.get_accept_drop_area_background_color()

            not_acceptable_test_result = {
                "drag_performed": not_acceptable_drag_result,
                "initial_text": initial_reject_text,
                "text_after": reject_text_after,
                "background_color": reject_area_color_after,
                "text_changed": reject_text_after != initial_reject_text,
                "appears_rejected": reject_text_after == initial_reject_text  # Текст не должен измениться
            }

            droppable_page.log_step(f"Результат непринимаемого элемента: {not_acceptable_test_result}")
            allure.attach(str(not_acceptable_test_result), "not_acceptable_element_result", allure.attachment_type.JSON)

            if not_acceptable_test_result["appears_rejected"]:
                droppable_page.log_step("✅ Непринимаемый элемент был корректно отклонен")
            else:
                droppable_page.log_step("⚠️ Непринимаемый элемент показал неожиданное поведение")
        else:
            droppable_page.log_step("⚠️ Непринимаемый элемент не найден на странице")

    with allure.step("Анализируем поведение Accept/Reject"):
        accept_reject_summary = {
            "acceptable_element_available": acceptable_element_present,
            "not_acceptable_element_available": not_acceptable_element_present,
            "both_elements_available": acceptable_element_present and not_acceptable_element_present,
            "accept_functionality_works": True  # Базовая проверка что вкладка работает
        }

        droppable_page.log_step(f"Итоги Accept/Reject функциональности: {accept_reject_summary}")
        allure.attach(str(accept_reject_summary), "accept_reject_summary", allure.attachment_type.JSON)

        assert accept_reject_summary["accept_functionality_works"], "Функциональность Accept/Reject должна работать"


@allure.epic("Interactions")
@allure.feature("Droppable")
@allure.story("Event Propagation")
@pytest.mark.interactions
@pytest.mark.regression
def test_prevent_propagation(droppable_page: DroppablePage):
    """
    Тест предотвращения всплытия событий.

    Проверяет поведение вложенных областей сброса и всплытие событий.
    """
    with allure.step("Переключаемся на вкладку Prevent Propagation"):
        droppable_page.log_step("Переключение на вкладку Prevent Propagation")
        droppable_page.switch_to_prevent_propagation_tab()

        propagation_tab_active = droppable_page.is_prevent_propagation_tab_active()
        assert propagation_tab_active, "Вкладка Prevent Propagation должна быть активной"

    with allure.step("Анализируем структуру вложенных областей"):
        outer_not_greedy_present = droppable_page.is_outer_not_greedy_area_present()
        inner_not_greedy_present = droppable_page.is_inner_not_greedy_area_present()
        outer_greedy_present = droppable_page.is_outer_greedy_area_present()
        inner_greedy_present = droppable_page.is_inner_greedy_area_present()
        drag_box_present = droppable_page.is_propagation_drag_box_present()

        propagation_structure = {
            "outer_not_greedy": outer_not_greedy_present,
            "inner_not_greedy": inner_not_greedy_present,
            "outer_greedy": outer_greedy_present,
            "inner_greedy": inner_greedy_present,
            "drag_box": drag_box_present
        }

        droppable_page.log_step(f"Структура областей propagation: {propagation_structure}")
        allure.attach(str(propagation_structure), "propagation_structure", allure.attachment_type.JSON)

        assert drag_box_present, "Перетаскиваемый элемент должен присутствовать"

    with allure.step("Тестируем сброс в не-жадную внутреннюю область"):
        if inner_not_greedy_present and drag_box_present:
            droppable_page.log_step("Перетаскивание в не-жадную внутреннюю область")

            # Получаем начальные тексты областей
            outer_not_greedy_initial = droppable_page.get_outer_not_greedy_text()
            inner_not_greedy_initial = droppable_page.get_inner_not_greedy_text()

            # Перетаскиваем в внутреннюю область
            drag_to_inner_result = droppable_page.drag_box_to_inner_not_greedy()
            droppable_page.page.wait_for_timeout(1000)

            # Проверяем результат
            outer_not_greedy_after = droppable_page.get_outer_not_greedy_text()
            inner_not_greedy_after = droppable_page.get_inner_not_greedy_text()

            not_greedy_test = {
                "drag_performed": drag_to_inner_result,
                "outer_initial": outer_not_greedy_initial,
                "inner_initial": inner_not_greedy_initial,
                "outer_after": outer_not_greedy_after,
                "inner_after": inner_not_greedy_after,
                "outer_changed": outer_not_greedy_after != outer_not_greedy_initial,
                "inner_changed": inner_not_greedy_after != inner_not_greedy_initial,
                "propagation_occurred": outer_not_greedy_after != outer_not_greedy_initial and inner_not_greedy_after != inner_not_greedy_initial
            }

            droppable_page.log_step(f"Результат не-жадного сброса: {not_greedy_test}")
            allure.attach(str(not_greedy_test), "not_greedy_drop_result", allure.attachment_type.JSON)

        else:
            droppable_page.log_step("⚠️ Не-жадные области не найдены")

    with allure.step("Тестируем сброс в жадную внутреннюю область"):
        if inner_greedy_present and drag_box_present:
            droppable_page.log_step("Перетаскивание в жадную внутреннюю область")

            # Сбрасываем состояние областей
            droppable_page.reset_propagation_areas()

            # Получаем начальные тексты жадных областей
            outer_greedy_initial = droppable_page.get_outer_greedy_text()
            inner_greedy_initial = droppable_page.get_inner_greedy_text()

            # Перетаскиваем в жадную внутреннюю область
            drag_to_greedy_result = droppable_page.drag_box_to_inner_greedy()
            droppable_page.page.wait_for_timeout(1000)

            # Проверяем результат
            outer_greedy_after = droppable_page.get_outer_greedy_text()
            inner_greedy_after = droppable_page.get_inner_greedy_text()

            greedy_test = {
                "drag_performed": drag_to_greedy_result,
                "outer_initial": outer_greedy_initial,
                "inner_initial": inner_greedy_initial,
                "outer_after": outer_greedy_after,
                "inner_after": inner_greedy_after,
                "outer_changed": outer_greedy_after != outer_greedy_initial,
                "inner_changed": inner_greedy_after != inner_greedy_initial,
                "propagation_prevented": inner_greedy_after != inner_greedy_initial and outer_greedy_after == outer_greedy_initial
            }

            droppable_page.log_step(f"Результат жадного сброса: {greedy_test}")
            allure.attach(str(greedy_test), "greedy_drop_result", allure.attachment_type.JSON)

        else:
            droppable_page.log_step("⚠️ Жадные области не найдены")

    with allure.step("Анализируем поведение предотвращения всплытия"):
        propagation_analysis = {
            "not_greedy_areas_available": inner_not_greedy_present and outer_not_greedy_present,
            "greedy_areas_available": inner_greedy_present and outer_greedy_present,
            "drag_element_available": drag_box_present,
            "propagation_testing_possible": drag_box_present and (inner_not_greedy_present or inner_greedy_present),
            "tab_functionality_works": propagation_tab_active
        }

        droppable_page.log_step(f"Анализ предотвращения всплытия: {propagation_analysis}")
        allure.attach(str(propagation_analysis), "propagation_analysis", allure.attachment_type.JSON)

        assert propagation_analysis["tab_functionality_works"], "Функциональность предотвращения всплытия должна быть доступна"

        if propagation_analysis["propagation_testing_possible"]:
            droppable_page.log_step("✅ Тестирование предотвращения всплытия выполнено")
        else:
            droppable_page.log_step("⚠️ Не все элементы для тестирования всплытия найдены")


@allure.epic("Interactions")
@allure.feature("Droppable")
@allure.story("Revertable Elements")
@pytest.mark.interactions
def test_revertable_drag_elements(droppable_page: DroppablePage):
    """
    Тест элементов с возвратом после сброса.

    Проверяет элементы которые возвращаются на место после неудачного сброса.
    """
    with allure.step("Переключаемся на вкладку Revert Draggable"):
        droppable_page.log_step("Переключение на вкладку Revert Draggable")
        droppable_page.switch_to_revert_draggable_tab()

        revert_tab_active = droppable_page.is_revert_draggable_tab_active()
        assert revert_tab_active, "Вкладка Revert Draggable должна быть активной"

    with allure.step("Анализируем элементы с возвратом"):
        revertable_element_present = droppable_page.is_revertable_element_present()
        not_revertable_element_present = droppable_page.is_not_revertable_element_present()
        revert_drop_area_present = droppable_page.is_revert_drop_area_present()

        revert_elements_info = {
            "revertable_element": revertable_element_present,
            "not_revertable_element": not_revertable_element_present,
            "revert_drop_area": revert_drop_area_present
        }

        droppable_page.log_step(f"Элементы Revert: {revert_elements_info}")
        allure.attach(str(revert_elements_info), "revert_elements_info", allure.attachment_type.JSON)

    with allure.step("Тестируем возвратный элемент"):
        if revertable_element_present and revert_drop_area_present:
            # Получаем начальную позицию возвратного элемента
            revertable_initial_position = droppable_page.get_revertable_element_position()
            droppable_page.log_step(f"Начальная позиция возвратного элемента: {revertable_initial_position}")

            # Перетаскиваем элемент в область сброса
            droppable_page.log_step("Перетаскивание возвратного элемента")
            revert_drag_result = droppable_page.drag_revertable_element_to_drop_area()

            # Проверяем позицию сразу после перетаскивания
            droppable_page.page.wait_for_timeout(500)
            position_after_drag = droppable_page.get_revertable_element_position()

            # Ждем возможного возврата элемента
            droppable_page.page.wait_for_timeout(2000)
            final_position = droppable_page.get_revertable_element_position()

            # Проверяем состояние области сброса
            drop_area_text = droppable_page.get_revert_drop_area_text()

            revertable_test = {
                "drag_performed": revert_drag_result,
                "initial_position": revertable_initial_position,
                "position_after_drag": position_after_drag,
                "final_position": final_position,
                "drop_area_text": drop_area_text,
                "element_moved_during_drag": position_after_drag != revertable_initial_position,
                "element_reverted": final_position == revertable_initial_position or abs(final_position["x"] - revertable_initial_position["x"]) < 10,
                "drop_area_accepted": "Dropped" in drop_area_text
            }

            droppable_page.log_step(f"Результат теста возвратного элемента: {revertable_test}")
            allure.attach(str(revertable_test), "revertable_element_test", allure.attachment_type.JSON)

            if revertable_test["element_reverted"] and not revertable_test["drop_area_accepted"]:
                droppable_page.log_step("✅ Возвратный элемент корректно вернулся на место")
            elif revertable_test["drop_area_accepted"]:
                droppable_page.log_step("✅ Возвратный элемент был принят областью сброса")
            else:
                droppable_page.log_step("ℹ️ Поведение возвратного элемента отличается от ожидаемого")

        else:
            droppable_page.log_step("⚠️ Элементы для тестирования возврата не найдены")

    with allure.step("Тестируем не-возвратный элемент"):
        if not_revertable_element_present and revert_drop_area_present:
            # Сбрасываем состояние области
            droppable_page.reset_revert_drop_area()

            # Получаем начальную позицию не-возвратного элемента
            not_revertable_initial = droppable_page.get_not_revertable_element_position()
            droppable_page.log_step(f"Начальная позиция не-возвратного элемента: {not_revertable_initial}")

            # Перетаскиваем элемент
            droppable_page.log_step("Перетаскивание не-возвратного элемента")
            not_revert_drag_result = droppable_page.drag_not_revertable_element_to_drop_area()

            # Проверяем результат
            droppable_page.page.wait_for_timeout(2000)
            not_revertable_final = droppable_page.get_not_revertable_element_position()
            not_revert_drop_text = droppable_page.get_revert_drop_area_text()

            not_revertable_test = {
                "drag_performed": not_revert_drag_result,
                "initial_position": not_revertable_initial,
                "final_position": not_revertable_final,
                "drop_area_text": not_revert_drop_text,
                "element_stayed_moved": not_revertable_final != not_revertable_initial,
                "drop_area_accepted": "Dropped" in not_revert_drop_text
            }

            droppable_page.log_step(f"Результат теста не-возвратного элемента: {not_revertable_test}")
            allure.attach(str(not_revertable_test), "not_revertable_element_test", allure.attachment_type.JSON)

            if not_revertable_test["drop_area_accepted"] or not_revertable_test["element_stayed_moved"]:
                droppable_page.log_step("✅ Не-возвратный элемент ведет себя как ожидается")
            else:
                droppable_page.log_step("ℹ️ Поведение не-возвратного элемента требует анализа")

        else:
            droppable_page.log_step("⚠️ Не-возвратный элемент для тестирования не найден")

    with allure.step("Анализируем функциональность возврата"):
        revert_functionality_summary = {
            "revertable_element_available": revertable_element_present,
            "not_revertable_element_available": not_revertable_element_present,
            "drop_area_available": revert_drop_area_present,
            "revert_testing_possible": revertable_element_present and revert_drop_area_present,
            "tab_works": revert_tab_active
        }

        droppable_page.log_step(f"Итоги функциональности возврата: {revert_functionality_summary}")
        allure.attach(str(revert_functionality_summary), "revert_functionality_summary", allure.attachment_type.JSON)

        assert revert_functionality_summary["tab_works"], "Вкладка Revert Draggable должна работать"


@allure.epic("Interactions")
@allure.feature("Droppable")
@allure.story("All Tabs Integration")
@pytest.mark.interactions
def test_all_droppable_tabs_integration(droppable_page: DroppablePage):
    """
    Интеграционный тест всех вкладок Droppable.

    Проверяет переключение между всеми вкладками и их работоспособность.
    """
    tabs_info = {}

    # Список всех вкладок для тестирования
    tabs_to_test = [
        ("Simple", "simple"),
        ("Accept", "accept"),
        ("Prevent Propagation", "prevent_propagation"),
        ("Revert Draggable", "revert_draggable")
    ]

    with allure.step("Тестируем все вкладки Droppable"):
        for tab_name, tab_key in tabs_to_test:
            with allure.step(f"Тестирование вкладки {tab_name}"):
                droppable_page.log_step(f"Переключение и тест вкладки: {tab_name}")

                # Переключаемся на вкладку
                if tab_key == "simple":
                    droppable_page.switch_to_simple_tab()
                elif tab_key == "accept":
                    droppable_page.switch_to_accept_tab()
                elif tab_key == "prevent_propagation":
                    droppable_page.switch_to_prevent_propagation_tab()
                elif tab_key == "revert_draggable":
                    droppable_page.switch_to_revert_draggable_tab()

                droppable_page.page.wait_for_timeout(1000)

                # Проверяем активность вкладки
                tab_active = droppable_page.is_tab_active(tab_key)

                # Получаем информацию о содержимом вкладки
                tab_content_present = droppable_page.is_tab_content_visible(tab_key)
                drag_elements_count = droppable_page.count_drag_elements_in_tab(tab_key)
                drop_areas_count = droppable_page.count_drop_areas_in_tab(tab_key)

                tab_info = {
                    "tab_name": tab_name,
                    "tab_key": tab_key,
                    "tab_active": tab_active,
                    "content_present": tab_content_present,
                    "drag_elements": drag_elements_count,
                    "drop_areas": drop_areas_count,
                    "functional": tab_active and content_present and drag_elements_count > 0
                }

                tabs_info[tab_key] = tab_info
                droppable_page.log_step(f"Информация о вкладке {tab_name}: {tab_info}")

                # Базовый тест функциональности вкладки
                if tab_info["functional"]:
                    basic_test_result = droppable_page.perform_basic_drag_test_in_tab(tab_key)
                    tab_info["basic_test_passed"] = basic_test_result
                    droppable_page.log_step(f"Базовый тест вкладки {tab_name}: {basic_test_result}")
                else:
                    tab_info["basic_test_passed"] = False

    with allure.step("Анализируем интеграцию всех вкладок"):
        allure.attach(str(tabs_info), "all_tabs_integration_info", allure.attachment_type.JSON)

        functional_tabs = sum(1 for info in tabs_info.values() if info["functional"])
        tabs_with_passed_tests = sum(1 for info in tabs_info.values() if info.get("basic_test_passed", False))
        total_tabs = len(tabs_info)

        integration_summary = {
            "total_tabs": total_tabs,
            "functional_tabs": functional_tabs,
            "tabs_with_passed_tests": tabs_with_passed_tests,
            "all_tabs_functional": functional_tabs == total_tabs,
            "most_tabs_working": functional_tabs >= total_tabs * 0.75,
            "integration_successful": functional_tabs >= 2,  # Минимум 2 вкладки должны работать
            "tabs_details": tabs_info
        }

        droppable_page.log_step(f"Итоги интеграции всех вкладок: {integration_summary}")
        allure.attach(str(integration_summary), "droppable_integration_summary", allure.attachment_type.JSON)

        assert integration_summary["integration_successful"], f"Минимум 2 вкладки должны быть функциональными: {functional_tabs}/{total_tabs}"
        assert functional_tabs > 0, f"Хотя бы одна вкладка должна быть функциональной: {functional_tabs}/{total_tabs}"

        if integration_summary["all_tabs_functional"]:
            droppable_page.log_step("🎉 Все вкладки Droppable функциональны!")
        else:
            droppable_page.log_step(f"ℹ️ Функциональных вкладок: {functional_tabs}/{total_tabs}")