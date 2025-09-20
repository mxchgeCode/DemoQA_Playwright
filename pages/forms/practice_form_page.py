"""
Page Object для страницы Practice Form.
Содержит методы для заполнения и отправки формы с различными типами полей.
"""

from playwright.sync_api import Page
from locators.forms.practice_form_locators import PracticeFormLocators
from pages.base_page import BasePage


class AutomationPracticeFormPage(BasePage):
    """
    Страница тестирования формы с различными элементами ввода.
    Включает текстовые поля, радиокнопки, чекбоксы, выпадающие списки, загрузку файлов.
    """

    def __init__(self, page: Page):
        """
        Инициализация страницы Practice Form.

        Args:
            page: Экземпляр страницы Playwright
        """
        super().__init__(page)

    def fill_first_name(self, first_name: str) -> None:
        """
        Заполняет поле "First Name".

        Args:
            first_name: Имя для заполнения
        """
        self.log_step(f"Заполняем поле First Name: {first_name}")
        self.safe_fill(PracticeFormLocators.FIRST_NAME, first_name)

    def fill_last_name(self, last_name: str) -> None:
        """
        Заполняет поле "Last Name".

        Args:
            last_name: Фамилия для заполнения
        """
        self.log_step(f"Заполняем поле Last Name: {last_name}")
        self.safe_fill(PracticeFormLocators.LAST_NAME, last_name)

    def fill_email(self, email: str) -> None:
        """
        Заполняет поле "Email".

        Args:
            email: Email адрес для заполнения
        """
        self.log_step(f"Заполняем поле Email: {email}")
        self.safe_fill(PracticeFormLocators.EMAIL, email)

    def select_gender(self, gender: str) -> None:
        """
        Выбирает пол в радиокнопках.

        Args:
            gender: Пол для выбора ("Male", "Female", "Other")
        """
        self.log_step(f"Выбираем пол: {gender}")
        if gender.lower() == "male":
            self.safe_click(PracticeFormLocators.GENDER_MALE)
        elif gender.lower() == "female":
            self.safe_click(PracticeFormLocators.GENDER_FEMALE)
        elif gender.lower() == "other":
            self.safe_click(PracticeFormLocators.GENDER_OTHER)

    def fill_mobile_number(self, mobile: str) -> None:
        """
        Заполняет поле "Mobile Number".

        Args:
            mobile: Номер телефона для заполнения
        """
        self.log_step(f"Заполняем номер телефона: {mobile}")
        self.safe_fill(PracticeFormLocators.MOBILE, mobile)

    def set_date_of_birth(self, day: str, month: str, year: str) -> None:
        """
        Устанавливает дату рождения через date picker.

        Args:
            day: День (например, "15")
            month: Месяц (например, "January")
            year: Год (например, "1990")
        """
        self.log_step(f"Устанавливаем дату рождения: {day}/{month}/{year}")

        # Кликаем по полю даты для открытия календаря
        self.safe_click(PracticeFormLocators.DATE_OF_BIRTH)

        # Выбираем месяц
        month_dropdown = self.page.locator(PracticeFormLocators.MONTH_DROPDOWN)
        month_dropdown.select_option(month)

        # Выбираем год
        year_dropdown = self.page.locator(PracticeFormLocators.YEAR_DROPDOWN)
        year_dropdown.select_option(year)

        # Выбираем день
        day_element = self.page.locator(f".react-datepicker__day--0{day.zfill(2)}")
        day_element.click()

    def fill_subjects(self, subjects: list[str]) -> None:
        """
        Заполняет поле "Subjects" с автодополнением.

        Args:
            subjects: Список предметов для добавления
        """
        self.log_step(f"Заполняем предметы: {subjects}")
        subjects_input = self.page.locator(PracticeFormLocators.SUBJECTS)

        for subject in subjects:
            subjects_input.click()
            subjects_input.type(subject)
            # Ждем появления опций и выбираем первую
            self.page.wait_for_timeout(500)
            suggestion = self.page.locator(f"text={subject}").first
            if suggestion.is_visible():
                suggestion.click()

    def select_hobbies(self, hobbies: list[str]) -> None:
        """
        Выбирает хобби из чекбоксов.

        Args:
            hobbies: Список хобби ("Sports", "Reading", "Music")
        """
        self.log_step(f"Выбираем хобби: {hobbies}")
        for hobby in hobbies:
            if hobby.lower() == "sports":
                self.safe_click(PracticeFormLocators.HOBBY_SPORTS)
            elif hobby.lower() == "reading":
                self.safe_click(PracticeFormLocators.HOBBY_READING)
            elif hobby.lower() == "music":
                self.safe_click(PracticeFormLocators.HOBBY_MUSIC)

    def upload_picture(self, file_path: str) -> None:
        """
        Загружает изображение через файловый input.

        Args:
            file_path: Путь к файлу изображения
        """
        self.log_step(f"Загружаем изображение: {file_path}")
        self.page.set_input_files(PracticeFormLocators.UPLOAD_PICTURE, file_path)

    def fill_current_address(self, address: str) -> None:
        """
        Заполняет поле "Current Address".

        Args:
            address: Адрес для заполнения
        """
        self.log_step(f"Заполняем текущий адрес: {address}")
        self.safe_fill(PracticeFormLocators.CURRENT_ADDRESS, address)

    def select_state(self, state: str) -> None:
        """
        Выбирает штат из выпадающего списка.

        Args:
            state: Название штата для выбора
        """
        self.log_step(f"Выбираем штат: {state}")
        # Кликаем по dropdown для его открытия
        state_dropdown = self.page.locator(PracticeFormLocators.STATE_DROPDOWN)
        state_dropdown.click()

        # Выбираем опцию
        option = self.page.locator(f"text={state}")
        option.click()

    def select_city(self, city: str) -> None:
        """
        Выбирает город из выпадающего списка.

        Args:
            city: Название города для выбора
        """
        self.log_step(f"Выбираем город: {city}")
        # Кликаем по dropdown для его открытия
        city_dropdown = self.page.locator(PracticeFormLocators.CITY_DROPDOWN)
        city_dropdown.click()

        # Выбираем опцию
        option = self.page.locator(f"text={city}")
        option.click()

    def submit_form(self) -> None:
        """
        Отправляет форму нажатием на кнопку Submit.
        Postconditions: появляется модальное окно с результатами отправки.
        """
        self.log_step("Отправляем форму")
        self.safe_click(PracticeFormLocators.SUBMIT_BUTTON)

    def is_modal_visible(self) -> bool:
        """
        Проверяет видимость модального окна с результатами.

        Returns:
            bool: True если модальное окно с результатами видимо
        """
        return self.page.locator(PracticeFormLocators.MODAL_CONTENT).is_visible()

    def get_modal_title(self) -> str:
        """
        Получает заголовок модального окна с результатами.

        Returns:
            str: Заголовок модального окна
        """
        return self.get_text_safe(PracticeFormLocators.MODAL_TITLE) or ""

    def close_modal(self) -> None:
        """
        Закрывает модальное окно с результатами.
        Postconditions: модальное окно скрыто.
        """
        self.log_step("Закрываем модальное окно с результатами")
        self.safe_click(PracticeFormLocators.CLOSE_MODAL_BUTTON)

    def get_form_results(self) -> dict:
        """
        Извлекает данные из таблицы результатов в модальном окне.

        Returns:
            dict: Словарь с парами ключ-значение из таблицы результатов
        """
        results = {}
        table_rows = self.page.locator(f"{PracticeFormLocators.MODAL_CONTENT} tbody tr")

        for i in range(table_rows.count()):
            row = table_rows.nth(i)
            cells = row.locator("td")
            if cells.count() >= 2:
                key = cells.nth(0).inner_text().strip()
                value = cells.nth(1).inner_text().strip()
                results[key] = value

        return results

    def fill_complete_form(self, form_data: dict) -> None:
        """
        Заполняет всю форму используя словарь с данными.

        Args:
            form_data: Словарь с данными формы

        Example:
            form_data = {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'gender': 'Male',
                'mobile': '1234567890',
                'subjects': ['Math', 'Physics'],
                'hobbies': ['Sports', 'Reading'],
                'address': '123 Main St'
            }
        """
        self.log_step("Заполняем всю форму")

        if "first_name" in form_data:
            self.fill_first_name(form_data["first_name"])
        if "last_name" in form_data:
            self.fill_last_name(form_data["last_name"])
        if "email" in form_data:
            self.fill_email(form_data["email"])
        if "gender" in form_data:
            self.select_gender(form_data["gender"])
        if "mobile" in form_data:
            self.fill_mobile_number(form_data["mobile"])
        if "subjects" in form_data:
            self.fill_subjects(form_data["subjects"])
        if "hobbies" in form_data:
            self.select_hobbies(form_data["hobbies"])
        if "address" in form_data:
            self.fill_current_address(form_data["address"])
        if "state" in form_data:
            self.select_state(form_data["state"])
        if "city" in form_data:
            self.select_city(form_data["city"])
