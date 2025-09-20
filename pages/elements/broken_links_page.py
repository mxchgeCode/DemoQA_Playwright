"""
Page Object для страницы Broken Links Images.
Содержит методы для проверки работоспособности изображений и ссылок.
"""

from playwright.sync_api import Page
from locators.elements.broken_links_locators import BrokenLinksLocators
from pages.base_page import BasePage


class BrokenLinksPage(BasePage):
    """
    Страница тестирования сломанных изображений и ссылок.
    Проверяет загрузку изображений и доступность ссылок.
    """

    def __init__(self, page: Page):
        """
        Инициализация страницы сломанных ссылок.

        Args:
            page: Экземпляр страницы Playwright
        """
        super().__init__(page)

    def is_image_broken(self, selector: str) -> bool:
        """
        Проверяет, является ли изображение сломанным (не загрузилось).

        Args:
            selector: CSS селектор изображения

        Returns:
            bool: True если изображение сломанное (naturalWidth = 0)

        Raises:
            Exception: Если элемент с селектором не найден
        """
        self.log_step(f"Проверяем состояние изображения: {selector}")
        widths = self.page.locator(selector).evaluate_all(
            "elements => elements.map(e => e.naturalWidth)"
        )
        if not widths:
            raise Exception(f"Ни одного элемента с селектором {selector} не найдено")
        return all(width == 0 for width in widths)

    def valid_image_broken(self) -> bool:
        """
        Проверяет, сломано ли валидное изображение.

        Returns:
            bool: True если валидное изображение сломано
        """
        return self.is_image_broken(BrokenLinksLocators.VALID_IMAGE)

    def broken_image_broken(self) -> bool:
        """
        Проверяет, сломано ли заведомо битое изображение.

        Returns:
            bool: True если битое изображение действительно сломано
        """
        return self.is_image_broken(BrokenLinksLocators.BROKEN_IMAGE)

    def is_valid_link_working(self) -> bool:
        """
        Проверяет работоспособность валидной ссылки.

        Returns:
            bool: True если ссылка возвращает успешный HTTP статус
        """
        self.log_step("Проверяем работоспособность валидной ссылки")
        href = self.page.get_attribute(BrokenLinksLocators.VALID_LINK, "href")
        response = self.page.request.get(href)
        return response.ok

    def is_broken_link_broken(self) -> bool:
        """
        Проверяет, действительно ли сломана заведомо битая ссылка.

        Returns:
            bool: True если ссылка возвращает ошибочный HTTP статус
        """
        self.log_step("Проверяем состояние сломанной ссылки")
        href = self.page.get_attribute(BrokenLinksLocators.BROKEN_LINK, "href")
        response = self.page.request.get(href)
        return not response.ok

    def click_valid_link(self) -> None:
        """
        Кликает по валидной ссылке.
        Postconditions: происходит переход по рабочей ссылке.
        """
        self.log_step("Кликаем по валидной ссылке")
        self.safe_click(BrokenLinksLocators.VALID_LINK)

    def click_broken_link(self) -> None:
        """
        Кликает по сломанной ссылке.
        Postconditions: происходит переход по нерабочей ссылке (может вызвать ошибку).
        """
        self.log_step("Кликаем по сломанной ссылке")
        self.safe_click(BrokenLinksLocators.BROKEN_LINK)
