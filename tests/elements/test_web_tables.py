import time

import pytest
from pages.elements.web_tables_page import WebTablesPage
from locators.elements.web_tables_locators import WebTablesLocators


@pytest.fixture(scope="function")
def webtables_page(page):
    wtp = WebTablesPage(page)
    wtp.open()
    return wtp


def test_add_and_search_row(webtables_page: WebTablesPage):
    webtables_page.click_add()
    webtables_page.fill_form(
        "John", "Doe", "john.doe@example.com", 28, 50000, "Engineering"
    )
    webtables_page.submit_form()
    rows = webtables_page.page.locator(
        ".rt-tr-group .rt-td:nth-child(4)"
    )  # 4-й столбец - Email
    count = rows.count()
    assert count > 3, "Добавленная запись должна отображаться в таблице"


def test_delete_row(webtables_page: WebTablesPage):
    webtables_page.search("Cierra")

    rows_before = webtables_page.page.locator(WebTablesLocators.DELETE_ROW).filter(
        has_text="Cierra"
    )

    if rows_before.count() > 0:
        webtables_page.page.locator("span[title='Delete']").first.click()

        # Ждём, что строка с "Cierra" исчезнет из DOM
        webtables_page.page.locator(WebTablesLocators.DELETE_ROW).filter(
            has_text="Cierra"
        ).wait_for(state="detached")

        webtables_page.search("Cierra")
        rows_after = rows_before = (
            webtables_page.page.locator(WebTablesLocators.DELETE_ROW)
            .filter(has_text="Cierra")
            .count()
        )
        assert rows_after < rows_before, "Запись должна быть удалена"
