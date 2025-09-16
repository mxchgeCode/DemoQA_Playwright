import pytest
from pages.elements.buttons_page import ButtonsPage


@pytest.fixture(scope="function")
def buttons_page(page):
    bp = ButtonsPage(page)
    bp.open()
    return bp


def test_double_click_button(buttons_page: ButtonsPage):
    buttons_page.double_click_button()
    assert buttons_page.get_double_click_message() == "You have done a double click"


def test_right_click_button(buttons_page: ButtonsPage):
    buttons_page.right_click_button()
    assert buttons_page.get_right_click_message() == "You have done a right click"


def test_dynamic_click_button(buttons_page: ButtonsPage):
    buttons_page.click_me_button()
    assert buttons_page.get_click_me_message() == "You have done a dynamic click"
