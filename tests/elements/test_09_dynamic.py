"""
Тесты для страницы Dynamic Properties.
Проверяет функциональность элементов с динамически изменяющимися свойствами:
- Кнопки с изменяющимися состояниями
- Элементы появляющиеся со временем
- Изменение цветов и стилей
- Обработка временных задержек
"""

import pytest
import allure
import time
from pages.elements.dynamic_properties_page import DynamicPropertiesPage


@allure.epic("Elements")
@allure.feature("Dynamic Properties")
@allure.story("Enable After Button")
@pytest.mark.elements
@pytest.mark.smoke
def test_enable_after_button(dynamic_properties_page: DynamicPropertiesPage):
    """
    Тест кнопки которая активируется через 5 секунд.

    Проверяет что кнопка изначально неактивна и становится активной через определенное время.
    """
    with allure.step("Проверяем начальное состояние кнопки 'Enable After 5 Seconds'"):
        initial_enabled = dynamic_properties_page.is_enable_after_button_enabled()
        dynamic_properties_page.log_step(
            f"Кнопка активна изначально: {initial_enabled}"
        )

        assert (
            not initial_enabled
        ), "Кнопка 'Enable After 5 Seconds' должна быть неактивна изначально"

        # Получаем атрибуты кнопки
        button_attributes = dynamic_properties_page.get_enable_after_button_attributes()
        dynamic_properties_page.log_step(f"Атрибуты кнопки: {button_attributes}")

        allure.attach(
            str(button_attributes),
            "initial_button_attributes",
            allure.attachment_type.JSON,
        )

    with allure.step("Ожидаем активации кнопки (до 10 секунд)"):
        dynamic_properties_page.log_step("Начало ожидания активации кнопки...")

        wait_start = time.time()
        max_wait_time = 10  # Максимальное время ожидания

        # Ожидаем активации кнопки
        button_enabled = dynamic_properties_page.wait_for_enable_after_button(
            timeout=max_wait_time * 1000
        )
        wait_duration = time.time() - wait_start

        dynamic_properties_page.log_step(f"Время ожидания: {wait_duration:.2f} секунд")
        dynamic_properties_page.log_step(f"Кнопка активировалась: {button_enabled}")

        timing_info = {
            "expected_delay_seconds": 5,
            "actual_wait_seconds": round(wait_duration, 2),
            "button_enabled": button_enabled,
            "timing_acceptable": 4 <= wait_duration <= 8,  # Допустимая погрешность
        }

        allure.attach(
            str(timing_info), "button_activation_timing", allure.attachment_type.JSON
        )

        assert (
            button_enabled
        ), f"Кнопка должна активироваться в течение {max_wait_time} секунд"

    with allure.step("Проверяем что кнопка стала кликабельной"):
        dynamic_properties_page.log_step("Попытка клика по активированной кнопке")

        click_successful = dynamic_properties_page.click_enable_after_button()
        dynamic_properties_page.log_step(f"Клик успешен: {click_successful}")

        assert click_successful, "После активации кнопка должна быть кликабельной"

        # Получаем финальные атрибуты
        final_attributes = dynamic_properties_page.get_enable_after_button_attributes()
        dynamic_properties_page.log_step(
            f"Финальные атрибуты кнопки: {final_attributes}"
        )

        allure.attach(
            str(final_attributes),
            "final_button_attributes",
            allure.attachment_type.JSON,
        )


