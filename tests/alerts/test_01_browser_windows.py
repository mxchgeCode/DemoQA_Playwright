import pytest


@pytest.mark.parametrize(
    "button_method", ["click_new_tab", "click_new_window", "click_new_window_message"]
)
def test_open_new_window_or_tab(browser_windows_page, button_method):
    with browser_windows_page.page.context.expect_page() as new_page_info:
        getattr(browser_windows_page, button_method)()
    new_page = new_page_info.value
    new_page.wait_for_load_state()

    if button_method == "click_new_window_message":
        content = new_page.locator("body").text_content()
        assert "Knowledge increases" in content
    else:
        assert new_page.url != browser_windows_page.page.url
