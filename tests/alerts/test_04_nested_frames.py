"""
Тесты для страницы Browser Windows - Nested Frames.
Проверяет функциональность работы с вложенными фреймами:
- Навигация по иерархии фреймов
- Получение контента из родительских и дочерних фреймов
- Переключение между уровнями вложенности
"""

import pytest
import allure
from pages.alerts.browser_windows_page import BrowserWindowsPage


@allure.epic("Alerts, Frame & Windows")
@allure.feature("Nested Frames")
@allure.story("Parent Frame Access")
@pytest.mark.alerts
@pytest.mark.smoke
def test_access_parent_frame(browser_windows_page: BrowserWindowsPage):
    """
    Тест доступа к родительскому фрейму.

    Шаги:
    1. Переключиться в родительский фрейм
    2. Получить текст из родительского фрейма
    3. Проверить содержимое
    """
    with allure.step("Открываем страницу Nested Frames"):
        browser_windows_page.log_step("Переход на страницу вложенных фреймов")

    with allure.step("Переключаемся в родительский фрейм"):
        browser_windows_page.log_step("Поиск и переключение в родительский iframe")
        parent_text = browser_windows_page.get_parent_frame_text()
        browser_windows_page.log_step(
            f"Получен текст родительского фрейма: {parent_text}"
        )

        allure.attach(parent_text, "parent_frame_content", allure.attachment_type.TEXT)

    with allure.step("Проверяем содержимое родительского фрейма"):
        expected_text = "Parent frame"
        assert (
            expected_text in parent_text
        ), f"Ожидается '{expected_text}' в тексте родительского фрейма, получено '{parent_text}'"

        browser_windows_page.log_step(f"✅ Содержимое родительского фрейма корректно")


@allure.epic("Alerts, Frame & Windows")
@allure.feature("Nested Frames")
@allure.story("Child Frame Access")
@pytest.mark.alerts
@pytest.mark.smoke
def test_access_child_frame(browser_windows_page: BrowserWindowsPage):
    """
    Тест доступа к дочернему фрейму внутри родительского.

    Проверяет двухуровневую навигацию: основная страница -> родительский фрейм -> дочерний фрейм.
    """
    with allure.step("Переключаемся в родительский фрейм"):
        browser_windows_page.log_step(
            "Первый уровень: переключение в родительский фрейм"
        )
        browser_windows_page.switch_to_parent_frame()

    with allure.step("Из родительского фрейма переключаемся в дочерний"):
        browser_windows_page.log_step("Второй уровень: переключение в дочерний фрейм")
        child_text = browser_windows_page.get_child_frame_text()
        browser_windows_page.log_step(f"Получен текст дочернего фрейма: {child_text}")

        allure.attach(child_text, "child_frame_content", allure.attachment_type.TEXT)

    with allure.step("Проверяем содержимое дочернего фрейма"):
        expected_text = "Child Iframe"
        assert (
            expected_text in child_text
        ), f"Ожидается '{expected_text}' в дочернем фрейме, получено '{child_text}'"

        browser_windows_page.log_step(f"✅ Содержимое дочернего фрейма корректно")


@allure.epic("Alerts, Frame & Windows")
@allure.feature("Nested Frames")
@allure.story("Frame Hierarchy Navigation")
@pytest.mark.alerts
@pytest.mark.regression
def test_nested_frames_navigation_hierarchy(browser_windows_page: BrowserWindowsPage):
    """
    Тест полной навигации по иерархии вложенных фреймов.

    Проверяет переходы: основная -> родительский -> дочерний -> родительский -> основная.
    """
    navigation_log = []

    with allure.step("Начинаем с основного контента"):
        browser_windows_page.log_step("🏠 Исходное положение: основной контент")
        main_visible = browser_windows_page.is_main_content_visible()
        navigation_log.append(f"Main content visible: {main_visible}")

        assert main_visible, "Должны начинать с основного контента"

    with allure.step("Переходим в родительский фрейм"):
        browser_windows_page.log_step("📄 Переход: основной -> родительский фрейм")
        browser_windows_page.switch_to_parent_frame()

        parent_text = browser_windows_page.get_current_frame_content()
        navigation_log.append(f"Parent frame content: {parent_text[:50]}...")
        browser_windows_page.log_step(f"Контент родительского фрейма: {parent_text}")

        assert "Parent" in parent_text, "Должны быть в родительском фрейме"

    with allure.step("Переходим в дочерний фрейм"):
        browser_windows_page.log_step("👶 Переход: родительский -> дочерний фрейм")
        browser_windows_page.switch_to_child_frame()

        child_text = browser_windows_page.get_current_frame_content()
        navigation_log.append(f"Child frame content: {child_text[:50]}...")
        browser_windows_page.log_step(f"Контент дочернего фрейма: {child_text}")

        assert "Child" in child_text, "Должны быть в дочернем фрейме"

    with allure.step("Возвращаемся в родительский фрейм"):
        browser_windows_page.log_step("⬆️ Переход: дочерний -> родительский фрейм")
        browser_windows_page.switch_to_parent_context()

        parent_text_return = browser_windows_page.get_current_frame_content()
        navigation_log.append(f"Back to parent: {parent_text_return[:50]}...")
        browser_windows_page.log_step(f"Возврат к родительскому: {parent_text_return}")

        assert "Parent" in parent_text_return, "Должны вернуться в родительский фрейм"

    with allure.step("Возвращаемся в основной контент"):
        browser_windows_page.log_step("🏠 Переход: родительский -> основной контент")
        browser_windows_page.switch_to_default_content()

        main_visible_return = browser_windows_page.is_main_content_visible()
        navigation_log.append(f"Back to main: {main_visible_return}")
        browser_windows_page.log_step(
            f"Возврат к основному контенту: {main_visible_return}"
        )

        assert main_visible_return, "Должны вернуться в основной контент"

    with allure.step("Финальная проверка навигации"):
        allure.attach(
            "\n".join(navigation_log), "navigation_log", allure.attachment_type.TEXT
        )

        # Проверяем что прошли полный цикл
        expected_steps = 5
        actual_steps = len(navigation_log)
        browser_windows_page.log_step(f"Выполнено навигационных шагов: {actual_steps}")

        assert (
            actual_steps >= expected_steps
        ), f"Должно быть выполнено минимум {expected_steps} шагов, выполнено {actual_steps}"


