import time

import pytest
from pages.elements.check_box_page import CheckboxPage

@pytest.fixture(scope="function")
def checkbox_page(page):
    page_obj = CheckboxPage(page)
    page_obj.open()
    return page_obj

def test_check_home_checkbox(checkbox_page: CheckboxPage):
    checkbox_page.expand_all()
    checkbox_page.check_home()
    result = checkbox_page.get_result_text()
    assert "home" in result.lower()
    assert "desktop" in result.lower()
    assert "documents" in result.lower()
    assert "downloads" in result.lower()

def test_collapse_all_checkbox(checkbox_page: CheckboxPage):
    checkbox_page.expand_all()
    checkbox_page.collapse_all()
    assert checkbox_page.is_result_hidden_or_empty(), "Результат должен быть скрыт или пуст после сворачивания"