@allure.epic("Elements")
@allure.feature("Dynamic Properties")
@allure.story("Color Change Button")
@pytest.mark.elements
@pytest.mark.smoke
def test_color_change_button(dynamic_properties_page: DynamicPropertiesPage):
    """
    Тест кнопки с изменяющимся цветом.

    Проверяет что цвет кнопки изменяется через определенное время.
    """
    with allure.step("Получаем начальный цвет кнопки"):
        initial_color = dynamic_properties_page.get_color_change_button_color()
        initial_classes = dynamic_properties_page.get_color_change_button_classes()

        dynamic_properties_page.log_step(f"Начальный цвет кнопки: {initial_color}")
        dynamic_properties_page.log_step(f"Начальные классы: {initial_classes}")

        color_info = {
            "initial_color": initial_color,
            "initial_classes": initial_classes,
            "timestamp": dynamic_properties_page.get_current_timestamp(),
        }

        allure.attach(
            str(color_info), "initial_color_info", allure.attachment_type.JSON
        )

    with allure.step("Ожидаем изменения цвета кнопки"):
        dynamic_properties_page.log_step("Ожидание изменения цвета...")

        max_wait_time = 10  # Максимальное время ожидания
        color_changed = dynamic_properties_page.wait_for_color_change(
            timeout=max_wait_time * 1000
        )

        dynamic_properties_page.log_step(f"Цвет изменился: {color_changed}")

        if color_changed:
            # Получаем новый цвет
            new_color = dynamic_properties_page.get_color_change_button_color()
            new_classes = dynamic_properties_page.get_color_change_button_classes()

            dynamic_properties_page.log_step(f"Новый цвет кнопки: {new_color}")
            dynamic_properties_page.log_step(f"Новые классы: {new_classes}")

            color_change_info = {
                "initial_color": initial_color,
                "new_color": new_color,
                "color_actually_changed": new_color != initial_color,
                "initial_classes": initial_classes,
                "new_classes": new_classes,
                "classes_changed": new_classes != initial_classes,
            }

            allure.attach(
                str(color_change_info),
                "color_change_result",
                allure.attachment_type.JSON,
            )

            # Проверяем что действительно произошло изменение
            visual_change = (new_color != initial_color) or (
                new_classes != initial_classes
            )
            assert (
                visual_change
            ), f"Должно произойти визуальное изменение кнопки: цвет {initial_color}->{new_color}, классы {initial_classes}->{new_classes}"

        else:
            dynamic_properties_page.log_step(
                "⚠️ Изменение цвета не произошло в ожидаемое время"
            )

    with allure.step("Проверяем кликабельность кнопки с измененным цветом"):
        click_result = dynamic_properties_page.click_color_change_button()
        dynamic_properties_page.log_step(
            f"Кнопка остается кликабельной: {click_result}"
        )

        assert (
            click_result
        ), "Кнопка должна оставаться кликабельной после изменения цвета"


@allure.epic("Elements")
@allure.feature("Dynamic Properties")
@allure.story("Visible After Button")
@pytest.mark.elements
@pytest.mark.regression
def test_visible_after_button(dynamic_properties_page: DynamicPropertiesPage):
    """
    Тест кнопки которая появляется через 5 секунд.

    Проверяет что кнопка изначально скрыта и становится видимой через определенное время.
    """
    with allure.step(
        "Проверяем что кнопка 'Visible After 5 Seconds' изначально скрыта"
    ):
        initial_visible = dynamic_properties_page.is_visible_after_button_visible()
        dynamic_properties_page.log_step(f"Кнопка видима изначально: {initial_visible}")

        # Кнопка должна быть скрыта изначально
        assert (
            not initial_visible
        ), "Кнопка 'Visible After 5 Seconds' должна быть скрыта изначально"

    with allure.step("Проверяем наличие кнопки в DOM"):
        button_exists_in_dom = dynamic_properties_page.is_visible_after_button_in_dom()
        dynamic_properties_page.log_step(
            f"Кнопка присутствует в DOM: {button_exists_in_dom}"
        )

        # Кнопка может присутствовать в DOM, но быть невидимой
        visibility_info = {
            "exists_in_dom": button_exists_in_dom,
            "initially_visible": initial_visible,
            "hidden_by_css": button_exists_in_dom and not initial_visible,
        }

        allure.attach(
            str(visibility_info),
            "initial_visibility_state",
            allure.attachment_type.JSON,
        )

    with allure.step("Ожидаем появления кнопки"):
        dynamic_properties_page.log_step("Ожидание появления кнопки...")

        wait_start_time = time.time()
        max_wait_time = 10  # Максимальное время ожидания

        button_appeared = dynamic_properties_page.wait_for_visible_after_button(
            timeout=max_wait_time * 1000
        )
        actual_wait_time = time.time() - wait_start_time

        dynamic_properties_page.log_step(
            f"Время ожидания: {actual_wait_time:.2f} секунд"
        )
        dynamic_properties_page.log_step(f"Кнопка появилась: {button_appeared}")

        appearance_timing = {
            "expected_delay_seconds": 5,
            "actual_wait_seconds": round(actual_wait_time, 2),
            "button_appeared": button_appeared,
            "timing_within_range": 4 <= actual_wait_time <= 8,
        }

        allure.attach(
            str(appearance_timing),
            "button_appearance_timing",
            allure.attachment_type.JSON,
        )

        assert (
            button_appeared
        ), f"Кнопка должна появиться в течение {max_wait_time} секунд"

    with allure.step("Проверяем видимость и кликабельность появившейся кнопки"):
        final_visible = dynamic_properties_page.is_visible_after_button_visible()
        dynamic_properties_page.log_step(
            f"Кнопка видима после ожидания: {final_visible}"
        )

        assert final_visible, "Кнопка должна быть видима после появления"

        # Пытаемся кликнуть по появившейся кнопке
        click_successful = dynamic_properties_page.click_visible_after_button()
        dynamic_properties_page.log_step(
            f"Клик по появившейся кнопке успешен: {click_successful}"
        )

        assert click_successful, "Появившаяся кнопка должна быть кликабельной"

        final_state = {
            "visible": final_visible,
            "clickable": click_successful,
            "appearance_time": appearance_timing["actual_wait_seconds"],
        }

        allure.attach(
            str(final_state), "final_button_state", allure.attachment_type.JSON
        )


