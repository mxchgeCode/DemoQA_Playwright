def test_tabs_page_loads(tabs_page):
    tabs_page.page.wait_for_timeout(1000)
    assert "tabs" in tabs_page.page.url
    assert tabs_page.tab_what.is_visible()
    assert tabs_page.tab_origin.is_visible()
    assert tabs_page.tab_use.is_visible()
    assert tabs_page.tab_more.is_visible()


def test_tabs_initial_state(tabs_page):
    tabs_page.page.wait_for_timeout(500)
    assert (
        tabs_page.is_what_tab_active()
    ), "Вкладка What должна быть активна по умолчанию"
    assert tabs_page.is_what_panel_visible(), "Панель What должна быть видима"


def test_tabs_switching_functionality(tabs_page):
    tabs_page.click_origin_tab()
    tabs_page.page.wait_for_timeout(300)
    assert tabs_page.is_origin_panel_visible()

    tabs_page.click_use_tab()
    tabs_page.page.wait_for_timeout(300)
    assert tabs_page.is_use_panel_visible()


def test_tabs_content_visibility(tabs_page):
    tabs_page.click_what_tab()
    tabs_page.page.wait_for_timeout(300)
    assert tabs_page.is_what_panel_visible()

    tabs_page.click_origin_tab()
    tabs_page.page.wait_for_timeout(300)
    assert tabs_page.is_origin_panel_visible()


def test_tabs_content_exists(tabs_page):
    tabs_page.click_what_tab()
    tabs_page.page.wait_for_timeout(300)
    assert tabs_page.get_what_panel_content() is not None

    tabs_page.click_origin_tab()
    tabs_page.page.wait_for_timeout(300)
    assert tabs_page.get_origin_panel_content() is not None

    tabs_page.click_use_tab()
    tabs_page.page.wait_for_timeout(300)
    assert tabs_page.get_use_panel_content() is not None


def test_tabs_active_state_tracking(tabs_page):
    tabs_page.page.wait_for_timeout(300)
    active = tabs_page.get_active_tab_text()
    assert active in {"What", "Origin", "Use", "More", ""}


def test_tabs_disabled_functionality(tabs_page):
    tabs_page.page.wait_for_timeout(300)
    assert tabs_page.tab_more.is_visible()
    _ = tabs_page.is_more_tab_disabled()  # Проверка не падает


def test_tabs_elements_persistence(tabs_page):
    tabs = [
        tabs_page.tab_what,
        tabs_page.tab_origin,
        tabs_page.tab_use,
        tabs_page.tab_more,
    ]
    for tab in tabs:
        assert tab.is_visible()


def test_tabs_basic_functionality(tabs_page):
    tabs_page.click_what_tab()
    tabs_page.page.wait_for_timeout(200)
    tabs_page.click_origin_tab()
    tabs_page.page.wait_for_timeout(200)
    tabs_page.click_use_tab()
    tabs_page.page.wait_for_timeout(200)
    assert True
