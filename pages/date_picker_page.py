from playwright.sync_api import Page
from locators.date_picker_locators import DatePickerLocators
from datetime import datetime


class DatePickerPage:
    def __init__(self, page: Page):
        self.page = page
        self.date_input = page.locator(DatePickerLocators.DATE_INPUT)
        self.date_time_input = page.locator(DatePickerLocators.DATE_TIME_INPUT)
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
        self.calendar_days = page.locator(DatePickerLocators.CALENDAR_DAY)
        self.calendar_selected_day = page.locator(
            DatePickerLocators.CALENDAR_DAY_SELECTED
        )
        self.calendar_today = page.locator(DatePickerLocators.CALENDAR_DAY_TODAY)
        self.time_picker_list = page.locator(DatePickerLocators.TIME_PICKER_LIST)
        self.time_picker_items = page.locator(DatePickerLocators.TIME_PICKER_ITEM)
        self.time_picker_selected = page.locator(
            DatePickerLocators.TIME_PICKER_ITEM_SELECTED
        )

    def click_date_input(self):
        self.date_input.click()
        self.page.wait_for_timeout(1000)

    def click_date_time_input(self):
        if self.is_calendar_visible():
            self.page.mouse.click(10, 10)
            self.page.wait_for_timeout(500)
        self.date_time_input.click()
        self.page.wait_for_timeout(1000)

    def select_date_by_day(self, day: int):
        if not self.is_calendar_visible():
            self.click_date_input()
        self.wait_for_calendar()
        day_locator = self.page.locator(
            f"{DatePickerLocators.CALENDAR_DAY}:has-text('{day}')"
        )
        if day_locator.count() > 0:
            day_locator.first.click()
        else:
            for i in range(self.calendar_days.count()):
                day_el = self.calendar_days.nth(i)
                if day_el.is_visible():
                    day_text = day_el.text_content().strip()
                    if day_text.isdigit() and int(day_text) == day:
                        day_el.click()
                        break
        self.page.wait_for_timeout(1000)

    def select_today(self):
        self.click_date_input()
        self.wait_for_calendar()
        if self.calendar_today.is_visible():
            self.calendar_today.click()
        self.page.wait_for_timeout(1000)

    def navigate_to_next_month(self):
        if self.is_calendar_visible():
            self.calendar_next_month_button.click()
        self.page.wait_for_timeout(1000)

    def navigate_to_prev_month(self):
        if self.is_calendar_visible():
            self.calendar_prev_month_button.click()
        self.page.wait_for_timeout(1000)

    def select_month(self, month: str):
        if self.is_calendar_visible():
            self.calendar_month_select.select_option(month)
        self.page.wait_for_timeout(1000)

    def select_year(self, year: str):
        if self.is_calendar_visible():
            self.calendar_year_select.select_option(year)
        self.page.wait_for_timeout(1000)

    def get_selected_date(self) -> str:
        return self.date_input.input_value().strip()

    def get_selected_date_time(self) -> str:
        return self.date_time_input.input_value().strip()

    def is_calendar_visible(self) -> bool:
        try:
            return self.calendar_popup.is_visible()
        except:
            return False

    def wait_for_calendar(self, timeout: int = 5000):
        try:
            self.calendar_popup.wait_for(state="visible", timeout=timeout)
            return True
        except:
            return False

    def wait_for_calendar_hidden(self, timeout: int = 5000):
        try:
            self.calendar_popup.wait_for(state="hidden", timeout=timeout)
            return True
        except:
            return False

    def select_time(self, time_text: str):
        self.click_date_time_input()
        self.wait_for_calendar()
        time_item = self.page.locator(
            f"{DatePickerLocators.TIME_PICKER_ITEM}:has-text('{time_text}')"
        )
        if time_item.count() > 0:
            time_item.first.click()
        self.page.wait_for_timeout(1000)

    def get_calendar_month(self) -> str:
        if self.is_calendar_visible():
            return self.calendar_month_select.input_value()
        return ""

    def get_calendar_year(self) -> str:
        if self.is_calendar_visible():
            return self.calendar_year_select.input_value()
        return ""

    def get_available_dates_count(self) -> int:
        if self.is_calendar_visible():
            return self.calendar_days.count()
        return 0

    def get_today_date_formatted(self) -> str:
        today = datetime.now()
        return today.strftime("%m/%d/%Y")
