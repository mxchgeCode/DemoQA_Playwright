"""
Page Object для страницы Text Box.
Содержит методы для заполнения текстовых полей и получения результатов вывода.
"""

from playwright.sync_api import Page
from locators.elements.text_box_locators import TextBoxLocators
from pages.base_page import BasePage


class TextBoxPage(BasePage):
    """
    Страница тестирования текстовых полей.
    Содержит поля для имени, email, текущего и постоянного адресов.
    """

    def __init__(self, page: Page):
        """
        Инициализация страницы Text Box.

        Args:
            page: Экземпляр страницы Playwright
        """
        super().__init__(page)

    def fill_user_name(self, name: str) -> None:
        """
        Заполняет поле "Full Name".

        Args:
            name: Полное имя пользователя

        Postconditions: поле заполнено указанным именем
        """
        self.log_step(f"Заполняем поле Full Name: {name}")
        self.safe_fill(TextBoxLocators.USER_NAME, name)

    def fill_user_email(self, email: str) -> None:
        """
        Заполняет поле "Email".

        Args:
            email: Email адрес пользователя

        Postconditions: поле заполнено указанным email
        """
        self.log_step(f"Заполняем поле Email: {email}")
        self.safe_fill(TextBoxLocators.USER_EMAIL, email)

    def fill_current_address(self, address: str) -> None:
        """
        Заполняет поле "Current Address".

        Args:
            address: Текущий адрес пользователя

        Postconditions: поле заполнено указанным адресом
        """
        self.log_step(f"Заполняем поле Current Address: {address}")
        self.safe_fill(TextBoxLocators.CURRENT_ADDRESS, address)

    def fill_permanent_address(self, address: str) -> None:
        """
        Заполняет поле "Permanent Address".

        Args:
            address: Постоянный адрес пользователя

        Postconditions: поле заполнено указанным адресом
        """
        self.log_step(f"Заполняем поле Permanent Address: {address}")
        self.safe_fill(TextBoxLocators.PERMANENT_ADDRESS, address)

    def submit(self) -> None:
        """
        Отправляет форму нажатием на кнопку Submit.
        Postconditions: форма отправлена, отображаются результаты вывода.
        """
        self.log_step("Отправляем форму")
        self.safe_click(TextBoxLocators.SUBMIT_BUTTON)

    def get_output_name(self) -> str:
        """
        Получает отображаемое имя из области вывода.

        Returns:
            str: Имя из области вывода или пустая строка
        """
        return self.get_text_safe(TextBoxLocators.OUTPUT_NAME) or ""

    def get_output_email(self) -> str:
        """
        Получает отображаемый email из области вывода.

        Returns:
            str: Email из области вывода или пустая строка
        """
        return self.get_text_safe(TextBoxLocators.OUTPUT_EMAIL) or ""

    def get_output_current_address(self) -> str:
        """
        Получает отображаемый текущий адрес из области вывода.

        Returns:
            str: Текущий адрес из области вывода или пустая строка
        """
        return self.get_text_safe(TextBoxLocators.OUTPUT_CURRENT_ADDRESS) or ""

    def get_output_permanent_address(self) -> str:
        """
        Получает отображаемый постоянный адрес из области вывода.

        Returns:
            str: Постоянный адрес из области вывода или пустая строка
        """
        return self.get_text_safe(TextBoxLocators.OUTPUT_PERMANENT_ADDRESS) or ""

    def is_output_visible(self) -> bool:
        """
        Проверяет, видима ли область вывода результатов.

        Returns:
            bool: True если область вывода видима
        """
        return self.page.locator("#output").is_visible()

    def get_all_output_data(self) -> dict:
        """
        Получает все данные из области вывода в виде словаря.

        Returns:
            dict: Словарь с ключами name, email, current_address, permanent_address
        """
        return {
            "name": self.get_output_name(),
            "email": self.get_output_email(),
            "current_address": self.get_output_current_address(),
            "permanent_address": self.get_output_permanent_address(),
        }

    def fill_all_fields(
        self, name: str, email: str, current_addr: str, permanent_addr: str
    ) -> None:
        """
        Заполняет все поля формы одним вызовом.

        Args:
            name: Полное имя
            email: Email адрес
            current_addr: Текущий адрес
            permanent_addr: Постоянный адрес

        Postconditions: все поля заполнены указанными значениями
        """
        self.log_step("Заполняем все поля формы")
        self.fill_user_name(name)
        self.fill_user_email(email)
        self.fill_current_address(current_addr)
        self.fill_permanent_address(permanent_addr)

    def clear_all_fields(self) -> None:
        """
        Очищает все поля формы.
        Postconditions: все поля формы пусты.
        """
        self.log_step("Очищаем все поля формы")
        self.page.fill(TextBoxLocators.USER_NAME, "")
        self.page.fill(TextBoxLocators.USER_EMAIL, "")
        self.page.fill(TextBoxLocators.CURRENT_ADDRESS, "")
        self.page.fill(TextBoxLocators.PERMANENT_ADDRESS, "")
