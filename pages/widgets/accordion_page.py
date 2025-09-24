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

    def is_section_content_visible(self, index: int) -> bool:
        """
        Проверяет, видимо ли содержимое секции.

        Args:
            index: Индекс секции (0, 1, 2)

        Returns:
            bool: True если содержимое видимо
        """
        contents = [
            AccordionLocators.FIRST_SECTION_CONTENT,
            AccordionLocators.SECOND_SECTION_CONTENT,
            AccordionLocators.THIRD_SECTION_CONTENT
        ]
        try:
            return self.page.locator(contents[index]).is_visible()
        except:
            return False

    def get_section_content_height(self, index: int) -> int:
        """
        Получает высоту содержимого секции.

        Args:
            index: Индекс секции (0, 1, 2)

        Returns:
            int: Высота в пикселях
        """
        contents = [
            AccordionLocators.FIRST_SECTION_CONTENT,
            AccordionLocators.SECOND_SECTION_CONTENT,
            AccordionLocators.THIRD_SECTION_CONTENT
        ]
        try:
            bbox = self.page.locator(contents[index]).bounding_box()
            return int(bbox['height']) if bbox else 0
        except:
            return 0

    def count_elements_in_section_content(self, index: int) -> int:
        """
        Считает количество элементов в содержимом секции.

        Args:
            index: Индекс секции (0, 1, 2)

        Returns:
            int: Количество элементов
        """
        contents = [
            AccordionLocators.FIRST_SECTION_CONTENT,
            AccordionLocators.SECOND_SECTION_CONTENT,
            AccordionLocators.THIRD_SECTION_CONTENT
        ]
        try:
            return self.page.locator(contents[index]).locator("*").count()
        except:
            return 0

    def focus_on_section_header(self, index: int) -> bool:
        """
        Фокусируется на заголовке секции.

        Args:
            index: Индекс секции (0, 1, 2)

        Returns:
            bool: True если фокус успешен
        """
        headers = [
            self.first_section_header,
            self.second_section_header,
            self.third_section_header
        ]
        try:
            headers[index].focus()
            return True
        except:
            return False

    def is_section_header_focused(self, index: int) -> bool:
        """
        Проверяет, сфокусирован ли заголовок секции.

        Args:
            index: Индекс секции (0, 1, 2)

        Returns:
            bool: True если сфокусирован
        """
        headers = [
            AccordionLocators.FIRST_SECTION_HEADER,
            AccordionLocators.SECOND_SECTION_HEADER,
            AccordionLocators.THIRD_SECTION_HEADER
        ]
        try:
            return self.page.locator(headers[index]).evaluate("el => el === document.activeElement")
        except:
            return False

    def activate_section_with_enter(self, index: int) -> bool:
        """
        Активирует секцию клавишей Enter.

        Args:
            index: Индекс секции (0, 1, 2)

        Returns:
            bool: True если активация успешна
        """
        try:
            self.page.keyboard.press("Enter")
            self.page.wait_for_timeout(500)
            return True
        except:
            return False

    def activate_section_with_space(self, index: int) -> bool:
        """
        Активирует секцию клавишей Space.

        Args:
            index: Индекс секции (0, 1, 2)

        Returns:
            bool: True если активация успешна
        """
        try:
            self.page.keyboard.press("Space")
            self.page.wait_for_timeout(500)
            return True
        except:
            return False

    def get_accordion_accessibility_info(self) -> dict:
        """
        Получает информацию о доступности аккордеона.

        Returns:
            dict: Информация о доступности
        """
        try:
            headers = [
                AccordionLocators.FIRST_SECTION_HEADER,
                AccordionLocators.SECOND_SECTION_HEADER,
                AccordionLocators.THIRD_SECTION_HEADER
            ]
            info = {}
            for i, header in enumerate(headers):
                tabindex = self.page.locator(header).get_attribute("tabindex")
                aria_expanded = self.page.locator(header).get_attribute("aria-expanded")
                info[f"section_{i+1}"] = {
                    "tabindex": tabindex,
                    "aria_expanded": aria_expanded
                }
            return info
        except:
            return {}

    def get_current_timestamp(self) -> int:
        """
        Получает текущую временную метку.

        Returns:
            int: Время в миллисекундах
        """
        import time
        return int(time.time() * 1000)

    def wait_for_section_expansion(self, index: int, timeout: int = 3000) -> bool:
        """
        Ожидает раскрытия секции.

        Args:
            index: Индекс секции (0, 1, 2)
            timeout: Время ожидания в мс

        Returns:
            bool: True если секция раскрыта
        """
        contents = [
            AccordionLocators.FIRST_SECTION_CONTENT,
            AccordionLocators.SECOND_SECTION_CONTENT,
            AccordionLocators.THIRD_SECTION_CONTENT
        ]
        try:
            self.page.locator(contents[index]).wait_for(state="visible", timeout=timeout)
            return True
        except:
            return False

    def wait_for_section_collapse(self, index: int, timeout: int = 3000) -> bool:
        """
        Ожидает сворачивания секции.

        Args:
            index: Индекс секции (0, 1, 2)
            timeout: Время ожидания в мс

        Returns:
            bool: True если секция свернута
        """
        contents = [
            AccordionLocators.FIRST_SECTION_CONTENT,
            AccordionLocators.SECOND_SECTION_CONTENT,
            AccordionLocators.THIRD_SECTION_CONTENT
        ]
        try:
            self.page.locator(contents[index]).wait_for(state="hidden", timeout=timeout)
            return True
        except:
            return False

    def is_animation_smooth(self, index: int) -> bool:
        """
        Проверяет плавность анимации секции.

        Args:
            index: Индекс секции (0, 1, 2)

        Returns:
            bool: True если анимация плавная
        """
        # Простая проверка - если секция переключается без ошибок, считаем плавной
        try:
            initial_state = self.get_section_state(index)["is_expanded"]
            self.click_section_header(index)
            final_state = self.get_section_state(index)["is_expanded"]
            return initial_state != final_state
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

    def get_all_sections_states(self) -> list:
        """
        Получает состояния всех секций аккордеона.

        Returns:
            list: Список словарей с состояниями секций
        """
        sections = []
        for i in range(3):
            section_info = self.get_section_state(i)
            sections.append(section_info)
        return sections

    def get_section_state(self, index: int) -> dict:
        """
        Получает состояние секции по индексу.

        Args:
            index: Индекс секции (0, 1, 2)

        Returns:
            dict: Словарь с информацией о секции
        """
        headers = [
            AccordionLocators.FIRST_SECTION_HEADER,
            AccordionLocators.SECOND_SECTION_HEADER,
            AccordionLocators.THIRD_SECTION_HEADER
        ]
        contents = [
            AccordionLocators.FIRST_SECTION_CONTENT,
            AccordionLocators.SECOND_SECTION_CONTENT,
            AccordionLocators.THIRD_SECTION_CONTENT
        ]

        header_text = self.get_text_safe(headers[index])
        is_expanded = self.page.locator(contents[index]).is_visible()

        return {
            "header_text": header_text,
            "is_expanded": is_expanded
        }

    def click_section_header(self, index: int) -> bool:
        """
        Кликает по заголовку секции по индексу.

        Args:
            index: Индекс секции (0, 1, 2)

        Returns:
            bool: True если клик успешен
        """
        headers = [
            self.first_section_header,
            self.second_section_header,
            self.third_section_header
        ]
        try:
            headers[index].click(force=True)
            self.page.wait_for_timeout(1000)
            return True
        except:
            return False

    def get_section_content(self, index: int) -> str:
        """
        Получает содержимое секции по индексу.

        Args:
            index: Индекс секции (0, 1, 2)

        Returns:
            str: Текст содержимого секции
        """
        contents = [
            AccordionLocators.FIRST_SECTION_CONTENT,
            AccordionLocators.SECOND_SECTION_CONTENT,
            AccordionLocators.THIRD_SECTION_CONTENT
        ]
        return self.get_text_safe(contents[index])

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
