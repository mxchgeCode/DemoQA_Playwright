"""
Тесты для страницы Buttons.
Проверяет функциональность различных типов кликов по кнопкам:
- Двойной клик (Double Click)
- Правый клик (Right Click)
- Обычный клик (Click Me)
- Проверка сообщений после кликов
"""

import pytest
import allure
from pages.elements.buttons_page import ButtonsPage


@allure.epic("Elements")
@allure.feature("Buttons")
@allure.story("Double Click")
@pytest.mark.elements
@pytest.mark.smoke
def test_double_click_button(buttons_page: ButtonsPage):
    """
    Тест двойного клика по кнопке.

    Шаги:
    1. Выполнить двойной клик по соответствующей кнопке
    2. Проверить что появилось сообщение о двойном клике
    """
    with allure.step("Выполняем двойной клик по кнопке"):
        buttons_page.log_step("Выполнение двойного клика по кнопке 'Double Click Me'")
        buttons_page.double_click_button()

    with allure.step("Проверяем сообщение о двойном клике"):
        double_click_message = buttons_page.get_double_click_message()
        buttons_page.log_step(f"Сообщение после двойного клика: {double_click_message}")

        allure.attach(
            double_click_message, "double_click_message", allure.attachment_type.TEXT
        )

        expected_text = "You have done a double click"
        assert (
            expected_text in double_click_message
        ), f"Ожидается текст '{expected_text}', получено '{double_click_message}'"

        buttons_page.log_step("✅ Двойной клик обработан корректно")


@allure.epic("Elements")
@allure.feature("Buttons")
@allure.story("Right Click")
@pytest.mark.elements
@pytest.mark.smoke
def test_right_click_button(buttons_page: ButtonsPage):
    """
    Тест правого клика по кнопке.

    Проверяет функциональность контекстного меню/правого клика.
    """
    with allure.step("Выполняем правый клик по кнопке"):
        buttons_page.log_step("Выполнение правого клика по кнопке 'Right Click Me'")
        buttons_page.right_click_button()

    with allure.step("Проверяем сообщение о правом клике"):
        right_click_message = buttons_page.get_right_click_message()
        buttons_page.log_step(f"Сообщение после правого клика: {right_click_message}")

        allure.attach(
            right_click_message, "right_click_message", allure.attachment_type.TEXT
        )

        expected_text = "You have done a right click"
        assert (
            expected_text in right_click_message
        ), f"Ожидается текст '{expected_text}', получено '{right_click_message}'"

        buttons_page.log_step("✅ Правый клик обработан корректно")


@allure.epic("Elements")
@allure.feature("Buttons")
@allure.story("Regular Click")
@pytest.mark.elements
@pytest.mark.smoke
def test_regular_click_button(buttons_page: ButtonsPage):
    """
    Тест обычного (левого) клика по кнопке.

    Проверяет стандартную функциональность клика.
    """
    with allure.step("Выполняем обычный клик по кнопке"):
        buttons_page.log_step("Выполнение обычного клика по кнопке 'Click Me'")
        buttons_page.click_me_button()

    with allure.step("Проверяем сообщение об обычном клике"):
        click_message = buttons_page.get_click_message()
        buttons_page.log_step(f"Сообщение после обычного клика: {click_message}")

        allure.attach(click_message, "click_message", allure.attachment_type.TEXT)

        expected_text = "You have done a dynamic click"
        assert (
            expected_text in click_message
        ), f"Ожидается текст '{expected_text}', получено '{click_message}'"

        buttons_page.log_step("✅ Обычный клик обработан корректно")


