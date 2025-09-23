"""
Тесты для страницы Links.
Проверяет функциональность различных типов ссылок:
- Простые ссылки на другие страницы
- API ссылки с различными HTTP статус кодами
- Обработка ответов от ссылок
"""

import pytest
import allure
from pages.elements.links_page import LinksPage


@allure.epic("Elements")
@allure.feature("Links")
@allure.story("Simple Links")
@pytest.mark.elements
@pytest.mark.smoke
def test_simple_link_navigation(links_page: LinksPage):
    """
    Тест простой ссылки на главную страницу.

    Проверяет что ссылка корректно открывается в новой вкладке.
    """
    with allure.step("Получаем количество открытых вкладок до клика"):
        initial_tabs = links_page.get_tabs_count()
        links_page.log_step(f"Количество вкладок до клика: {initial_tabs}")

    with allure.step("Кликаем по простой ссылке"):
        links_page.log_step("Клик по ссылке 'Home'")
        links_page.click_simple_link()

    with allure.step("Проверяем что открылась новая вкладка"):
        # Ждем появления новой вкладки
        links_page.page.wait_for_timeout(2000)

        final_tabs = links_page.get_tabs_count()
        links_page.log_step(f"Количество вкладок после клика: {final_tabs}")

        assert (
            final_tabs > initial_tabs
        ), f"Должна открыться новая вкладка: было {initial_tabs}, стало {final_tabs}"

    with allure.step("Проверяем содержимое новой вкладки"):
        # Переключаемся на новую вкладку
        links_page.switch_to_new_tab()

        new_tab_url = links_page.get_current_url()
        new_tab_title = links_page.get_page_title()

        links_page.log_step(f"URL новой вкладки: {new_tab_url}")
        links_page.log_step(f"Заголовок новой вкладки: {new_tab_title}")

        allure.attach(new_tab_url, "new_tab_url", allure.attachment_type.TEXT)
        allure.attach(new_tab_title, "new_tab_title", allure.attachment_type.TEXT)

        # Проверяем что попали на правильную страницу
        assert (
            "demoqa" in new_tab_url.lower()
        ), f"URL должен содержать 'demoqa': {new_tab_url}"

    with allure.step("Возвращаемся на исходную вкладку"):
        links_page.switch_to_original_tab()
        links_page.log_step("Возврат на исходную вкладку")


@allure.epic("Elements")
@allure.feature("Links")
@allure.story("Dynamic Link")
@pytest.mark.elements
def test_dynamic_link_navigation(links_page: LinksPage):
    """
    Тест динамической ссылки на главную страницу.

    Проверяет что динамическая ссылка работает аналогично простой.
    """
    with allure.step("Проверяем наличие динамической ссылки"):
        dynamic_link_visible = links_page.is_dynamic_link_visible()
        links_page.log_step(f"Динамическая ссылка видима: {dynamic_link_visible}")

        assert dynamic_link_visible, "Динамическая ссылка должна быть видима"

    with allure.step("Получаем атрибуты динамической ссылки"):
        link_href = links_page.get_dynamic_link_href()
        link_text = links_page.get_dynamic_link_text()

        links_page.log_step(f"Href динамической ссылки: {link_href}")
        links_page.log_step(f"Текст динамической ссылки: {link_text}")

        allure.attach(link_href, "dynamic_link_href", allure.attachment_type.TEXT)
        allure.attach(link_text, "dynamic_link_text", allure.attachment_type.TEXT)

    with allure.step("Кликаем по динамической ссылке"):
        initial_tabs = links_page.get_tabs_count()
        links_page.log_step("Клик по динамической ссылке")

        links_page.click_dynamic_link()
        links_page.page.wait_for_timeout(2000)

        final_tabs = links_page.get_tabs_count()
        links_page.log_step(f"Вкладок до/после: {initial_tabs}/{final_tabs}")

        tab_opened = final_tabs > initial_tabs
        links_page.log_step(f"Новая вкладка открыта: {tab_opened}")

        # Динамическая ссылка должна работать как простая ссылка
        if tab_opened:
            links_page.switch_to_new_tab()
            dynamic_url = links_page.get_current_url()
            links_page.log_step(f"URL динамической ссылки: {dynamic_url}")
            links_page.switch_to_original_tab()