@allure.epic("Alerts, Frame & Windows")
@allure.feature("Nested Frames")
@allure.story("Frame Context Isolation")
@pytest.mark.alerts
def test_nested_frames_context_isolation(browser_windows_page: BrowserWindowsPage):
    """
    Тест изоляции контекста между вложенными фреймами.

    Проверяет что элементы доступны только в своем контексте фрейма.
    """
    isolation_results = {}

    with allure.step("Проверяем изоляцию из основного контекста"):
        browser_windows_page.log_step(
            "🧪 Тест изоляции: поиск элементов фреймов из основного контекста"
        )

        parent_accessible = browser_windows_page.can_access_parent_frame_elements()
        child_accessible = browser_windows_page.can_access_child_frame_elements()

        isolation_results["from_main"] = {
            "parent_accessible": parent_accessible,
            "child_accessible": child_accessible,
        }

        browser_windows_page.log_step(
            f"Из основного контекста - родительский: {parent_accessible}, дочерний: {child_accessible}"
        )

        assert (
            not parent_accessible
        ), "Элементы родительского фрейма НЕ должны быть доступны из основного контекста"
        assert (
            not child_accessible
        ), "Элементы дочернего фрейма НЕ должны быть доступны из основного контекста"

    with allure.step("Проверяем изоляцию из родительского фрейма"):
        browser_windows_page.switch_to_parent_frame()
        browser_windows_page.log_step(
            "🧪 Тест изоляции: поиск элементов из родительского фрейма"
        )

        main_accessible = browser_windows_page.can_access_main_content_elements()
        child_accessible_from_parent = (
            browser_windows_page.can_access_child_frame_elements()
        )

        isolation_results["from_parent"] = {
            "main_accessible": main_accessible,
            "child_accessible": child_accessible_from_parent,
        }

        browser_windows_page.log_step(
            f"Из родительского фрейма - основной: {main_accessible}, дочерний: {child_accessible_from_parent}"
        )

        assert (
            not main_accessible
        ), "Элементы основного контента НЕ должны быть доступны из родительского фрейма"
        # Дочерний может быть доступен из родительского (зависит от реализации)

    with allure.step("Проверяем изоляцию из дочернего фрейма"):
        browser_windows_page.switch_to_child_frame()
        browser_windows_page.log_step(
            "🧪 Тест изоляции: поиск элементов из дочернего фрейма"
        )

        main_accessible_from_child = (
            browser_windows_page.can_access_main_content_elements()
        )
        parent_accessible_from_child = (
            browser_windows_page.can_access_parent_frame_elements()
        )

        isolation_results["from_child"] = {
            "main_accessible": main_accessible_from_child,
            "parent_accessible": parent_accessible_from_child,
        }

        browser_windows_page.log_step(
            f"Из дочернего фрейма - основной: {main_accessible_from_child}, родительский: {parent_accessible_from_child}"
        )

        assert (
            not main_accessible_from_child
        ), "Элементы основного контента НЕ должны быть доступны из дочернего фрейма"
        assert (
            not parent_accessible_from_child
        ), "Элементы родительского фрейма НЕ должны быть доступны напрямую из дочернего"

    with allure.step("Возвращаемся и сохраняем результаты изоляции"):
        browser_windows_page.switch_to_default_content()

        allure.attach(
            str(isolation_results),
            "frame_isolation_results",
            allure.attachment_type.JSON,
        )
        browser_windows_page.log_step(f"✅ Все проверки изоляции пройдены успешно")
