import pytest
from pages.elements.radio_button_page import RadioButtonPage
from locators.elements.radio_button_locators import RadioButtonLocators
from playwright.sync_api import Error

@pytest.fixture(scope="function")
def radio_page(page):
    rb_page = RadioButtonPage(page)
    rb_page.open()
    return rb_page

def test_select_yes_radio(radio_page: RadioButtonPage):
    radio_page.select_yes()
    result = radio_page.get_result_text()
    assert result == "Yes"

def test_select_impressive_radio(radio_page: RadioButtonPage):
    radio_page.select_impressive()
    result = radio_page.get_result_text()
    assert result == "Impressive"

def test_select_no_radio_disabled(radio_page: RadioButtonPage):
    with pytest.raises(Error):
        radio_page.select_no()
    # Проверка, что результат не отображается
    assert not radio_page.page.locator(RadioButtonLocators.RESULT_TEXT).is_visible()
