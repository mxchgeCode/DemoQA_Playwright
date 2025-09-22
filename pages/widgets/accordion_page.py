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

    # === Методы для совместимости с тестами ===

    def get_all_sections_states(self) -> dict:
        """
        Получает состояния всех секций аккордеона.

        Returns:
            dict: Словарь с состояниями секций (expanded/collapsed)
        """
        return {
            "first_section": self.is_first_section_expanded(),
            "second_section": self.is_second_section_expanded(),
            "third_section": self.is_third_section_expanded(),
        }

    def close_all_sections(self) -> None:
        """
        Закрывает все секции аккордеона.
        """
        self.log_step("Закрываем все секции аккордеона")
        # Кликаем по всем секциям, чтобы закрыть их
        if self.is_first_section_expanded():
            self.click_first_section()
        if self.is_second_section_expanded():
            self.click_second_section()
        if self.is_third_section_expanded():
            self.click_third_section()

    def is_accordion_keyboard_accessible(self) -> bool:
        """
        Проверяет доступность аккордеона для клавиатурной навигации.

        Returns:
            bool: True если аккордеон доступен для клавиатуры
        """
        # Проверяем наличие tabindex атрибутов у заголовков секций
        try:
            first_header_tabindex = self.first_section_header.get_attribute("tabindex")
            second_header_tabindex = self.second_section_header.get_attribute("tabindex")
            third_header_tabindex = self.third_section_header.get_attribute("tabindex")

            # Если хотя бы один заголовок имеет tabindex, считаем доступным
            return (
                first_header_tabindex is not None or
                second_header_tabindex is not None or
                third_header_tabindex is not None
            )
        except:
            return False