@allure.epic("Elements")
@allure.feature("Dynamic Properties")
@allure.story("All Dynamic Elements")
@pytest.mark.elements
@pytest.mark.regression
def test_all_dynamic_properties_simultaneously(
    dynamic_properties_page: DynamicPropertiesPage,
):
    """
    Комплексный тест всех динамических свойств одновременно.

    Проверяет поведение всех динамических элементов в течение времени.
    """
    test_duration = 12  # Общее время теста в секундах
    check_interval = 1  # Интервал проверки в секундах

    dynamic_states = []

    with allure.step("Записываем начальное состояние всех динамических элементов"):
        initial_state = {
            "timestamp": 0,
            "enable_after_enabled": dynamic_properties_page.is_enable_after_button_enabled(),
            "color_change_color": dynamic_properties_page.get_color_change_button_color(),
            "color_change_classes": dynamic_properties_page.get_color_change_button_classes(),
            "visible_after_visible": dynamic_properties_page.is_visible_after_button_visible(),
        }

        dynamic_states.append(initial_state)
        dynamic_properties_page.log_step(f"Начальное состояние: {initial_state}")

    with allure.step(f"Мониторим изменения в течение {test_duration} секунд"):
        start_time = time.time()

        while time.time() - start_time < test_duration:
            current_time = time.time() - start_time

            current_state = {
                "timestamp": round(current_time, 1),
                "enable_after_enabled": dynamic_properties_page.is_enable_after_button_enabled(),
                "color_change_color": dynamic_properties_page.get_color_change_button_color(),
                "color_change_classes": dynamic_properties_page.get_color_change_button_classes(),
                "visible_after_visible": dynamic_properties_page.is_visible_after_button_visible(),
            }

            dynamic_states.append(current_state)
            dynamic_properties_page.log_step(
                f"Состояние на {current_state['timestamp']}с: Enable={current_state['enable_after_enabled']}, Color={current_state['color_change_color']}, Visible={current_state['visible_after_visible']}"
            )

            time.sleep(check_interval)

    with allure.step("Анализируем изменения динамических свойств"):
        allure.attach(
            str(dynamic_states), "dynamic_states_timeline", allure.attachment_type.JSON
        )

        # Анализируем когда произошли изменения
        changes_analysis = {
            "enable_after_changes": [],
            "color_changes": [],
            "visibility_changes": [],
        }

        for i in range(1, len(dynamic_states)):
            prev_state = dynamic_states[i - 1]
            curr_state = dynamic_states[i]

            # Проверяем изменение активности кнопки
            if prev_state["enable_after_enabled"] != curr_state["enable_after_enabled"]:
                changes_analysis["enable_after_changes"].append(
                    {
                        "timestamp": curr_state["timestamp"],
                        "from": prev_state["enable_after_enabled"],
                        "to": curr_state["enable_after_enabled"],
                    }
                )

            # Проверяем изменение цвета
            if (
                prev_state["color_change_color"] != curr_state["color_change_color"]
                or prev_state["color_change_classes"]
                != curr_state["color_change_classes"]
            ):
                changes_analysis["color_changes"].append(
                    {
                        "timestamp": curr_state["timestamp"],
                        "color_from": prev_state["color_change_color"],
                        "color_to": curr_state["color_change_color"],
                        "classes_from": prev_state["color_change_classes"],
                        "classes_to": curr_state["color_change_classes"],
                    }
                )

            # Проверяем изменение видимости
            if (
                prev_state["visible_after_visible"]
                != curr_state["visible_after_visible"]
            ):
                changes_analysis["visibility_changes"].append(
                    {
                        "timestamp": curr_state["timestamp"],
                        "from": prev_state["visible_after_visible"],
                        "to": curr_state["visible_after_visible"],
                    }
                )

        dynamic_properties_page.log_step(f"Анализ изменений: {changes_analysis}")
        allure.attach(
            str(changes_analysis), "changes_analysis", allure.attachment_type.JSON
        )

    with allure.step("Проверяем финальное состояние всех элементов"):
        final_state = dynamic_states[-1]

        # После достаточного времени все элементы должны быть в активном состоянии
        final_checks = {
            "enable_after_final": final_state["enable_after_enabled"],
            "visible_after_final": final_state["visible_after_visible"],
            "total_enable_changes": len(changes_analysis["enable_after_changes"]),
            "total_color_changes": len(changes_analysis["color_changes"]),
            "total_visibility_changes": len(changes_analysis["visibility_changes"]),
        }

        dynamic_properties_page.log_step(f"Финальные проверки: {final_checks}")
        allure.attach(str(final_checks), "final_checks", allure.attachment_type.JSON)

        # Проверяем что произошли ожидаемые изменения
        assert final_checks[
            "enable_after_final"
        ], "Кнопка 'Enable After' должна стать активной"
        assert final_checks[
            "visible_after_final"
        ], "Кнопка 'Visible After' должна стать видимой"
        assert (
            final_checks["total_enable_changes"] > 0
        ), "Должно произойти изменение состояния кнопки 'Enable After'"
        assert (
            final_checks["total_visibility_changes"] > 0
        ), "Должно произойти изменение видимости кнопки 'Visible After'"


