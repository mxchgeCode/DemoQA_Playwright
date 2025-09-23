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
        # Храним исходную вкладку для переключений
        self._original_page = None

    # ======== Простой и динамический переход (алиасы под тесты) ========
    def click_simple_link(self) -> None:
        self.click_home_link()

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

    # ======== Переключение вкладок ========
    def get_tabs_count(self) -> int:
        return len(self.page.context.pages)

    def switch_to_new_tab(self) -> None:
        """
        Переключается на последнюю открытую вкладку.
        Сохраняет исходную вкладку для возврата.
        """
        if self._original_page is None:
            self._original_page = self.page
        pages = self.page.context.pages
        if pages:
            self.page = pages[-1]

    def switch_to_original_tab(self) -> None:
        """Возвращается на исходную вкладку, если сохранена."""
        if self._original_page is not None:
            self.page = self._original_page

    def get_current_url(self) -> str:
        return self.page.url

    def get_page_title(self) -> str:
        return self.page.title()

    # ======== Атрибуты ссылок ========
    def is_simple_link_visible(self) -> bool:
        return self.page.locator(LinksLocators.SIMPLE_LINK).is_visible()

    def is_simple_link_enabled(self) -> bool:
        return not self.page.locator(LinksLocators.SIMPLE_LINK).is_disabled()

    def get_simple_link_href(self) -> str:
        return self.page.locator(LinksLocators.SIMPLE_LINK).get_attribute("href") or ""

    def get_simple_link_text(self) -> str:
        return (self.page.locator(LinksLocators.SIMPLE_LINK).inner_text() or "").strip()

    def get_simple_link_target(self) -> str:
        return self.page.locator(LinksLocators.SIMPLE_LINK).get_attribute("target") or ""

    def is_dynamic_link_visible(self) -> bool:
        return self.page.locator(LinksLocators.DYNAMIC_LINK).is_visible()

    def is_dynamic_link_enabled(self) -> bool:
        return not self.page.locator(LinksLocators.DYNAMIC_LINK).is_disabled()

    def get_dynamic_link_href(self) -> str:
        return self.page.locator(LinksLocators.DYNAMIC_LINK).get_attribute("href") or ""

    def get_dynamic_link_text(self) -> str:
        return (self.page.locator(LinksLocators.DYNAMIC_LINK).inner_text() or "").strip()

    def get_dynamic_link_target(self) -> str:
        return self.page.locator(LinksLocators.DYNAMIC_LINK).get_attribute("target") or ""

    def click_dynamic_link(self) -> None:
        self.log_step("Кликаем по динамической ссылке")
        self.safe_click(LinksLocators.DYNAMIC_LINK)

    # ======== API ссылки (универсальные методы под тесты) ========
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
        return self.get_text_safe(LinksLocators.LINK_RESPONSE_MESSAGE) or ""

    def click_api_link(self, name: str) -> bool:
        """
        Кликает по API ссылке по ее имени ('created','no-content','moved','bad-request','unauthorized','forbidden','not-found')
        и ожидает появления блока ответа. Возвращает True если ответ появился.
        """
        mapping = {
            "created": LinksLocators.CREATED_LINK,
            "no-content": LinksLocators.NO_CONTENT_LINK,
            "moved": LinksLocators.MOVED_LINK,
            "bad-request": LinksLocators.BAD_REQUEST_LINK,
            "unauthorized": LinksLocators.UNAUTHORIZED_LINK,
            "forbidden": LinksLocators.FORBIDDEN_LINK,
            "not-found": LinksLocators.NOT_FOUND_LINK,
        }
        loc = mapping.get(name)
        if not loc:
            return False
        self.safe_click(loc)
        try:
            self.page.locator(LinksLocators.LINK_RESPONSE_MESSAGE).wait_for(
                state="visible", timeout=5000
            )
            return True
        except Exception:
            return False

    def get_api_response_message(self) -> str:
        """Возвращает текст ответа API (универсальный метод под тесты)."""
        self.page.wait_for_timeout(2000)  # Пауза для получения ответа
        return self.get_response_message()

    # ======== Статистика ссылок ========
    def get_all_links_count(self) -> int:
        return self.page.locator(LinksLocators.ALL_LINKS).count()

    def get_api_links_count(self) -> int:
        # На странице API ссылки имеют id из набора ниже
        api_ids = [
            LinksLocators.CREATED_LINK,
            LinksLocators.NO_CONTENT_LINK,
            LinksLocators.MOVED_LINK,
            LinksLocators.BAD_REQUEST_LINK,
            LinksLocators.UNAUTHORIZED_LINK,
            LinksLocators.FORBIDDEN_LINK,
            LinksLocators.NOT_FOUND_LINK,
        ]
        total = 0
        for sel in api_ids:
            total += self.page.locator(sel).count()
        return total

    # ======== Приватные вспомогательные (оставлены без изменений) ========
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
