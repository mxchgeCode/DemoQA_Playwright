"""
Тесты для страницы Modal Dialogs.
Проверяет функциональность модальных окон:
- Открытие и закрытие модальных окон
- Проверка содержимого модальных окон
- Взаимодействие с элементами в модальных окнах
- Валидация размеров модальных окон
"""

import pytest
import allure
from pages.alerts.modal_page import ModalPage


@allure.epic("Alerts, Frame & Windows")
@allure.feature("Modal Dialogs")
@allure.story("Small Modal Dialog")
@pytest.mark.alerts
@pytest.mark.smoke
def test_small_modal_functionality(modal_page: ModalPage):
    """
    Тест функциональности малого модального окна.

    Проверяет открытие, содержимое и закрытие малого модального окна.
    """
    with allure.step("Открываем малое модальное окно"):
        modal_page.log_step("Клик по кнопке открытия малого модального окна")
        modal_page.open_small_modal()

        # Проверяем что модальное окно открылось
        modal_visible = modal_page.is_small_modal_visible()
        modal_page.log_step(f"Малое модальное окно видимо: {modal_visible}")

        assert modal_visible, "Малое модальное окно должно быть видимым после открытия"

    with allure.step("Проверяем заголовок малого модального окна"):
        modal_title = modal_page.get_modal_title()
        modal_page.log_step(f"Заголовок модального окна: '{modal_title}'")

        assert (
            modal_title == "Small Modal"
        ), f"Заголовок должен быть 'Small Modal', получен: '{modal_title}'"

    with allure.step("Проверяем содержимое малого модального окна"):
        modal_body = modal_page.get_modal_body()
        modal_page.log_step(f"Содержимое модального окна: '{modal_body[:100]}...'")

        # Проверяем что содержимое не пустое
        assert len(modal_body) > 0, "Содержимое модального окна не должно быть пустым"

        # Проверяем наличие ключевых элементов
        has_close_button = modal_page.has_small_modal_close_button()
        modal_page.log_step(f"Кнопка закрытия присутствует: {has_close_button}")

        assert has_close_button, "Модальное окно должно содержать кнопку закрытия"

    with allure.step("Получаем размеры малого модального окна"):
        modal_size = modal_page.get_small_modal_size()
        modal_page.log_step(f"Размеры малого модального окна: {modal_size}")

        # Проверяем что размеры разумные для малого окна
        assert (
            modal_size["width"] > 0 and modal_size["height"] > 0
        ), "Модальное окно должно иметь положительные размеры"
        assert (
            modal_size["width"] < 800
        ), "Малое модальное окно должно быть относительно небольшим по ширине"

        allure.attach(
            str(modal_size), "small_modal_dimensions", allure.attachment_type.JSON
        )

    with allure.step("Закрываем малое модальное окно"):
        modal_page.log_step("Клик по кнопке закрытия малого модального окна")
        modal_page.close_small_modal()

        # Проверяем что модальное окно закрылось
        modal_page.page.wait_for_timeout(1000)  # Ждем анимацию закрытия
        modal_closed = not modal_page.is_small_modal_visible()
        modal_page.log_step(f"Малое модальное окно закрыто: {modal_closed}")

        assert (
            modal_closed
        ), "Малое модальное окно должно быть закрыто после клика по кнопке закрытия"


@allure.epic("Alerts, Frame & Windows")
@allure.feature("Modal Dialogs")
@allure.story("Large Modal Dialog")
@pytest.mark.alerts
@pytest.mark.smoke
def test_large_modal_functionality(modal_page: ModalPage):
    """
    Тест функциональности большого модального окна.

    Проверяет открытие, содержимое и закрытие большого модального окна.
    """
    with allure.step("Открываем большое модальное окно"):
        modal_page.log_step("Клик по кнопке открытия большого модального окна")
        modal_page.open_large_modal()

        # Проверяем что модальное окно открылось
        modal_visible = modal_page.is_large_modal_visible()
        modal_page.log_step(f"Большое модальное окно видимо: {modal_visible}")

        assert (
            modal_visible
        ), "Большое модальное окно должно быть видимым после открытия"

    with allure.step("Проверяем заголовок большого модального окна"):
        modal_title = modal_page.get_modal_title()
        modal_page.log_step(f"Заголовок модального окна: '{modal_title}'")

        assert (
            modal_title == "Large Modal"
        ), f"Заголовок должен быть 'Large Modal', получен: '{modal_title}'"

    with allure.step("Проверяем содержимое большого модального окна"):
        modal_body = modal_page.get_modal_body()
        modal_page.log_step(
            f"Длина содержимого модального окна: {len(modal_body)} символов"
        )

        # Проверяем что содержимое достаточно объемное для большого окна
        assert (
            len(modal_body) > 20
        ), f"Содержимое большого модального окна должно быть объемным, получено: {len(modal_body)} символов"

        # Проверяем наличие ключевых элементов
        has_close_button = modal_page.has_large_modal_close_button()
        modal_page.log_step(f"Кнопка закрытия присутствует: {has_close_button}")

        assert has_close_button, "Модальное окно должно содержать кнопку закрытия"

        # Сохраняем содержимое для анализа
        allure.attach(
            modal_body[:500], "large_modal_content_preview", allure.attachment_type.TEXT
        )

    with allure.step("Получаем размеры большого модального окна"):
        modal_size = modal_page.get_large_modal_size()
        modal_page.log_step(f"Размеры большого модального окна: {modal_size}")

        # Проверяем что размеры подходят для большого окна
        assert (
            modal_size["width"] > 0 and modal_size["height"] > 0
        ), "Модальное окно должно иметь положительные размеры"
        assert (
            modal_size["width"] >= 600
        ), "Большое модальное окно должно быть достаточно широким"

        allure.attach(
            str(modal_size), "large_modal_dimensions", allure.attachment_type.JSON
        )

    with allure.step("Закрываем большое модальное окно"):
        modal_page.log_step("Клик по кнопке закрытия большого модального окна")
        modal_page.close_large_modal()

        # Проверяем что модальное окно закрылось
        modal_page.page.wait_for_timeout(1000)  # Ждем анимацию закрытия
        modal_closed = not modal_page.is_large_modal_visible()
        modal_page.log_step(f"Большое модальное окно закрыто: {modal_closed}")

        assert (
            modal_closed
        ), "Большое модальное окно должно быть закрыто после клика по кнопке закрытия"


