import time

import pytest
from pages.elements.text_box_page import TextBoxPage


@pytest.fixture(scope="function")
def text_box_page(page):
    tb_page = TextBoxPage(page)
    tb_page.open()
    return tb_page


def test_fill_form_and_submit(text_box_page: TextBoxPage):
    text_box_page.fill_user_name("John Doe")
    text_box_page.fill_user_email("john.doe@example.com")
    text_box_page.fill_current_address("123 Main St")
    text_box_page.fill_permanent_address("456 Park Ave")
    text_box_page.submit()

    assert "John Doe" in text_box_page.get_output_name()
    assert "john.doe@example.com" in text_box_page.get_output_email()
    assert "123 Main St" in text_box_page.get_output_current_address()
    assert "456 Park Ave" in text_box_page.get_output_permanent_address()
