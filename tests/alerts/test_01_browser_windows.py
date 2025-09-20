"""
Тесты для страницы Browser Windows.
Проверяет функциональность открытия новых вкладок и окон браузера.
"""

import pytest
import allure
from data import URLs


@allure.epic("Alerts, Frame & Windows")
@allure.feature("Browser Windows")
@allure.story("New Tab Opening")
@pytest.mark.alerts
@pytest.mark.smoke
def test_open_new_tab(browser_windows_page):
    """
    Тест открытия новой вкладки браузера.

    Шаги:
    1. Получить начальное количество открытых вкладок
    2. Кликнуть по кнопке "New Tab"
    3. Дождаться открытия новой вкладки
    4. Проверить что количество вкладок увеличилось
    """
    with allure.step("Получаем начальное количество вкладок"):
        initial_tabs_count = browser_windows_page.get_current_window_count()
        allure.attach(f"Начальное количество: {initial_tabs_count}", "initial_count")

    with allure.step("Кликаем по кнопке New Tab и ждем открытия"):
        # Настраиваем ожидание новой страницы перед кликом
        with browser_windows_page.page.context.expect_page() as new_page_info:
            browser_windows_page.click_new_tab()

        new_page = new_page_info.value

    with allure.step("Проверяем что новая вкладка открылась"):
        final_tabs_count = browser_windows_page.get_current_window_count()

        assert (
            final_tabs_count == initial_tabs_count + 1
        ), f"Ожидалось {initial_tabs_count + 1} вкладок, получено {final_tabs_count}"

        # Проверяем что новая страница содержит ожидаемый контент
        assert new_page.is_visible("h1"), "На новой вкладке должен быть заголовок"

        allure.attach(f"Финальное количество: {final_tabs_count}", "final_count")
        allure.attach(new_page.url, "new_page_url")

    with allure.step("Закрываем новую вкладку для очистки"):
        new_page.close()


@allure.epic("Alerts, Frame & Windows")
@allure.feature("Browser Windows")
@allure.story("New Window Opening")
@pytest.mark.alerts
def test_open_new_window(browser_windows_page):
    """
    Тест открытия нового окна браузера.

    Шаги:
    1. Зафиксировать начальное количество окон
    2. Кликнуть по кнопке "New Window"
    3. Дождаться открытия нового окна
    4. Проверить увеличение количества окон
    """
    with allure.step("Фиксируем начальное состояние"):
        initial_windows_count = browser_windows_page.get_current_window_count()

    with allure.step("Открываем новое окно"):
        with browser_windows_page.page.context.expect_page(
            timeout=10000
        ) as new_window_info:
            browser_windows_page.click_new_window()

        new_window = new_window_info.value

    with allure.step("Верифицируем открытие нового окна"):
        final_windows_count = browser_windows_page.get_current_window_count()

        assert (
            final_windows_count == initial_windows_count + 1
        ), f"Количество окон должно увеличиться с {initial_windows_count} до {initial_windows_count + 1}"

        # Проверяем что новое окно функционально
        assert new_window.url, "Новое окно должно иметь URL"
        assert not new_window.is_closed(), "Новое окно не должно быть закрыто"

        allure.attach(new_window.url, "new_window_url")

    with allure.step("Очистка: закрываем новое окно"):
        new_window.close()


@allure.epic("Alerts, Frame & Windows")
@allure.feature("Browser Windows")
@allure.story("Message Window Opening")
@pytest.mark.alerts
def test_open_new_window_message(browser_windows_page):
    """
    Тест открытия нового окна с сообщением.

    Шаги:
    1. Запустить ожидание нового окна
    2. Кликнуть по кнопке "New Window Message"
    3. Проверить что окно открылось с сообщением
    4. Проверить содержимое сообщения
    """
    with allure.step("Открываем окно с сообщением"):
        with browser_windows_page.page.context.expect_page() as message_window_info:
            browser_windows_page.click_new_window_message()

        message_window = message_window_info.value

    with allure.step("Проверяем содержимое окна с сообщением"):
        # Ждем загрузки содержимого
        message_window.wait_for_load_state("domcontentloaded")

        # Проверяем что в окне есть контент
        page_content = message_window.content()
        assert len(page_content) > 0, "Окно с сообщением должно содержать контент"

        allure.attach(message_window.url, "message_window_url")
        allure.attach(page_content[:500] + "...", "message_window_content_preview")

    with allure.step("Закрываем окно с сообщением"):
        message_window.close()


