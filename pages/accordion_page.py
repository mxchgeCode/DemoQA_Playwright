from playwright.sync_api import Page


class AccordionPage:
    def __init__(self, page: Page):
        self.page = page
        # Используем CSS селекторы (более надежные)
        self.first_section_header = page.locator("#section1Heading")
        self.first_section_content = page.locator("#section1Content")
        self.first_section_button = page.locator("#section1Heading button")

        self.second_section_header = page.locator("#section2Heading")
        self.second_section_content = page.locator("#section2Content")
        self.second_section_button = page.locator("#section2Heading button")

        self.third_section_header = page.locator("#section3Heading")
        self.third_section_content = page.locator("#section3Content")
        self.third_section_button = page.locator("#section3Heading button")

    def click_first_section(self):
        """Клик по заголовку первого раздела."""
        self.first_section_header.click(force=True)
        self.page.wait_for_timeout(1000)

    def click_second_section(self):
        """Клик по заголовку второго раздела."""
        self.second_section_header.click(force=True)
        self.page.wait_for_timeout(1000)

    def click_third_section(self):
        """Клик по заголовку третьего раздела."""
        self.third_section_header.click(force=True)
        self.page.wait_for_timeout(1000)

    def click_first_button(self):
        """Клик по кнопке первого раздела."""
        # Проверяем, что кнопка видима, если нет - кликаем по заголовку
        try:
            if self.first_section_button.is_visible():
                self.first_section_button.click(force=True)
            else:
                self.first_section_header.click(force=True)
        except:
            self.first_section_header.click(force=True)
        self.page.wait_for_timeout(1000)

    def click_second_button(self):
        """Клик по кнопке второго раздела."""
        try:
            if self.second_section_button.is_visible():
                self.second_section_button.click(force=True)
            else:
                self.second_section_header.click(force=True)
        except:
            self.second_section_header.click(force=True)
        self.page.wait_for_timeout(1000)

    def click_third_button(self):
        """Клик по кнопке третьего раздела."""
        try:
            if self.third_section_button.is_visible():
                self.third_section_button.click(force=True)
            else:
                self.third_section_header.click(force=True)
        except:
            self.third_section_header.click(force=True)
        self.page.wait_for_timeout(1000)

    def is_first_section_expanded(self) -> bool:
        """Проверяет, раскрыт ли первый раздел."""
        try:
            return self.first_section_content.is_visible()
        except:
            return False

    def is_second_section_expanded(self) -> bool:
        """Проверяет, раскрыт ли второй раздел."""
        try:
            return self.second_section_content.is_visible()
        except:
            return False

    def is_third_section_expanded(self) -> bool:
        """Проверяет, раскрыт ли третий раздел."""
        try:
            return self.third_section_content.is_visible()
        except:
            return False

    def is_first_section_collapsed(self) -> bool:
        """Проверяет, свернут ли первый раздел."""
        try:
            return not self.first_section_content.is_visible()
        except:
            return True

    def is_second_section_collapsed(self) -> bool:
        """Проверяет, свернут ли второй раздел."""
        try:
            return not self.second_section_content.is_visible()
        except:
            return True

    def is_third_section_collapsed(self) -> bool:
        """Проверяет, свернут ли третий раздел."""
        try:
            return not self.third_section_content.is_visible()
        except:
            return True

    def get_first_section_text(self) -> str:
        """Получает текст первого раздела."""
        return self.first_section_content.text_content().strip()

    def get_second_section_text(self) -> str:
        """Получает текст второго раздела."""
        return self.second_section_content.text_content().strip()

    def get_third_section_text(self) -> str:
        """Получает текст третьего раздела."""
        return self.third_section_content.text_content().strip()

    def get_first_section_header_text(self) -> str:
        """Получает текст заголовка первого раздела."""
        return self.first_section_header.text_content().strip()

    def get_second_section_header_text(self) -> str:
        """Получает текст заголовка второго раздела."""
        return self.second_section_header.text_content().strip()

    def get_third_section_header_text(self) -> str:
        """Получает текст заголовка третьего раздела."""
        return self.third_section_header.text_content().strip()
