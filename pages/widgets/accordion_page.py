"""
Page Object для страницы Accordion с раскрывающимися секциями.
Содержит методы для работы с тремя секциями аккордеона.
"""

from playwright.sync_api import Page
from locators.widgets.accordion_locators import AccordionLocators
from pages.base_page import BasePage


class AccordionPage(BasePage):
    """
    Страница тестирования аккордеона с тремя раскрывающимися секциями.
    Каждая секция может быть раскрыта/свернута независимо.
    """

    def __init__(self, page: Page):
        """
        Инициализация страницы аккордеона.

        Args:
            page: Экземпляр страницы Playwright
        """
        super().__init__(page)
        self.first_section_header = page.locator(AccordionLocators.FIRST_SECTION_HEADER)
        self.first_section_content = page.locator(
            AccordionLocators.FIRST_SECTION_CONTENT
        )
        self.first_section_button = page.locator(AccordionLocators.FIRST_SECTION_BUTTON)

        self.second_section_header = page.locator(
            AccordionLocators.SECOND_SECTION_HEADER
        )
        self.second_section_content = page.locator(
            AccordionLocators.SECOND_SECTION_CONTENT
        )
        self.second_section_button = page.locator(
            AccordionLocators.SECOND_SECTION_BUTTON
        )

        self.third_section_header = page.locator(AccordionLocators.THIRD_SECTION_HEADER)
        self.third_section_content = page.locator(
            AccordionLocators.THIRD_SECTION_CONTENT
        )
        self.third_section_button = page.locator(AccordionLocators.THIRD_SECTION_BUTTON)

    def click_first_section(self) -> None:
        """
        Кликает по заголовку первой секции для раскрытия/сворачивания.
        Postconditions: состояние первой секции изменяется (раскрыта/свернута).
        """
        self.log_step("Кликаем по первой секции аккордеона")
        self.first_section_header.click(force=True)
        self.page.wait_for_timeout(1000)

    def click_second_section(self) -> None:
        """
        Кликает по заголовку второй секции для раскрытия/сворачивания.
        Postconditions: состояние второй секции изменяется.
        """
        self.log_step("Кликаем по второй секции аккордеона")
        self.second_section_header.click(force=True)
        self.page.wait_for_timeout(1000)

    def click_third_section(self) -> None:
        """
        Кликает по заголовку третьей секции для раскрытия/сворачивания.
        Postconditions: состояние третьей секции изменяется.
        """
        self.log_step("Кликаем по третьей секции аккордеона")
        self.third_section_header.click(force=True)
        self.page.wait_for_timeout(1000)

    def is_first_section_expanded(self) -> bool:
        """
        Проверяет, раскрыта ли первая секция аккордеона.

        Returns:
            bool: True если секция раскрыта и контент виден
        """
        try:
            return self.first_section_content.is_visible()
        except:
            return False

    def is_second_section_expanded(self) -> bool:
        """
        Проверяет, раскрыта ли вторая секция аккордеона.

        Returns:
            bool: True если секция раскрыта и контент виден
        """
        try:
            return self.second_section_content.is_visible()
        except:
            return False

    def is_third_section_expanded(self) -> bool:
        """
        Проверяет, раскрыта ли третья секция аккордеона.

        Returns:
            bool: True если секция раскрыта и контент виден
        """
        try:
            return self.third_section_content.is_visible()
        except:
            return False

    def get_first_section_text(self) -> str:
        """
        Получает текстовое содержимое первой секции.

        Returns:
            str: Текст содержимого первой секции
        """
        return self.get_text_safe(AccordionLocators.FIRST_SECTION_CONTENT)

    def get_second_section_text(self) -> str:
        """
        Получает текстовое содержимое второй секции.

        Returns:
            str: Текст содержимого второй секции
        """
        return self.get_text_safe(AccordionLocators.SECOND_SECTION_CONTENT)

    def get_third_section_text(self) -> str:
        """
        Получает текстовое содержимое третьей секции.

        Returns:
            str: Текст содержимого третьей секции
        """
        return self.get_text_safe(AccordionLocators.THIRD_SECTION_CONTENT)
