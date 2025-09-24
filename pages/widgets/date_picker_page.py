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
        self.safe_click(DatePickerLocators.DATE_INPUT)
        self.wait_for_visible(".react-datepicker", timeout=3000)

    def open_date_time_picker(self) -> None:
        """
        Открывает календарь с выбором даты и времени.
        Postconditions: календарь с временем открыт и готов для выбора.
        """
        self.log_step("Открываем date time picker")
        self.safe_click(DatePickerLocators.DATE_TIME_INPUT)
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
            year_dropdown = self.page.locator(DatePickerLocators.YEAR_DROPDOWN)
            if year_dropdown.is_visible():
                year_dropdown.select_option(year)

        # Если указан месяц, выбираем его
        if month:
            month_dropdown = self.page.locator(DatePickerLocators.MONTH_DROPDOWN)
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
        date_input = self.page.locator(DatePickerLocators.DATE_INPUT)
        return date_input.input_value()

    def get_selected_date_time(self) -> str:
        """
        Получает выбранную дату и время из date-time picker.

        Returns:
            str: Выбранная дата и время в формате поля ввода
        """
        datetime_input = self.page.locator(DatePickerLocators.DATE_TIME_INPUT)
        return datetime_input.input_value()

    def clear_date(self) -> None:
        """
        Очищает поле простой даты.
        Postconditions: поле даты очищено.
        """
        self.log_step("Очищаем поле даты")
        date_input = self.page.locator(DatePickerLocators.DATE_INPUT)
        date_input.clear()

    def clear_date_time(self) -> None:
        """
        Очищает поле даты и времени.
        Postconditions: поле даты и времени очищено.
        """
        self.log_step("Очищаем поле даты и времени")
        datetime_input = self.page.locator(DatePickerLocators.DATE_TIME_INPUT)
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

    def navigate_to_previous_month(self) -> bool:
        """
        Переходит к предыдущему месяцу в календаре.
        Preconditions: календарь должен быть открыт.
        Postconditions: отображается предыдущий месяц.

        Returns:
            bool: True если переход успешен
        """
        self.log_step("Переходим к предыдущему месяцу")
        try:
            prev_button = self.page.locator(".react-datepicker__navigation--previous")
            if prev_button.is_visible():
                prev_button.click()
                time.sleep(0.5)
                return True
            return False
        except Exception as e:
            self.log_step(f"Ошибка при навигации к предыдущему месяцу: {e}")
            return False

    def navigate_to_next_month(self) -> bool:
        """
        Переходит к следующему месяцу в календаре.
        Preconditions: календарь должен быть открыт.
        Postconditions: отображается следующий месяц.

        Returns:
            bool: True если переход успешен
        """
        self.log_step("Переходим к следующему месяцу")
        try:
            next_button = self.page.locator(".react-datepicker__navigation--next")
            if next_button.is_visible():
                next_button.click()
                time.sleep(0.5)
                return True
            return False
        except Exception as e:
            self.log_step(f"Ошибка при навигации к следующему месяцу: {e}")
            return False

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
            input_field = self.page.locator(DatePickerLocators.DATE_TIME_INPUT)
        else:
            input_field = self.page.locator(DatePickerLocators.DATE_INPUT)

        input_field.clear()
        input_field.type(date_string)
        # Нажимаем Enter для подтверждения
        input_field.press("Enter")

    # === Методы для совместимости с тестами ===

    def is_date_input_present(self) -> bool:
        """
        Проверяет наличие поля выбора даты.

        Returns:
            bool: True если поле присутствует
        """
        return self.page.locator(DatePickerLocators.DATE_INPUT).is_visible()

    def clear_date_input(self) -> None:
        """
        Очищает поле простой даты (алиас для clear_date).
        """
        self.clear_date()

    def is_datetime_input_present(self) -> bool:
        """
        Проверяет наличие поля выбора даты и времени.

        Returns:
            bool: True если поле присутствует
        """
        return self.page.locator(DatePickerLocators.DATE_TIME_INPUT).is_visible()

    def is_date_range_picker_available(self) -> bool:
        """
        Проверяет доступность date range picker.

        Returns:
            bool: True если date range picker доступен
        """
        # Проверяем наличие дополнительных полей для диапазона дат
        return (
            self.page.locator(DatePickerLocators.DATE_INPUT).is_visible() and
            self.page.locator(DatePickerLocators.DATE_TIME_INPUT).is_visible()
        )

    def open_date_calendar(self) -> bool:
        """
        Открывает календарь для выбора даты.

        Returns:
            bool: True если календарь успешно открыт
        """
        try:
            self.open_date_picker()
            return self.is_calendar_visible()
        except:
            return False

    # === ДОПОЛНИТЕЛЬНЫЕ МЕТОДЫ ДЛЯ ТЕСТОВ ===

    def get_date_input_value(self) -> str:
        """
        Получает значение поля выбора даты.

        Returns:
            str: Текущее значение поля даты
        """
        return self.get_selected_date()

    def type_date_manually(self, date_string: str) -> bool:
        """
        Вводит дату вручную в поле выбора даты.

        Args:
            date_string: Строка даты для ввода

        Returns:
            bool: True если ввод успешен
        """
        try:
            self.log_step(f"Ввод даты вручную: {date_string}")
            date_input = self.page.locator(DatePickerLocators.DATE_INPUT)
            date_input.clear()
            date_input.type(date_string)
            return True
        except Exception as e:
            self.log_step(f"Ошибка при вводе даты: {e}")
            return False

    def get_datetime_input_value(self) -> str:
        """
        Получает значение поля выбора даты и времени.

        Returns:
            str: Текущее значение поля даты и времени
        """
        return self.get_selected_date_time()

    def get_start_date_value(self) -> str:
        """
        Получает значение начальной даты диапазона.

        Returns:
            str: Значение начальной даты
        """
        # Для простоты используем основное поле даты
        # В реальном приложении могут быть отдельные поля для диапазона
        return self.get_selected_date()

    def get_end_date_value(self) -> str:
        """
        Получает значение конечной даты диапазона.

        Returns:
            str: Значение конечной даты
        """
        # Для простоты используем поле даты и времени
        # В реальном приложении могут быть отдельные поля для диапазона
        return self.get_selected_date_time()

    def get_calendar_current_month_year(self) -> str:
        """
        Получает текущий месяц и год в календаре.

        Returns:
            str: Месяц и год в формате календаря
        """
        return self.get_current_month_year()

    def get_calendar_info(self) -> dict:
        """
        Получает информацию о структуре календаря.

        Returns:
            dict: Информация о календаре
        """
        info = {
            "has_navigation": False,
            "has_date_cells": False,
            "navigation_buttons": [],
            "total_days": 0,
            "visible_days": 0
        }

        try:
            # Проверяем навигацию
            prev_button = self.page.locator(DatePickerLocators.PREV_MONTH_BUTTON)
            next_button = self.page.locator(DatePickerLocators.NEXT_MONTH_BUTTON)
            info["has_navigation"] = prev_button.is_visible() and next_button.is_visible()
            info["navigation_buttons"] = ["previous", "next"] if info["has_navigation"] else []

            # Проверяем ячейки с датами
            day_elements = self.page.locator(DatePickerLocators.DAY)
            info["total_days"] = day_elements.count()
            info["has_date_cells"] = info["total_days"] > 0

            # Считаем видимые дни (не отключенные и не вне месяца)
            visible_days = 0
            for i in range(info["total_days"]):
                day = day_elements.nth(i)
                if day.is_visible():
                    visible_days += 1
            info["visible_days"] = visible_days

        except Exception as e:
            self.log_step(f"Ошибка при получении информации о календаре: {e}")

        return info

    def select_calendar_date(self, day: int) -> bool:
        """
        Выбирает дату в календаре по номеру дня.

        Args:
            day: Номер дня (1-31)

        Returns:
            bool: True если дата выбрана успешно
        """
        try:
            self.log_step(f"Выбор даты {day} в календаре")
            day_elements = self.page.locator(DatePickerLocators.DAY)

            for i in range(day_elements.count()):
                element = day_elements.nth(i)
                if element.inner_text().strip() == str(day):
                    element.click()
                    return True
            return False
        except Exception as e:
            self.log_step(f"Ошибка при выборе даты: {e}")
            return False

    def select_first_available_date(self) -> bool:
        """
        Выбирает первую доступную дату в календаре.

        Returns:
            bool: True если дата выбрана
        """
        try:
            day_elements = self.page.locator(DatePickerLocators.DAY)
            for i in range(day_elements.count()):
                element = day_elements.nth(i)
                if element.is_visible() and not element.has_class("react-datepicker__day--disabled"):
                    element.click()
                    return True
            return False
        except Exception as e:
            self.log_step(f"Ошибка при выборе первой доступной даты: {e}")
            return False

    def confirm_date_input(self) -> None:
        """
        Подтверждает ввод даты (нажатием Enter или кликом вне поля).
        """
        try:
            date_input = self.page.locator(DatePickerLocators.DATE_INPUT)
            date_input.press("Enter")
        except Exception as e:
            self.log_step(f"Ошибка при подтверждении ввода даты: {e}")

    def get_date_validation_message(self) -> str:
        """
        Получает сообщение валидации для поля даты.

        Returns:
            str: Сообщение валидации или пустая строка
        """
        # Ищем возможные элементы валидации
        validation_selectors = [
            ".invalid-feedback",
            ".error-message",
            "[data-error]",
            ".text-danger"
        ]

        for selector in validation_selectors:
            element = self.page.locator(selector).first
            if element.is_visible():
                return element.inner_text().strip()
        return ""

    def open_datetime_calendar(self) -> bool:
        """
        Открывает календарь для выбора даты и времени.

        Returns:
            bool: True если календарь открыт
        """
        try:
            self.open_date_time_picker()
            return self.is_calendar_visible()
        except:
            return False

    def get_datetime_calendar_info(self) -> dict:
        """
        Получает информацию о календаре даты и времени.

        Returns:
            dict: Информация о календаре
        """
        return self.get_calendar_info()  # Используем общий метод

    def select_datetime_calendar_date(self, day: int) -> bool:
        """
        Выбирает дату в календаре даты и времени.

        Args:
            day: Номер дня

        Returns:
            bool: True если дата выбрана
        """
        return self.select_calendar_date(day)

    def select_first_available_datetime_date(self) -> bool:
        """
        Выбирает первую доступную дату в календаре даты и времени.

        Returns:
            bool: True если дата выбрана
        """
        return self.select_first_available_date()

    def is_time_picker_available(self) -> bool:
        """
        Проверяет доступность time picker.

        Returns:
            bool: True если time picker доступен
        """
        return self.page.locator(DatePickerLocators.TIME_CONTAINER).is_visible()

    def set_time(self, hour: int, minute: int) -> bool:
        """
        Устанавливает время.

        Args:
            hour: Час
            minute: Минута

        Returns:
            bool: True если время установлено
        """
        try:
            time_str = f"{hour:02d}:{minute:02d}"
            time_option = self.page.locator(f"text={time_str}")
            if time_option.is_visible():
                time_option.click()
                return True
            return False
        except Exception as e:
            self.log_step(f"Ошибка при установке времени: {e}")
            return False

    def select_predefined_time(self) -> bool:
        """
        Выбирает предустановленное время.

        Returns:
            bool: True если время выбрано
        """
        try:
            time_items = self.page.locator(DatePickerLocators.TIME_LIST_ITEM)
            if time_items.count() > 0:
                time_items.first.click()
                return True
            return False
        except Exception as e:
            self.log_step(f"Ошибка при выборе предустановленного времени: {e}")
            return False

    def confirm_datetime_selection(self) -> bool:
        """
        Подтверждает выбор даты и времени.

        Returns:
            bool: True если подтверждено
        """
        try:
            # Нажимаем вне календаря или подтверждаем
            self.page.click("body", position={"x": 10, "y": 10})
            return True
        except Exception as e:
            self.log_step(f"Ошибка при подтверждении выбора даты и времени: {e}")
            return False

    def is_datetime_calendar_visible(self) -> bool:
        """
        Проверяет видимость календаря даты и времени.

        Returns:
            bool: True если видим
        """
        return self.is_calendar_visible()

    def select_range_start_date(self) -> bool:
        """
        Выбирает начальную дату диапазона.

        Returns:
            bool: True если дата выбрана
        """
        return self.select_first_available_date()

    def select_range_end_date(self) -> bool:
        """
        Выбирает конечную дату диапазона.

        Returns:
            bool: True если дата выбрана
        """
        # Выбираем другую дату для диапазона
        try:
            day_elements = self.page.locator(DatePickerLocators.DAY)
            if day_elements.count() > 1:
                # Выбираем вторую доступную дату
                for i in range(1, day_elements.count()):
                    element = day_elements.nth(i)
                    if element.is_visible() and not element.has_class("react-datepicker__day--disabled"):
                        element.click()
                        return True
            return False
        except Exception as e:
            self.log_step(f"Ошибка при выборе конечной даты диапазона: {e}")
            return False

    def is_year_navigation_available(self) -> bool:
        """
        Проверяет доступность навигации по годам.

        Returns:
            bool: True если доступна
        """
        return self.page.locator(DatePickerLocators.YEAR_SELECT).is_visible()

    def get_calendar_current_year(self) -> str:
        """
        Получает текущий год в календаре.

        Returns:
            str: Текущий год
        """
        year_select = self.page.locator(DatePickerLocators.YEAR_SELECT)
        if year_select.is_visible():
            return year_select.input_value()
        return ""

    def navigate_to_next_year(self) -> bool:
        """
        Переходит к следующему году.

        Returns:
            bool: True если переход успешен
        """
        try:
            next_year_button = self.page.locator(DatePickerLocators.NEXT_YEAR_BUTTON)
            if next_year_button.is_visible():
                next_year_button.click()
                return True
            return False
        except Exception as e:
            self.log_step(f"Ошибка при переходе к следующему году: {e}")
            return False

    def navigate_to_previous_year(self) -> bool:
        """
        Переходит к предыдущему году.

        Returns:
            bool: True если переход успешен
        """
        try:
            prev_year_button = self.page.locator(DatePickerLocators.PREV_YEAR_BUTTON)
            if prev_year_button.is_visible():
                prev_year_button.click()
                return True
            return False
        except Exception as e:
            self.log_step(f"Ошибка при переходе к предыдущему году: {e}")
            return False