@allure.epic("Alerts, Frame & Windows")
@allure.feature("Modal Dialogs")
@allure.story("Modal Dialogs Comparison")
@pytest.mark.alerts
@pytest.mark.regression
def test_modal_sizes_comparison(modal_page: ModalPage):
    """
    Тест сравнения размеров модальных окон.

    Сравнивает размеры малого и большого модальных окон.
    """
    small_modal_info = {}
    large_modal_info = {}

    with allure.step("Измеряем параметры малого модального окна"):
        modal_page.log_step("Открытие и измерение малого модального окна")
        modal_page.open_small_modal()
        modal_page.page.wait_for_timeout(500)

        small_modal_info = {
            "visible": modal_page.is_small_modal_visible(),
            "size": modal_page.get_small_modal_size(),
            "title": modal_page.get_modal_title(),
            "body_length": len(modal_page.get_modal_body()),
        }

        modal_page.log_step(f"Параметры малого окна: {small_modal_info}")
        modal_page.close_small_modal()
        modal_page.page.wait_for_timeout(500)

    with allure.step("Измеряем параметры большого модального окна"):
        modal_page.log_step("Открытие и измерение большого модального окна")
        modal_page.open_large_modal()
        modal_page.page.wait_for_timeout(500)

        large_modal_info = {
            "visible": modal_page.is_large_modal_visible(),
            "size": modal_page.get_large_modal_size(),
            "title": modal_page.get_modal_title(),
            "body_length": len(modal_page.get_modal_body()),
        }

        modal_page.log_step(f"Параметры большого окна: {large_modal_info}")
        modal_page.close_large_modal()
        modal_page.page.wait_for_timeout(500)

    with allure.step("Сравниваем размеры модальных окон"):
        comparison = {
            "small_modal": small_modal_info,
            "large_modal": large_modal_info,
            "width_difference": large_modal_info["size"]["width"]
            - small_modal_info["size"]["width"],
            "height_difference": large_modal_info["size"]["height"]
            - small_modal_info["size"]["height"],
            "content_difference": large_modal_info["body_length"]
            - small_modal_info["body_length"],
            "large_is_wider": large_modal_info["size"]["width"]
            > small_modal_info["size"]["width"],
            "large_has_more_content": large_modal_info["body_length"]
            > small_modal_info["body_length"],
        }

        modal_page.log_step(f"Сравнение модальных окон: {comparison}")
        allure.attach(
            str(comparison), "modal_sizes_comparison", allure.attachment_type.JSON
        )

        # Проверяем логичность размеров
        assert comparison[
            "large_is_wider"
        ], "Большое модальное окно должно быть шире малого"
        assert comparison[
            "large_has_more_content"
        ], "Большое модальное окно должно содержать больше контента"

        modal_page.log_step("✅ Размеры модальных окон соответствуют ожиданиям")


