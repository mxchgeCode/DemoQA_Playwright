"""
Page Object для страницы Date Picker.
Содержит методы для работы с календарем и выбором даты/времени.
"""

import time
from playwright.sync_api import Page
from locators.widgets.datepicker_locators import DatePickerLocators
from pages.widgets.base_page import WidgetBasePage


class DatePickerPage(WidgetBasePage):
    """
    Страница тестирования календарей и выбора даты.
    Поддерживает простой date picker и date/time picker с временем.
    """

    def __init__(self, page: Page):
        """
        Инициализация страницы Date Picker.

        Args:
            page: Экземпляр страницы Playwright
        """
        super().__init__(page)

    def open_date_picker(self) -> None:
        """
        Открывает простой календарь для выбора даты.
        Postconditions: календарь открыт и готов для выбора даты.
        """
        self.log_step("Открываем date picker")
        self.safe_click(DatepickerLocators.DATE_INPUT)
        self.wait_for_visible(".react-datepicker", timeout=3000)

    def open_date_time_picker(self) -> None:
        """
        Открывает календарь с выбором даты и времени.
        Postconditions: календарь с временем открыт и готов для выбора.
        """
        self.log_step("Открываем date time picker")
        self.safe_click(DatepickerLocators.DATE_TIME_INPUT)
        self.wait_for_visible(".react-datepicker", timeout=3000)

    def select_date(self, day: str, month: str = None, year: str = None) -> None:
        """
        Выбирает дату в календаре.

        Args:
            day: День месяца (например, "15")
            month: Месяц (например, "January", опционально)
            year: Год (например, "2024", опционально)

        Postconditions: выбранная дата установлена в поле ввода
        """
        self.log_step(f"Выбираем дату: {day}/{month}/{year}")

        # Если указан год, выбираем его
        if year:
            year_dropdown = self.page.locator(DatepickerLocators.YEAR_DROPDOWN)
            if year_dropdown.is_visible():
                year_dropdown.select_option(year)

        # Если указан месяц, выбираем его
        if month:
            month_dropdown = self.page.locator(DatepickerLocators.MONTH_DROPDOWN)
            if month_dropdown.is_visible():
                month_dropdown.select_option(month)

        # Выбираем день
        # Нормализуем номер дня (добавляем ведущий ноль если нужно)
        day_normalized = day.zfill(2)
        day_selector = f".react-datepicker__day--0{day_normalized}:not(.react-datepicker__day--outside-month)"

        day_element = self.page.locator(day_selector).first
        if day_element.is_visible():
            day_element.click()
        else:
            # Альтернативный способ - поиск по тексту
            day_elements = self.page.locator(
                f".react-datepicker__day:not(.react-datepicker__day--outside-month)"
            )
            for i in range(day_elements.count()):
                element = day_elements.nth(i)
                if element.inner_text().strip() == day:
                    element.click()
                    break

    def select_time(self, hour: str, minute: str = "00") -> None:
        """
        Выбирает время в time picker (только для date-time picker).

        Args:
            hour: Час в формате "14" или "02"
            minute: Минута в формате "30" или "00"

        Postconditions: выбранное время установлено
        """
        self.log_step(f"Выбираем время: {hour}:{minute}")

        # Кликаем по полю времени если оно есть
        time_input = self.page.locator(".react-datepicker__time-container")
        if time_input.is_visible():
            # Ищем нужное время в списке
            time_option = self.page.locator(f"text={hour}:{minute}")
            if time_option.is_visible():
                time_option.click()

    def get_selected_date(self) -> str:
        """
        Получает выбранную дату из простого date picker.

        Returns:
            str: Выбранная дата в формате поля ввода
        """
        date_input = self.page.locator(DatepickerLocators.DATE_INPUT)
        return date_input.input_value()

    def get_selected_date_time(self) -> str:
        """
        Получает выбранную дату и время из date-time picker.

        Returns:
            str: Выбранная дата и время в формате поля ввода
        """
        datetime_input = self.page.locator(DatepickerLocators.DATE_TIME_INPUT)
        return datetime_input.input_value()

    def clear_date(self) -> None:
        """
        Очищает поле простой даты.
        Postconditions: поле даты очищено.
        """
        self.log_step("Очищаем поле даты")
        date_input = self.page.locator(DatepickerLocators.DATE_INPUT)
        date_input.clear()

    def clear_date_time(self) -> None:
        """
        Очищает поле даты и времени.
        Postconditions: поле даты и времени очищено.
        """
        self.log_step("Очищаем поле даты и времени")
        datetime_input = self.page.locator(DatepickerLocators.DATE_TIME_INPUT)
        datetime_input.clear()

    def is_calendar_visible(self) -> bool:
        """
        Проверяет видимость календаря.

        Returns:
            bool: True если календарь открыт и видим
        """
        return self.page.locator(".react-datepicker").is_visible()

    def close_calendar(self) -> None:
        """
        Закрывает календарь кликом вне его области.
        Postconditions: календарь скрыт.
        """
        self.log_step("Закрываем календарь")
        # Кликаем в пустое место рядом с календарем
        self.page.click("body", position={"x": 10, "y": 10})

    def navigate_to_previous_month(self) -> None:
        """
        Переходит к предыдущему месяцу в календаре.
        Preconditions: календарь должен быть открыт.
        Postconditions: отображается предыдущий месяц.
        """
        self.log_step("Переходим к предыдущему месяцу")
        prev_button = self.page.locator(".react-datepicker__navigation--previous")
        if prev_button.is_visible():
            prev_button.click()
            time.sleep(500)

    def navigate_to_next_month(self) -> None:
        """
        Переходит к следующему месяцу в календаре.
        Preconditions: календарь должен быть открыт.
        Postconditions: отображается следующий месяц.
        """
        self.log_step("Переходим к следующему месяцу")
        next_button = self.page.locator(".react-datepicker__navigation--next")
        if next_button.is_visible():
            next_button.click()
            time.sleep(500)

    def get_current_month_year(self) -> str:
        """
        Получает текущий отображаемый месяц и год в календаре.

        Returns:
            str: Месяц и год в формате "January 2024"
        """
        month_year = self.page.locator(".react-datepicker__current-month")
        if month_year.is_visible():
            return month_year.inner_text()
        return ""

    def select_today(self) -> None:
        """
        Выбирает сегодняшнюю дату в календаре.
        Postconditions: выбрана текущая дата.
        """
        self.log_step("Выбираем сегодняшнюю дату")
        today_button = self.page.locator(".react-datepicker__day--today")
        if today_button.is_visible():
            today_button.click()

    def set_date_by_typing(self, date_string: str, is_datetime: bool = False) -> None:
        """
        Устанавливает дату путем прямого ввода в поле.

        Args:
            date_string: Строка даты в правильном формате
            is_datetime: True для поля date-time, False для простой даты

        Postconditions: дата установлена в поле ввода
        """
        self.log_step(f"Устанавливаем дату вводом: {date_string}")

        if is_datetime:
            input_field = self.page.locator(DatepickerLocators.DATE_TIME_INPUT)
        else:
            input_field = self.page.locator(DatepickerLocators.DATE_INPUT)

        input_field.clear()
        input_field.type(date_string)
        # Нажимаем Enter для подтверждения
        input_field.press("Enter")
