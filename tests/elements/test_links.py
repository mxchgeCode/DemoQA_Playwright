import pytest
from data import URLs


@pytest.mark.parametrize(
    "click_method, expected_text",
    [
        ("click_created_link", "Created"),
        ("click_no_content_link", "No Content"),
        ("click_moved_link", "Moved"),
        ("click_bad_request_link", "Bad Request"),
        ("click_unauthorized_link", "Unauthorized"),
        ("click_forbidden_link", "Forbidden"),
        ("click_not_found_link", "Not Found"),
    ],
)
def test_click_api_links(links_page, click_method, expected_text):
    links_page.page.goto(URLs.LINKS_PAGE)  # возврат на страницу
    getattr(links_page, click_method)()
    response_text = links_page.get_link_response_text()
    assert expected_text in response_text


def test_click_home_link(links_page):
    with links_page.page.context.expect_page() as new_page_info:
        links_page.click_home_link()
    new_page = new_page_info.value
    new_page.wait_for_load_state()
    assert new_page.url == "https://demoqa.com/"
    new_page.close()


def test_click_home79udw_link(links_page):
    with links_page.page.context.expect_page() as new_page_info:
        links_page.click_home79udw_link()
    new_page = new_page_info.value
    new_page.wait_for_load_state()
    assert new_page.url == "https://demoqa.com/"
    new_page.close()
