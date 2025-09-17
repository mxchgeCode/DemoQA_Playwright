# tests/test_links_page.py

import pytest
from locators.elements.links_locators import LinksLocators


@pytest.mark.parametrize(
    "link_locator, expected_text",
    [
        (
            LinksLocators.CREATED_LINK,
            "Link has responded with staus 201 and status text Created",
        ),
        (
            LinksLocators.NO_CONTENT_LINK,
            "Link has responded with staus 204 and status text No Content",
        ),
        (
            LinksLocators.MOVED_LINK,
            "Link has responded with staus 301 and status text Moved Permanently",
        ),
        (
            LinksLocators.BAD_REQUEST_LINK,
            "Link has responded with staus 400 and status text Bad Request",
        ),
        (
            LinksLocators.UNAUTHORIZED_LINK,
            "Link has responded with staus 401 and status text Unauthorized",
        ),
        (
            LinksLocators.FORBIDDEN_LINK,
            "Link has responded with staus 403 and status text Forbidden",
        ),
        (
            LinksLocators.NOT_FOUND_LINK,
            "Link has responded with staus 404 and status text Not Found",
        ),
    ],
)
def test_api_response_links(links_page, link_locator, expected_text):
    links_page.click_link_and_check_response(link_locator, expected_text)


def test_click_home_link(links_page):
    # Ожидаем открытие новой вкладки после клика
    with links_page.page.context.expect_page() as new_page_info:
        links_page.click_home_link()  # или другой метод, который кликает по <a id="simpleLink">
    new_page = new_page_info.value
    new_page.wait_for_load_state("domcontentloaded", timeout=10000)
    assert new_page.url == "https://demoqa.com/"  # сравниваем url новой страницы
    new_page.close()


def test_click_home79udw_link(links_page):
    with links_page.page.context.expect_page() as new_page_info:
        links_page.click_home79udw_link()  # кликает по <a id="dynamicLink">
    new_page = new_page_info.value
    new_page.wait_for_load_state("domcontentloaded", timeout=10000)
    assert new_page.url == "https://demoqa.com/"
    new_page.close()
