"""
Тесты для страницы Browser Windows - Frames.
Проверяет функциональность работы с фреймами (iframe):
- Переключение между фреймами
- Получение контента из фреймов
- Проверка изоляции фреймов
"""

import pytest
import allure
from pages.alerts.browser_windows_page import BrowserWindowsPage


@allure.epic("Alerts, Frame & Windows")
@allure.feature("Frames")
@allure.story("Basic Frame Interaction")
@pytest.mark.alerts
@pytest.mark.smoke
def test_switch_to_frame_and_get_text(browser_windows_page: BrowserWindowsPage):
    """
    Тест переключения во фрейм и получения текста из него.

    Шаги:
    1. Открыть страницу Frames
    2. Переключиться в первый фрейм
    3. Получить текст из фрейма
    4. Проверить содержимое фрейма
    """
    with allure.step("Открываем страницу Frames"):
        browser_windows_page.log_step("Переходим на страницу Frames")

    with allure.step("Переключаемся в первый фрейм"):
        browser_windows_page.log_step("Поиск и переключение в iframe")
        frame_text = browser_windows_page.get_text_from_frame()
        browser_windows_page.log_step(f"Получен текст из фрейма: {frame_text}")

        allure.attach(frame_text, "frame_content", allure.attachment_type.TEXT)

    with allure.step("Проверяем содержимое фрейма"):
        expected_text = "This is a sample page"
        assert expected_text in frame_text, f"Ожидается текст '{expected_text}', получено '{frame_text}'"

        browser_windows_page.log_step(f"✅ Текст фрейма корректен: {frame_text}")


@allure.epic("Alerts, Frame & Windows")
@allure.feature("Frames")
@allure.story("Multiple Frames")
@pytest.mark.alerts
def test_multiple_frames_handling(browser_windows_page: BrowserWindowsPage):
    """
    Тест работы с несколькими фреймами на странице.

    Проверяет способность переключаться между разными фреймами
    и корректно возвращаться в основной контент.
    """
    with allure.step("Подготавливаем тестовые данные"):
        browser_windows_page.log_step("Инициализация теста множественных фреймов")

    with allure.step("Проверяем наличие фреймов на странице"):
        frame_count = browser_windows_page.get_frames_count()
        browser_windows_page.log_step(f"Найдено фреймов на странице: {frame_count}")

        allure.attach(str(frame_count), "frames_count", allure.attachment_type.TEXT)

        assert frame_count > 0, f"На странице должен быть хотя бы один фрейм, найдено: {frame_count}"

    with allure.step("Переключаемся в первый фрейм"):
        first_frame_text = browser_windows_page.get_text_from_frame()
        browser_windows_page.log_step(f"Текст первого фрейма: {first_frame_text}")

        assert first_frame_text, "Первый фрейм должен содержать текст"

    with allure.step("Возвращаемся в основной контент"):
        browser_windows_page.switch_to_default_content()
        browser_windows_page.log_step("Переключились обратно в основной контент")

    with allure.step("Проверяем что мы в основном контенте"):
        # Можно проверить наличие элементов основной страницы
        main_content = browser_windows_page.is_main_content_visible()
        browser_windows_page.log_step(f"Основной контент видим: {main_content}")

        assert main_content, "Должны быть в основном контенте после переключения"


@allure.epic("Alerts, Frame & Windows")
@allure.feature("Frames")
@allure.story("Frame Isolation")
@pytest.mark.alerts
@pytest.mark.regression
def test_frame_isolation(browser_windows_page: BrowserWindowsPage):
    """
    Тест изоляции фреймов - элементы одного фрейма не доступны из другого.

    Проверяет что элементы внутри фрейма изолированы от основной страницы.
    """
    with allure.step("Пытаемся найти элементы фрейма из основного контекста"):
        browser_windows_page.log_step("Проверка изоляции: поиск элементов фрейма из основного контекста")

        # Пытаемся найти элементы фрейма не переключаясь в него
        frame_element_accessible = browser_windows_page.is_frame_element_accessible_from_main()
        browser_windows_page.log_step(f"Элементы фрейма доступны из основного контекста: {frame_element_accessible}")

        assert not frame_element_accessible, "Элементы фрейма НЕ должны быть доступны из основного контекста"

    with allure.step("Переключаемся во фрейм и ищем элементы"):
        frame_element_found = browser_windows_page.find_elements_inside_frame()
        browser_windows_page.log_step(f"Элементы найдены внутри фрейма: {frame_element_found}")

        assert frame_element_found, "Элементы ДОЛЖНЫ быть доступны внутри фрейма"

    with allure.step("Возвращаемся в основной контент и проверяем изоляцию"):
        browser_windows_page.switch_to_default_content()

        # Повторная проверка недоступности после возврата
        frame_element_accessible_after = browser_windows_page.is_frame_element_accessible_from_main()
        browser_windows_page.log_step(f"Элементы фрейма доступны после возврата: {frame_element_accessible_after}")

        assert not frame_element_accessible_after, "Изоляция фрейма должна сохраняться"

        isolation_result = {
            "before_switch": not frame_element_accessible,
            "inside_frame": frame_element_found,
            "after_return": not frame_element_accessible_after
        }
        allure.attach(str(isolation_result), "frame_isolation_test", allure.attachment_type.JSON)


@allure.epic("Alerts, Frame & Windows")
@allure.feature("Frames")
@allure.story("Frame Navigation")
@pytest.mark.alerts
def test_frame_navigation_and_interaction(browser_windows_page: BrowserWindowsPage):
    """
    Тест навигации по фреймам и взаимодействия с элементами внутри них.

    Проверяет полный цикл работы с фреймами: поиск, переключение, взаимодействие.
    """
    with allure.step("Получаем список всех фреймов"):
        browser_windows_page.log_step("Поиск всех доступных фреймов на странице")
        frames_info = browser_windows_page.get_all_frames_info()

        browser_windows_page.log_step(f"Информация о фреймах: {frames_info}")
        allure.attach(str(frames_info), "frames_info", allure.attachment_type.JSON)

    with allure.step("Последовательно переключаемся по всем фреймам"):
        for i, frame_info in enumerate(frames_info):
            with allure.step(f"Обрабатываем фрейм {i + 1}"):
                browser_windows_page.log_step(f"Переключение во фрейм {i + 1}: {frame_info}")

                # Переключаемся во фрейм
                browser_windows_page.switch_to_frame_by_index(i)

                # Получаем контент фрейма
                frame_content = browser_windows_page.get_current_frame_content()
                browser_windows_page.log_step(f"Контент фрейма {i + 1}: {frame_content[:100]}...")

                # Проверяем что получили какой-то контент
                assert frame_content, f"Фрейм {i + 1} должен содержать контент"

                allure.attach(frame_content, f"frame_{i + 1}_content", allure.attachment_type.TEXT)

                # Возвращаемся в основной контент перед переключением в следующий фрейм
                browser_windows_page.switch_to_default_content()
                browser_windows_page.log_step(f"Возврат в основной контент после фрейма {i + 1}")

    with allure.step("Финальная проверка возврата в основной контент"):
        is_main = browser_windows_page.is_main_content_visible()
        browser_windows_page.log_step(f"Финальная проверка основного контента: {is_main}")

        assert is_main, "После работы с фреймами должны быть в основном контенте"
