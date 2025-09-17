import time


from playwright.sync_api import Page
from locators.forms.practice_form_locators import AutomationPracticeFormLocators
from data import URLs


class AutomationPracticeFormPage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self):
        self.page.goto(URLs.PRACTICE_FORM)
        self.page.wait_for_selector(AutomationPracticeFormLocators.FORM_CONTAINER)

    def fill_first_name(self, first_name: str):
        self.page.fill(AutomationPracticeFormLocators.FIRST_NAME_INPUT, first_name)

    def fill_last_name(self, last_name: str):
        self.page.fill(AutomationPracticeFormLocators.LAST_NAME_INPUT, last_name)

    def fill_email(self, email: str):
        self.page.fill(AutomationPracticeFormLocators.EMAIL_INPUT, email)

    def select_gender(self, gender_value: str):
        # по значению Gender=Male, Female, Other находим id input и кликаем по label с for= этому id
        inputs = self.page.locator("input[name='gender']")
        count = inputs.count()
        for i in range(count):
            val = inputs.nth(i).get_attribute("value")
            if val == gender_value:
                input_id = inputs.nth(i).get_attribute("id")
                label_locator = self.page.locator(f"label[for='{input_id}']")
                label_locator.click()
                break

    def fill_mobile(self, mobile: str):
        self.page.fill(AutomationPracticeFormLocators.MOBILE_INPUT, mobile)

    def fill_date_of_birth(self, date_str: str):
        # date_str = "10 Sep 1990" - поле открывается кликом и можно вводить текст
        self.page.click(AutomationPracticeFormLocators.DATE_OF_BIRTH_INPUT)
        self.page.fill(AutomationPracticeFormLocators.DATE_OF_BIRTH_INPUT, date_str)
        self.page.keyboard.press("Enter")

    def fill_subjects(self, subjects: list[str]):
        subj_input = self.page.locator(AutomationPracticeFormLocators.SUBJECTS_INPUT)
        for subj in subjects:
            subj_input.fill(subj)
            self.page.wait_for_selector(".subjects-auto-complete__menu", timeout=7000)
            option = self.page.locator(
                f"div.subjects-auto-complete__option", has_text=subj
            )
            option.wait_for(state="visible", timeout=7000)
            element = option.element_handle()
            if element:
                self.page.evaluate("(el) => el.click()", element)
                self.page.wait_for_timeout(200)
            else:
                raise Exception(f"Option '{subj}' not found in autocomplete")

    def select_hobbies(self, hobbies: list[str]):
        # Получаем все чекбоксы input[name='hobbies-checkbox-X']
        checkboxes = self.page.locator("input[type='checkbox'].custom-control-input")
        count = checkboxes.count()
        for i in range(count):
            input_el = checkboxes.nth(i)
            input_id = input_el.get_attribute("id")
            label_locator = self.page.locator(f"label[for='{input_id}']")
            label_text = label_locator.text_content().strip()
            if label_text in hobbies:
                label_locator = self.page.locator(f"label[for='{input_id}']")
                label_locator.wait_for(state="visible", timeout=5000)
                label_locator.click()

    def upload_picture(self, filepath: str):
        self.page.set_input_files(
            AutomationPracticeFormLocators.PICTURE_UPLOAD_INPUT, filepath
        )

    def fill_current_address(self, address: str):
        self.page.fill(AutomationPracticeFormLocators.CURRENT_ADDRESS_TEXTAREA, address)

    def select_state(self, state_name: str):
        # Клик по контейнеру, чтобы раскрыть список
        self.page.locator("#state").click()
        # Ввод значения в скрытый input
        input_locator = self.page.locator("#react-select-3-input")
        input_locator.fill(state_name)
        # Явное ожидание появления опции с точным текстом state_name
        option_locator = self.page.locator(
            f"div.css-1n7v3ny-option:has-text('{state_name}')"
        )
        option_locator.wait_for(state="visible", timeout=5000)
        option_locator.click()

    def select_city(self, city_name: str):
        # Клик по контейнеру, чтобы раскрыть список
        self.page.locator("#city").click()
        # Ввод значения в скрытый input
        input_locator = self.page.locator("#react-select-4-input")
        input_locator.fill(city_name)
        # Явное ожидание появления опции с точным текстом
        option_locator = self.page.locator(
            f"div.css-1n7v3ny-option:has-text('{city_name}')"
        )
        option_locator.wait_for(state="visible", timeout=5000)
        option_locator.click()
        time.sleep(3)

    def submit_form(self):
        self.page.click(AutomationPracticeFormLocators.SUBMIT_BUTTON)

    def is_modal_visible(self):
        try:
            self.page.locator(AutomationPracticeFormLocators.MODAL_DIALOG).wait_for(
                state="visible", timeout=5000
            )
            return True
        except TimeoutError:
            return False

    def close_modal(self):
        close_btn = self.page.locator("#closeLargeModal")
        close_btn.wait_for(state="visible", timeout=5000)
        close_btn.click()