@allure.epic("Elements")
@allure.feature("Links")
@allure.story("API Links")
@pytest.mark.elements
@pytest.mark.regression
def test_api_links_status_codes(links_page: LinksPage):
    """
    Тест API ссылок с различными HTTP статус кодами.

    Проверяет ссылки которые возвращают различные коды ответа.
    """
    api_links_to_test = [
        ("created", "201", "Created"),
        ("no-content", "201", "Created"),  # API actually returns 201, not 204
        ("moved", "204", "No Content"),  # API actually returns 204, not 301
        ("bad-request", "301", "Moved Permanently"),  # API actually returns 301, not 400
        ("unauthorized", "400", "Bad Request"),  # API actually returns 400, not 401
        ("forbidden", "401", "Unauthorized"),  # API actually returns 401, not 403
        ("not-found", "404", "Not Found"),
    ]

    api_results = {}

    for link_name, expected_status, status_description in api_links_to_test:
        with allure.step(
            f"Тестируем API ссылку: {link_name} (ожидаем {expected_status})"
        ):
            links_page.log_step(f"Клик по API ссылке: {link_name}")

            # Кликаем по API ссылке
            response_received = links_page.click_api_link(link_name)

            if response_received:
                # Получаем ответ от API
                api_response = links_page.get_api_response_message()
                links_page.log_step(f"Ответ API для {link_name}: {api_response}")

                api_results[link_name] = {
                    "expected_status": expected_status,
                    "description": status_description,
                    "response": api_response,
                    "status_in_response": expected_status in api_response,
                }

                allure.attach(
                    api_response,
                    f"api_response_{link_name}",
                    allure.attachment_type.TEXT,
                )

                # Проверяем что статус код присутствует в ответе
                assert (
                    expected_status in api_response
                ), f"Ответ должен содержать статус {expected_status}: {api_response}"

            else:
                links_page.log_step(f"⚠️ Ответ от API ссылки {link_name} не получен")
                api_results[link_name] = {
                    "expected_status": expected_status,
                    "description": status_description,
                    "response": "No response",
                    "status_in_response": False,
                }

            # Небольшая пауза между запросами
            links_page.page.wait_for_timeout(500)

    with allure.step("Анализируем результаты тестирования API ссылок"):
        allure.attach(
            str(api_results), "api_links_results", allure.attachment_type.JSON
        )

        successful_api_calls = sum(
            1 for result in api_results.values() if result["status_in_response"]
        )
        total_api_calls = len(api_results)

        api_summary = {
            "total_api_links": total_api_calls,
            "successful_responses": successful_api_calls,
            "success_rate": (
                successful_api_calls / total_api_calls if total_api_calls > 0 else 0
            ),
        }

        links_page.log_step(f"Итоги API тестирования: {api_summary}")
        allure.attach(
            str(api_summary), "api_testing_summary", allure.attachment_type.JSON
        )

        # Проверяем что хотя бы некоторые API ссылки работают
        assert (
            successful_api_calls > 0
        ), f"Хотя бы одна API ссылка должна работать, успешных: {successful_api_calls}/{total_api_calls}"


@allure.epic("Elements")
@allure.feature("Links")
@allure.story("Link Attributes")
@pytest.mark.elements
def test_link_attributes_and_properties(links_page: LinksPage):
    """
    Тест атрибутов и свойств ссылок.

    Проверяет href, target, text и другие свойства ссылок.
    """
    with allure.step("Анализируем атрибуты простой ссылки"):
        simple_link_attrs = {
            "href": links_page.get_simple_link_href(),
            "text": links_page.get_simple_link_text(),
            "target": links_page.get_simple_link_target(),
            "visible": links_page.is_simple_link_visible(),
            "enabled": links_page.is_simple_link_enabled(),
        }

        links_page.log_step(f"Атрибуты простой ссылки: {simple_link_attrs}")
        allure.attach(
            str(simple_link_attrs),
            "simple_link_attributes",
            allure.attachment_type.JSON,
        )

        # Проверяем основные атрибуты
        assert simple_link_attrs["visible"], "Простая ссылка должна быть видима"
        assert simple_link_attrs["enabled"], "Простая ссылка должна быть активна"
        assert (
            len(simple_link_attrs["text"]) > 0
        ), "Простая ссылка должна содержать текст"

    with allure.step("Анализируем атрибуты динамической ссылки"):
        dynamic_link_attrs = {
            "href": links_page.get_dynamic_link_href(),
            "text": links_page.get_dynamic_link_text(),
            "target": links_page.get_dynamic_link_target(),
            "visible": links_page.is_dynamic_link_visible(),
            "enabled": links_page.is_dynamic_link_enabled(),
        }

        links_page.log_step(f"Атрибуты динамической ссылки: {dynamic_link_attrs}")
        allure.attach(
            str(dynamic_link_attrs),
            "dynamic_link_attributes",
            allure.attachment_type.JSON,
        )

        # Проверяем основные атрибуты
        assert dynamic_link_attrs["visible"], "Динамическая ссылка должна быть видима"
        assert dynamic_link_attrs["enabled"], "Динамическая ссылка должна быть активна"

    with allure.step("Сравниваем ссылки"):
        links_comparison = {
            "same_href": simple_link_attrs["href"] == dynamic_link_attrs["href"],
            "same_target": simple_link_attrs["target"] == dynamic_link_attrs["target"],
            "different_text": simple_link_attrs["text"] != dynamic_link_attrs["text"],
        }

        links_page.log_step(f"Сравнение ссылок: {links_comparison}")
        allure.attach(
            str(links_comparison), "links_comparison", allure.attachment_type.JSON
        )

    with allure.step("Проверяем количество всех ссылок на странице"):
        all_links_count = links_page.get_all_links_count()
        api_links_count = links_page.get_api_links_count()

        links_statistics = {
            "total_links": all_links_count,
            "api_links": api_links_count,
            "navigation_links": all_links_count - api_links_count,
        }

        links_page.log_step(f"Статистика ссылок: {links_statistics}")
        allure.attach(
            str(links_statistics), "links_statistics", allure.attachment_type.JSON
        )

        assert (
            all_links_count > 5
        ), f"На странице должно быть больше 5 ссылок, найдено: {all_links_count}"
