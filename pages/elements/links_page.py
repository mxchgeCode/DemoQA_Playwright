"""
Page Object для страницы Links с различными типами ссылок.
Содержит методы для клика по ссылкам и проверки API responses.
"""

from playwright.sync_api import Page, expect
from locators.elements.links_locators import LinksLocators
from pages.base_page import BasePage


class LinksPage(BasePage):
    """
    Страница тестирования различных типов ссылок.
    Включает простые ссылки и API call links с проверкой статус-кодов.
    """

    def __init__(self, page: Page):
        """
        Инициализация страницы ссылок.

        Args:
            page: Экземпляр страницы Playwright
        """
        super().__init__(page)

    def click_home_link(self) -> None:
        """
        Кликает по простой Home ссылке.
        Postconditions: открывается новая вкладка с главной страницей.
        """
        self.log_step("Кликаем по простой Home ссылке")
        self.safe_click(LinksLocators.SIMPLE_LINK)

    def click_home_dynamic_link(self) -> None:
        """
        Кликает по динамической Home ссылке.
        Postconditions: открывается новая вкладка с главной страницей.
        """
        self.log_step("Кликаем по динамической Home ссылке")
        self.safe_click(LinksLocators.DYNAMIC_LINK)

    def click_link_and_check_response(self, locator: str, expected_text: str) -> None:
        """
        Кликает по API ссылке и проверяет ответ.

        Args:
            locator: CSS селектор ссылки для клика
            expected_text: Ожидаемый текст в ответе

        Postconditions: отображается сообщение с результатом API запроса
        """
        self.log_step(f"Кликаем по API ссылке и проверяем ответ: {expected_text}")
        self.safe_click(locator)
        expect(self.page.locator(LinksLocators.LINK_RESPONSE_MESSAGE)).to_have_text(
            expected_text
        )

    def get_response_message(self) -> str:
        """
        Получает текст сообщения об ответе API.

        Returns:
            str: Текст сообщения о статусе API запроса
        """
        return self.get_text_safe(LinksLocators.LINK_RESPONSE_MESSAGE)

    def click_created_link(self) -> None:
        """
        Кликает по ссылке Created (201).
        Postconditions: отображается сообщение о создании ресурса.
        """
        self.click_link_and_check_response(
            LinksLocators.CREATED_LINK,
            "Link has responded with staus 201 and status text Created",
        )

    def click_no_content_link(self) -> None:
        """
        Кликает по ссылке No Content (204).
        Postconditions: отображается сообщение об отсутствии содержимого.
        """
        self.click_link_and_check_response(
            LinksLocators.NO_CONTENT_LINK,
            "Link has responded with staus 204 and status text No Content",
        )

    def click_moved_link(self) -> None:
        """
        Кликает по ссылке Moved (301).
        Postconditions: отображается сообщение о перемещении ресурса.
        """
        self.click_link_and_check_response(
            LinksLocators.MOVED_LINK,
            "Link has responded with staus 301 and status text Moved Permanently",
        )

    def click_bad_request_link(self) -> None:
        """
        Кликает по ссылке Bad Request (400).
        Postconditions: отображается сообщение о неверном запросе.
        """
        self.click_link_and_check_response(
            LinksLocators.BAD_REQUEST_LINK,
            "Link has responded with staus 400 and status text Bad Request",
        )

    def click_unauthorized_link(self) -> None:
        """
        Кликает по ссылке Unauthorized (401).
        Postconditions: отображается сообщение о неавторизованном доступе.
        """
        self.click_link_and_check_response(
            LinksLocators.UNAUTHORIZED_LINK,
            "Link has responded with staus 401 and status text Unauthorized",
        )

    def click_forbidden_link(self) -> None:
        """
        Кликает по ссылке Forbidden (403).
        Postconditions: отображается сообщение о запрещенном доступе.
        """
        self.click_link_and_check_response(
            LinksLocators.FORBIDDEN_LINK,
            "Link has responded with staus 403 and status text Forbidden",
        )

    def click_not_found_link(self) -> None:
        """
        Кликает по ссылке Not Found (404).
        Postconditions: отображается сообщение о ненайденном ресурсе.
        """
        self.click_link_and_check_response(
            LinksLocators.NOT_FOUND_LINK,
            "Link has responded with staus 404 and status text Not Found",
        )
