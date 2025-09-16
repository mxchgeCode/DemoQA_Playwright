from playwright.sync_api import Page
from locators.elements.web_tables_locators import WebTablesLocators
from data import URLs


class WebTablesPage:
    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto(URLs.WEB_TABLES)

    def click_add(self):
        self.page.click(WebTablesLocators.ADD_BUTTON)

    def fill_form(self, first_name, last_name, email, age, salary, department):
        self.page.fill(WebTablesLocators.FIRST_NAME_INPUT, first_name)
        self.page.fill(WebTablesLocators.LAST_NAME_INPUT, last_name)
        self.page.fill(WebTablesLocators.EMAIL_INPUT, email)
        self.page.fill(WebTablesLocators.AGE_INPUT, str(age))
        self.page.fill(WebTablesLocators.SALARY_INPUT, str(salary))
        self.page.fill(WebTablesLocators.DEPARTMENT_INPUT, department)

    def submit_form(self):
        self.page.click(WebTablesLocators.SUBMIT_BUTTON)

    def search(self, text):
        self.page.fill(WebTablesLocators.SEARCH_BOX, text)

    def get_table_rows_count(self):
        return self.page.locator(WebTablesLocators.TABLE_ROWS).count()

    def get_visible_table_rows_count(self):
        return (
            self.page.locator(".rt-tr-group")
            .filter(has=self.page.locator("div.rt-td"))
            .count()
        )