@allure.epic("Alerts, Frame & Windows")
@allure.feature("Modal Dialogs")
@allure.story("Modal Dialog Overlay")
@pytest.mark.alerts
def test_modal_overlay_interaction(modal_page: ModalPage):
    """
    Тест взаимодействия с overlay модального окна.

    Проверяет поведение при клике на фон модального окна.
    """
    with allure.step("Открываем модальное окно для тестирования overlay"):
        modal_page.log_step("Открытие малого модального окна для тестирования overlay")
        modal_page.open_small_modal()

        initial_modal_state = modal_page.is_small_modal_visible()
        modal_page.log_step(
            f"Начальное состояние модального окна: {initial_modal_state}"
        )

        assert initial_modal_state, "Модальное окно должно быть открыто"

    with allure.step("Проверяем наличие overlay"):
        has_overlay = modal_page.has_modal_overlay()
        modal_page.log_step(f"Overlay присутствует: {has_overlay}")

        if has_overlay:
            overlay_visible = modal_page.is_modal_overlay_visible()
            modal_page.log_step(f"Overlay видимый: {overlay_visible}")

        overlay_info = {
            "has_overlay": has_overlay,
            "overlay_visible": overlay_visible if has_overlay else False,
        }

        allure.attach(
            str(overlay_info), "modal_overlay_info", allure.attachment_type.JSON
        )

    with allure.step("Тестируем клик по overlay"):
        if has_overlay:
            modal_page.log_step("Клик по overlay модального окна")
            overlay_click_result = modal_page.click_modal_overlay()
            modal_page.page.wait_for_timeout(1000)

            modal_state_after_overlay_click = modal_page.is_small_modal_visible()
            modal_page.log_step(
                f"Состояние модального окна после клика по overlay: {modal_state_after_overlay_click}"
            )

            overlay_test_result = {
                "overlay_click_attempted": overlay_click_result,
                "modal_closed_by_overlay": not modal_state_after_overlay_click,
                "overlay_behavior": (
                    "closes_modal"
                    if not modal_state_after_overlay_click
                    else "keeps_modal_open"
                ),
            }

            modal_page.log_step(f"Результат теста overlay: {overlay_test_result}")
            allure.attach(
                str(overlay_test_result),
                "overlay_click_test",
                allure.attachment_type.JSON,
            )

        else:
            modal_page.log_step("Overlay не найден, пропускаем тест клика")

    with allure.step("Закрываем модальное окно если оно все еще открыто"):
        if modal_page.is_small_modal_visible():
            modal_page.log_step("Закрытие модального окна через кнопку")
            modal_page.close_small_modal()

        final_modal_state = modal_page.is_small_modal_visible()
        modal_page.log_step(f"Финальное состояние модального окна: {final_modal_state}")


@allure.epic("Alerts, Frame & Windows")
@allure.feature("Modal Dialogs")
@allure.story("Modal Dialog Accessibility")
@pytest.mark.alerts
def test_modal_accessibility_features(modal_page: ModalPage):
    """
    Тест функций доступности модальных окон.

    Проверяет ARIA атрибуты, фокус и клавиатурную навигацию.
    """
    with allure.step("Открываем модальное окно для тестирования доступности"):
        modal_page.log_step("Открытие малого модального окна для проверки доступности")
        modal_page.open_small_modal()

        assert modal_page.is_small_modal_visible(), "Модальное окно должно быть открыто"

    with allure.step("Проверяем ARIA атрибуты модального окна"):
        aria_attributes = modal_page.get_modal_aria_attributes()
        modal_page.log_step(f"ARIA атрибуты модального окна: {aria_attributes}")

        # Проверяем ключевые ARIA атрибуты
        has_aria_modal = "aria-modal" in aria_attributes
        has_role_dialog = aria_attributes.get("role") == "dialog"
        has_aria_labelledby = "aria-labelledby" in aria_attributes

        accessibility_checks = {
            "aria_attributes": aria_attributes,
            "has_aria_modal": has_aria_modal,
            "has_role_dialog": has_role_dialog,
            "has_aria_labelledby": has_aria_labelledby,
            "accessibility_compliant": has_aria_modal or has_role_dialog,
        }

        modal_page.log_step(f"Проверки доступности: {accessibility_checks}")
        allure.attach(
            str(accessibility_checks),
            "modal_accessibility_checks",
            allure.attachment_type.JSON,
        )

    with allure.step("Проверяем управление фокусом"):
        # Проверяем куда устанавливается фокус при открытии модального окна
        focused_element = modal_page.get_focused_element_in_modal()
        modal_page.log_step(f"Элемент с фокусом в модальном окне: {focused_element}")

        # Проверяем можно ли закрыть модальное окно клавишей Escape
        escape_close_available = modal_page.can_close_modal_with_escape()
        modal_page.log_step(f"Закрытие по Escape доступно: {escape_close_available}")

        if escape_close_available:
            modal_page.log_step("Попытка закрытия модального окна клавишей Escape")
            escape_close_result = modal_page.close_modal_with_escape()
            modal_page.page.wait_for_timeout(500)

            modal_closed_by_escape = not modal_page.is_small_modal_visible()
            modal_page.log_step(
                f"Модальное окно закрыто по Escape: {modal_closed_by_escape}"
            )

            focus_management = {
                "focused_element": focused_element,
                "escape_close_available": escape_close_available,
                "escape_close_successful": modal_closed_by_escape,
                "focus_management_good": focused_element is not None,
            }

        else:
            focus_management = {
                "focused_element": focused_element,
                "escape_close_available": False,
                "focus_management_good": focused_element is not None,
            }

            # Закрываем модальное окно обычным способом
            modal_page.close_small_modal()

        modal_page.log_step(f"Управление фокусом: {focus_management}")
        allure.attach(
            str(focus_management), "modal_focus_management", allure.attachment_type.JSON
        )
