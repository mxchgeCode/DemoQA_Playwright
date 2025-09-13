from playwright.sync_api import Page
from locators.date_picker_locators import DatePickerLocators
from datetime import datetime


class DatePickerPage:
    def __init__(self, page: Page):
        self.page = page
        # Date input elements
        self.date_input = page.locator(DatePickerLocators.DATE_INPUT)
        self.date_time_input = page.locator(DatePickerLocators.DATE_TIME_INPUT)

        # Calendar elements
        self.calendar_popup = page.locator(DatePickerLocators.CALENDAR_POPUP)
        self.calendar_month_select = page.locator(
            DatePickerLocators.CALENDAR_MONTH_SELECT
        )
        self.calendar_year_select = page.locator(
            DatePickerLocators.CALENDAR_YEAR_SELECT
        )
        self.calendar_next_month_button = page.locator(
            DatePickerLocators.CALENDAR_NEXT_MONTH_BUTTON
        )
        self.calendar_prev_month_button = page.locator(
            DatePickerLocators.CALENDAR_PREV_MONTH_BUTTON
        )

        # Calendar days
        self.calendar_days = page.locator(DatePickerLocators.CALENDAR_DAY)
        self.calendar_selected_day = page.locator(
            DatePickerLocators.CALENDAR_DAY_SELECTED
        )
        self.calendar_today = page.locator(DatePickerLocators.CALENDAR_DAY_TODAY)

        # Time picker elements
        self.time_picker_list = page.locator(DatePickerLocators.TIME_PICKER_LIST)
        self.time_picker_items = page.locator(DatePickerLocators.TIME_PICKER_ITEM)
        self.time_picker_selected = page.locator(
            DatePickerLocators.TIME_PICKER_ITEM_SELECTED
        )

    def click_date_input(self):
        """Клик по полю выбора даты."""
        self.date_input.click()
        self.page.wait_for_timeout(1000)

    def click_date_time_input(self):
        """Клик по полю выбора даты и времени."""
        # Исправлено: Если календарь открыт, сначала кликаем вне его, чтобы закрыть
        if self.is_calendar_visible():
            print("~ Календарь уже открыт, закрываем перед кликом по полю ввода...")
            # Кликаем в левый верхний угол страницы, чтобы закрыть календарь
            self.page.mouse.click(10, 10)
            self.page.wait_for_timeout(500)  # Короткая пауза

        # Теперь кликаем по полю ввода
        self.date_time_input.click()
        self.page.wait_for_timeout(1000)

    def select_date_by_day(self, day: int):
        """Выбирает дату по номеру дня в текущем месяце."""
        # Кликаем по полю даты, если календарь не открыт
        if not self.is_calendar_visible():
            self.click_date_input()

        # Ждем появления календаря
        self.wait_for_calendar()

        # Находим и кликаем по нужному дню
        day_locator = self.page.locator(
            f"{DatePickerLocators.CALENDAR_DAY}:has-text('{day}')"
        )
        if day_locator.count() > 0:
            day_locator.first.click()
        else:
            # Если точное совпадение не найдено, ищем по номеру
            day_elements = self.calendar_days
            for i in range(day_elements.count()):
                day_element = day_elements.nth(i)
                if day_element.is_visible():
                    day_text = day_element.text_content().strip()
                    if day_text.isdigit() and int(day_text) == day:
                        day_element.click()
                        break

        self.page.wait_for_timeout(1000)

    def select_today(self):
        """Выбирает сегодняшнюю дату."""
        self.click_date_input()
        self.wait_for_calendar()

        if self.calendar_today.is_visible():
            self.calendar_today.click()
        self.page.wait_for_timeout(1000)

    def navigate_to_next_month(self):
        """Переходит к следующему месяцу в календаре."""
        if self.is_calendar_visible():
            self.calendar_next_month_button.click()
        self.page.wait_for_timeout(1000)

    def navigate_to_prev_month(self):
        """Переходит к предыдущему месяцу в календаре."""
        if self.is_calendar_visible():
            self.calendar_prev_month_button.click()
        self.page.wait_for_timeout(1000)

    def select_month(self, month: str):
        """Выбирает месяц из dropdown."""
        if self.is_calendar_visible():
            self.calendar_month_select.select_option(month)
        self.page.wait_for_timeout(1000)

    def select_year(self, year: str):
        """Выбирает год из dropdown."""
        if self.is_calendar_visible():
            self.calendar_year_select.select_option(year)
        self.page.wait_for_timeout(1000)

    def get_selected_date(self) -> str:
        """Получает выбранную дату из поля ввода."""
        return self.date_input.input_value().strip()

    def get_selected_date_time(self) -> str:
        """Получает выбранную дату и время из поля ввода."""
        return self.date_time_input.input_value().strip()

    def is_calendar_visible(self) -> bool:
        """Проверяет, виден ли календарь."""
        try:
            return self.calendar_popup.is_visible()
        except:
            return False

    def wait_for_calendar(self, timeout: int = 5000):
        """Ждет появления календаря."""
        try:
            self.calendar_popup.wait_for(state="visible", timeout=timeout)
            return True
        except:
            return False

    def wait_for_calendar_hidden(self, timeout: int = 5000):
        """Ждет скрытия календаря."""
        try:
            self.calendar_popup.wait_for(state="hidden", timeout=timeout)
            return True
        except:
            return False

    def select_time(self, time_text: str):
        """Выбирает время из списка."""
        self.click_date_time_input()
        self.wait_for_calendar()

        # Ищем элемент времени и кликаем по нему
        time_item = self.page.locator(
            f"{DatePickerLocators.TIME_PICKER_ITEM}:has-text('{time_text}')"
        )
        if time_item.count() > 0:
            time_item.first.click()
        self.page.wait_for_timeout(1000)

    def get_calendar_month(self) -> str:
        """Получает текущий месяц из календаря."""
        if self.is_calendar_visible():
            return self.calendar_month_select.input_value()
        return ""

    def get_calendar_year(self) -> str:
        """Получает текущий год из календаря."""
        if self.is_calendar_visible():
            return self.calendar_year_select.input_value()
        return ""

    def get_available_dates_count(self) -> int:
        """Получает количество доступных дат в календаре."""
        if self.is_calendar_visible():
            return self.calendar_days.count()
        return 0

    def get_today_date_formatted(self) -> str:
        """Получает сегодняшнюю дату в формате MM/dd/yyyy."""
        today = datetime.now()
        return today.strftime("%m/%d/%Y")