@allure.epic("Elements")
@allure.feature("Buttons")
@allure.story("All Click Types")
@pytest.mark.elements
@pytest.mark.regression
def test_all_button_click_types(buttons_page: ButtonsPage):
    """
    Комплексный тест всех типов кликов по кнопкам.

    Проверяет последовательное выполнение всех видов кликов и их сообщений.
    """
    click_results = {}

    with allure.step("Тестируем все типы кликов последовательно"):

        # Двойной клик
        with allure.step("1. Тестируем двойной клик"):
            buttons_page.log_step("Этап 1: Двойной клик")
            buttons_page.double_click_button()
            double_msg = buttons_page.get_double_click_message()
            click_results["double_click"] = {
                "message": double_msg,
                "success": "double click" in double_msg.lower(),
            }
            buttons_page.log_step(f"Двойной клик: {click_results['double_click']}")

        # Правый клик
        with allure.step("2. Тестируем правый клик"):
            buttons_page.log_step("Этап 2: Правый клик")
            buttons_page.right_click_button()
            right_msg = buttons_page.get_right_click_message()
            click_results["right_click"] = {
                "message": right_msg,
                "success": "right click" in right_msg.lower(),
            }
            buttons_page.log_step(f"Правый клик: {click_results['right_click']}")

        # Обычный клик
        with allure.step("3. Тестируем обычный клик"):
            buttons_page.log_step("Этап 3: Обычный клик")
            buttons_page.click_me_button()
            click_msg = buttons_page.get_click_message()
            click_results["regular_click"] = {
                "message": click_msg,
                "success": "dynamic click" in click_msg.lower(),
            }
            buttons_page.log_step(f"Обычный клик: {click_results['regular_click']}")

    with allure.step("Анализируем результаты всех кликов"):
        allure.attach(
            str(click_results), "all_click_results", allure.attachment_type.JSON
        )

        successful_clicks = sum(
            1 for result in click_results.values() if result["success"]
        )
        total_clicks = len(click_results)

        summary = {
            "total_click_types": total_clicks,
            "successful_clicks": successful_clicks,
            "success_rate": successful_clicks / total_clicks,
            "all_clicks_successful": successful_clicks == total_clicks,
        }

        buttons_page.log_step(f"Итоги тестирования кликов: {summary}")
        allure.attach(str(summary), "clicks_summary", allure.attachment_type.JSON)

        assert summary[
            "all_clicks_successful"
        ], f"Все типы кликов должны работать корректно. Успешно: {successful_clicks}/{total_clicks}"


@allure.epic("Elements")
@allure.feature("Buttons")
@allure.story("Button States")
@pytest.mark.elements
def test_button_states_and_visibility(buttons_page: ButtonsPage):
    """
    Тест состояний и видимости кнопок.

    Проверяет что все кнопки видимы и кликабельны.
    """
    with allure.step("Проверяем видимость всех кнопок"):
        buttons_visibility = {
            "double_click_button": buttons_page.is_double_click_button_visible(),
            "right_click_button": buttons_page.is_right_click_button_visible(),
            "click_me_button": buttons_page.is_click_me_button_visible(),
        }

        buttons_page.log_step(f"Видимость кнопок: {buttons_visibility}")
        allure.attach(
            str(buttons_visibility), "buttons_visibility", allure.attachment_type.JSON
        )

        for button_name, is_visible in buttons_visibility.items():
            assert is_visible, f"Кнопка '{button_name}' должна быть видима"

    with allure.step("Проверяем доступность кнопок для клика"):
        buttons_enabled = {
            "double_click_button": buttons_page.is_double_click_button_enabled(),
            "right_click_button": buttons_page.is_right_click_button_enabled(),
            "click_me_button": buttons_page.is_click_me_button_enabled(),
        }

        buttons_page.log_step(f"Доступность кнопок: {buttons_enabled}")
        allure.attach(
            str(buttons_enabled), "buttons_enabled", allure.attachment_type.JSON
        )

        for button_name, is_enabled in buttons_enabled.items():
            assert is_enabled, f"Кнопка '{button_name}' должна быть доступна для клика"

    with allure.step("Проверяем текст на кнопках"):
        buttons_text = {
            "double_click_button": buttons_page.get_double_click_button_text(),
            "right_click_button": buttons_page.get_right_click_button_text(),
            "click_me_button": buttons_page.get_click_me_button_text(),
        }

        buttons_page.log_step(f"Текст кнопок: {buttons_text}")
        allure.attach(str(buttons_text), "buttons_text", allure.attachment_type.JSON)

        expected_texts = {
            "double_click_button": "Double Click Me",
            "right_click_button": "Right Click Me",
            "click_me_button": "Click Me",
        }

        for button_name, actual_text in buttons_text.items():
            expected_text = expected_texts[button_name]
            assert (
                expected_text.lower() in actual_text.lower()
            ), f"Кнопка '{button_name}' должна содержать текст '{expected_text}'"