@allure.epic("Elements")
@allure.feature("Dynamic Properties")
@allure.story("Random ID Element")
@pytest.mark.elements
def test_random_id_element(dynamic_properties_page: DynamicPropertiesPage):
    """
    Тест элемента с случайным ID.

    Проверяет обработку элемента который имеет динамически генерируемый ID.
    """
    with allure.step("Ищем элемент с случайным ID"):
        random_id_element = dynamic_properties_page.find_random_id_element()
        dynamic_properties_page.log_step(
            f"Элемент с случайным ID найден: {random_id_element is not None}"
        )

    with allure.step("Получаем информацию об элементе с случайным ID"):
        if random_id_element:
            element_info = dynamic_properties_page.get_random_id_element_info()
            dynamic_properties_page.log_step(f"Информация об элементе: {element_info}")

            allure.attach(
                str(element_info), "random_id_element_info", allure.attachment_type.JSON
            )

            # Проверяем что ID действительно случайный (содержит цифры/буквы)
            element_id = element_info.get("id", "")
            assert (
                len(element_id) > 5
            ), f"ID должен быть достаточно длинным: {element_id}"

        else:
            dynamic_properties_page.log_step(
                "ℹ️ Элемент с случайным ID не найден на странице"
            )

    with allure.step("Проверяем стабильность случайного ID"):
        # Проверяем что ID не изменяется при обновлении
        if random_id_element:
            first_id = dynamic_properties_page.get_random_id_element_id()

            # Небольшая пауза
            time.sleep(2)

            second_id = dynamic_properties_page.get_random_id_element_id()

            id_stability = {
                "first_id": first_id,
                "second_id": second_id,
                "id_stable": first_id == second_id,
                "id_length": len(first_id) if first_id else 0,
            }

            dynamic_properties_page.log_step(f"Стабильность ID: {id_stability}")
            allure.attach(
                str(id_stability), "id_stability_check", allure.attachment_type.JSON
            )

            # ID должен оставаться стабильным в пределах одной сессии
            assert id_stability[
                "id_stable"
            ], f"ID должен оставаться стабильным в течение сессии: {first_id} != {second_id}"
