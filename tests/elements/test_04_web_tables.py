import time

from locators.elements.web_tables_locators import WebTablesLocators


def test_add_and_search_row(web_tables_page):
    web_tables_page.click_add()
    web_tables_page.fill_form(
        "John", "Doe", "john.doe@example.com", 28, 50000, "Engineering"
    )
    web_tables_page.submit_form()
    rows = web_tables_page.page.locator(
        ".rt-tr-group .rt-td:nth-child(4)"
    )  # 4-й столбец - Email
    count = rows.count()
    assert count > 3, "Добавленная запись должна отображаться в таблице"


def test_delete_row(web_tables_page):
    web_tables_page.search("Cierra")
    rows_before = (
        web_tables_page.page.locator(WebTablesLocators.DELETE_ROW)
        .filter(has_text="Cierra")
        .count()
    )

    web_tables_page.page.locator("span[title='Delete']").first.click()
    # Ждём, что строка с "Cierra" исчезнет из DOM
    web_tables_page.page.locator(WebTablesLocators.DELETE_ROW).filter(
        has_text="Cierra"
    ).wait_for(state="detached")
    time.sleep(2)

    web_tables_page.search("Cierra")
    rows_after = (
        web_tables_page.page.locator(WebTablesLocators.DELETE_ROW)
        .filter(has_text="Cierra")
        .count()
    )

    assert rows_after < rows_before, "Запись должна быть удалена"
