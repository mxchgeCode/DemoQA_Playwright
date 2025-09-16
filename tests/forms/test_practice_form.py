import pytest


from pages.forms.practice_form_page import AutomationPracticeFormPage
from data import URLs


@pytest.fixture(scope="function")
def form_page(page):
    form = AutomationPracticeFormPage(page)
    form.goto()
    return form


def test_fill_form_and_submit(form_page):
    form_page.fill_first_name("John")
    form_page.fill_last_name("Doe")
    form_page.fill_email("john.doe@example.com")
    form_page.select_gender("Male")
    form_page.fill_mobile("1234567890")
    form_page.fill_date_of_birth("10 Sep 1990")
    form_page.fill_subjects(["Maths", "Physics"])
    form_page.select_hobbies(["Sports", "Music"])
    form_page.upload_picture(URLs.PICTURE_PATH)
    form_page.fill_current_address("123 Main Street")
    form_page.select_state("NCR")
    form_page.select_city("Delhi")
    form_page.submit_form()

    assert form_page.is_modal_visible(), "Ожидался модальный диалог с результатами"
    form_page.close_modal()
