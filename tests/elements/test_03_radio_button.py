import pytest
from locators.elements.radio_button_locators import RadioButtonLocators
from playwright.sync_api import Error


def test_select_yes_radio(radio_button_page):
    radio_button_page.select_yes()
    result = radio_button_page.get_result_text()
    assert result == "Yes"


def test_select_impressive_radio(radio_button_page):
    radio_button_page.select_impressive()
    result = radio_button_page.get_result_text()
    assert result == "Impressive"


def test_select_no_radio_disabled(radio_button_page):
    with pytest.raises(Error):
        radio_button_page.select_no()
    # Проверка, что результат не отображается
    assert not radio_button_page.page.locator(
        RadioButtonLocators.RESULT_TEXT
    ).is_visible()