@allure.epic("Alerts, Frame & Windows")
@allure.feature("Browser Windows")
@allure.story("Multiple Windows Management")
@pytest.mark.alerts
@pytest.mark.regression
def test_multiple_windows_handling(browser_windows_page):
    """
    Тест управления несколькими окнами одновременно.

    Шаги:
    1. Открыть несколько вкладок и окон
    2. Проверить корректность подсчета
    3. Проверить переключение между окнами
    4. Закрыть все дополнительные окна
    """
    opened_pages = []
    initial_count = browser_windows_page.get_current_window_count()

    with allure.step("Открываем несколько новых окон"):
        # Открываем новую вкладку
        with browser_windows_page.page.context.expect_page() as new_tab_info:
            browser_windows_page.click_new_tab()
        opened_pages.append(new_tab_info.value)

        # Открываем новое окно
        with browser_windows_page.page.context.expect_page() as new_window_info:
            browser_windows_page.click_new_window()
        opened_pages.append(new_window_info.value)

        # Открываем окно с сообщением
        with browser_windows_page.page.context.expect_page() as message_window_info:
            browser_windows_page.click_new_window_message()
        opened_pages.append(message_window_info.value)

    with allure.step("Проверяем корректность подсчета окон"):
        current_count = browser_windows_page.get_current_window_count()
        expected_count = initial_count + 3

        assert (
            current_count == expected_count
        ), f"Ожидалось {expected_count} окон, получено {current_count}"

        allure.attach(f"Открыто окон: {current_count}", "windows_count")

    with allure.step("Проверяем доступность каждого окна"):
        for i, page in enumerate(opened_pages):
            assert not page.is_closed(), f"Окно {i+1} не должно быть закрыто"
            assert page.url, f"Окно {i+1} должно иметь URL"

    with allure.step("Закрываем все дополнительные окна"):
        for page in opened_pages:
            page.close()

        final_count = browser_windows_page.get_current_window_count()
        assert (
            final_count == initial_count
        ), f"После закрытия должно остаться {initial_count} окон, осталось {final_count}"


@allure.epic("Alerts, Frame & Windows")
@allure.feature("Browser Windows")
@allure.story("Window Context Switching")
@pytest.mark.alerts
def test_window_context_switching(browser_windows_page):
    """
    Тест переключения контекста между окнами.

    Проверяет возможность работы с элементами в разных окнах.
    """
    original_page = browser_windows_page.page

    with allure.step("Открываем новое окно"):
        with original_page.context.expect_page() as new_window_info:
            browser_windows_page.click_new_window()
        new_window = new_window_info.value

    with allure.step("Работаем в контексте нового окна"):
        # Переходим на страницу с элементами в новом окне
        new_window.goto(URLs.TEXT_BOX)
        new_window.wait_for_selector("#userName", timeout=10000)

        # Выполняем действия в новом окне
        new_window.fill("#userName", "Test User in New Window")
        filled_value = new_window.input_value("#userName")

        assert (
            filled_value == "Test User in New Window"
        ), "Значение должно быть заполнено в новом окне"

    with allure.step("Возвращаемся к исходному окну"):
        # Проверяем что исходное окно все еще доступно
        assert original_page.url != new_window.url, "Окна должны иметь разные URL"

        # Можем работать с исходным окном
        original_title = original_page.title()
        assert (
            "Browser Windows" in original_title
        ), "Исходное окно должно сохранить свое содержимое"

    with allure.step("Очистка"):
        new_window.close()

        # Проверяем что после закрытия нового окна исходное остается рабочим
        assert not original_page.is_closed(), "Исходное окно должно остаться открытым"
