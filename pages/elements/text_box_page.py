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

        # Проверяем состояние перед отправкой
        submit_button = self.page.locator(TextBoxLocators.SUBMIT_BUTTON)
        initial_button_text = submit_button.inner_text() if submit_button.is_visible() else "not visible"

        self.safe_click(TextBoxLocators.SUBMIT_BUTTON)

        # Добавляем отладочную информацию
        self.log_step("Форма отправлена, ждем результатов...")

        # Проверяем что кнопка submit изменила состояние (если есть индикатор загрузки)
        try:
            submit_button = self.page.locator(TextBoxLocators.SUBMIT_BUTTON)
            if submit_button.is_visible():
                final_button_text = submit_button.inner_text()
                self.log_step(f"Кнопка submit: '{initial_button_text}' -> '{final_button_text}'")

                # Проверяем если кнопка стала disabled (индикатор загрузки)
                is_disabled = submit_button.is_disabled()
                self.log_step(f"Кнопка submit disabled: {is_disabled}")
            else:
                self.log_step("Кнопка submit не видима после отправки")
        except Exception as e:
            self.log_step(f"Ошибка при проверке кнопки submit: {e}")

        # Небольшая пауза для обработки
        self.page.wait_for_timeout(500)

    def get_output_name(self) -> str:
        """
        Получает отображаемое имя из области вывода.

        Returns:
            str: Имя из области вывода или пустая строка
        """
        # Пробуем основные селекторы
        name = self.get_text_safe(TextBoxLocators.OUTPUT_NAME)
        if name:
            return name

        # Пробуем альтернативные селекторы
        name = self.get_text_safe(TextBoxLocators.OUTPUT_NAME_ALT)
        if name:
            return name

        # Пробуем найти по тексту "Name:"
        try:
            name_element = self.page.locator("p").filter(has_text="Name:").first
            if name_element.is_visible():
                return name_element.inner_text().replace("Name:", "").strip()
        except Exception:
            pass

        # Пробуем найти все элементы в области вывода и ищем имя
        try:
            output_container = self.page.locator("#output")
            if output_container.is_visible():
                all_text = output_container.inner_text()
                # Ищем строку с именем
                lines = all_text.split('\n')
                for line in lines:
                    if 'Name:' in line:
                        return line.replace('Name:', '').strip()
        except Exception:
            pass

        return ""

    def get_output_email(self) -> str:
        """
        Получает отображаемый email из области вывода.

        Returns:
            str: Email из области вывода или пустая строка
        """
        # Пробуем основные селекторы
        email = self.get_text_safe(TextBoxLocators.OUTPUT_EMAIL)
        if email:
            return email

        # Пробуем альтернативные селекторы
        email = self.get_text_safe(TextBoxLocators.OUTPUT_EMAIL_ALT)
        if email:
            return email

        # Пробуем найти по тексту "Email:"
        try:
            email_element = self.page.locator("p").filter(has_text="Email:").first
            if email_element.is_visible():
                return email_element.inner_text().replace("Email:", "").strip()
        except Exception:
            pass

        # Пробуем найти все элементы в области вывода и ищем email
        try:
            output_container = self.page.locator("#output")
            if output_container.is_visible():
                all_text = output_container.inner_text()
                # Ищем строку с email
                lines = all_text.split('\n')
                for line in lines:
                    if 'Email:' in line:
                        return line.replace('Email:', '').strip()
        except Exception:
            pass

        return ""

    def get_output_current_address(self) -> str:
        """
        Получает отображаемый текущий адрес из области вывода.

        Returns:
            str: Текущий адрес из области вывода или пустая строка
        """
        # Пробуем основные селекторы
        address = self.get_text_safe(TextBoxLocators.OUTPUT_CURRENT_ADDRESS)
        if address:
            return address

        # Пробуем альтернативные селекторы
        address = self.get_text_safe(TextBoxLocators.OUTPUT_CURRENT_ADDRESS_ALT)
        if address:
            return address

        # Пробуем найти по тексту "Current Address:"
        try:
            address_element = self.page.locator("p").filter(has_text="Current Address:").first
            if address_element.is_visible():
                return address_element.inner_text().replace("Current Address:", "").strip()
        except Exception:
            pass

        return ""

    def get_output_permanent_address(self) -> str:
        """
        Получает отображаемый постоянный адрес из области вывода.

        Returns:
            str: Постоянный адрес из области вывода или пустая строка
        """
        # Пробуем основные селекторы
        address = self.get_text_safe(TextBoxLocators.OUTPUT_PERMANENT_ADDRESS)
        if address:
            return address

        # Пробуем альтернативные селекторы
        address = self.get_text_safe(TextBoxLocators.OUTPUT_PERMANENT_ADDRESS_ALT)
        if address:
            return address

        # Пробуем найти по тексту "Permanent Address:"
        try:
            address_element = self.page.locator("p").filter(has_text="Permanent Address:").first
            if address_element.is_visible():
                return address_element.inner_text().replace("Permanent Address:", "").strip()
        except Exception:
            pass

        return ""

    def is_output_visible(self) -> bool:
        """
        Проверяет, видима ли область вывода результатов.

        Returns:
            bool: True если область вывода видима
        """
        return self.page.locator("#output").is_visible()

    def wait_for_output(self, timeout: int = 5000) -> bool:
        """
        Ожидает появления области вывода результатов.

        Args:
            timeout: Таймаут ожидания в миллисекундах

        Returns:
            bool: True если область вывода появилась
        """
        try:
            self.page.locator("#output").wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def debug_page_content(self) -> dict:
        """
        Отладочная функция для анализа содержимого страницы после отправки формы.

        Returns:
            dict: Словарь с отладочной информацией
        """
        debug_info = {}

        try:
            # Проверяем основную область вывода
            output_locator = self.page.locator("#output")
            debug_info["output_visible"] = output_locator.is_visible()
            if output_locator.is_visible():
                debug_info["output_text"] = output_locator.inner_text()
                debug_info["output_html"] = output_locator.inner_html()
            else:
                debug_info["output_text"] = "Output not visible"
                debug_info["output_html"] = "Output not visible"

            # Проверяем тело страницы
            body_text = self.page.locator("body").inner_text()
            debug_info["body_contains_output"] = "#output" in body_text

            # Ищем любые элементы, которые могут содержать результаты
            all_divs = self.page.locator("div").all()
            div_contents = []
            for i, div in enumerate(all_divs[:10]):  # Проверяем первые 10 div'ов
                try:
                    text = div.inner_text()
                    if len(text) > 10:  # Только непустые элементы
                        div_contents.append(f"Div {i}: {text[:100]}...")
                except:
                    pass
            debug_info["sample_divs"] = div_contents

            # Проверяем наличие элементов с id, содержащими "output"
            output_elements = self.page.locator("[id*='output']").all()
            debug_info["output_elements_count"] = len(output_elements)
            if output_elements:
                debug_info["output_elements"] = []
                for elem in output_elements:
                    try:
                        elem_id = elem.get_attribute("id")
                        elem_text = elem.inner_text()
                        debug_info["output_elements"].append({
                            "id": elem_id,
                            "text": elem_text[:100] if elem_text else ""
                        })
                    except:
                        pass

            # Добавляем прямое логирование для отладки
            print(f"DEBUG PAGE CONTENT: {debug_info}")

        except Exception as e:
            debug_info["error"] = str(e)
            print(f"DEBUG ERROR: {e}")

        return debug_info

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

    def is_submit_button_enabled(self) -> bool:
        """
        Проверяет, активна ли кнопка отправки формы.

        Returns:
            bool: True если кнопка активна и доступна для клика
        """
        try:
            submit_button = self.page.locator(TextBoxLocators.SUBMIT_BUTTON)
            if not submit_button.is_visible():
                return False

            # Проверяем, не заблокирована ли кнопка (disabled)
            is_disabled = submit_button.is_disabled()

            # Проверяем, можно ли кликнуть по кнопке
            is_clickable = submit_button.is_enabled()

            self.log_step(f"Submit button state: visible={submit_button.is_visible()}, disabled={is_disabled}, enabled={is_clickable}")

            return submit_button.is_visible() and not is_disabled and is_clickable
        except Exception as e:
            self.log_step(f"Error checking submit button state: {e}")
            return False
