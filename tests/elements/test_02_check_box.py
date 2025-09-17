def test_check_home_checkbox(check_box_page):
    check_box_page.expand_all()
    check_box_page.check_home()
    result = check_box_page.get_result_text()
    assert "home" in result.lower()
    assert "desktop" in result.lower()
    assert "documents" in result.lower()
    assert "downloads" in result.lower()


def test_collapse_all_checkbox(check_box_page):
    check_box_page.expand_all()
    check_box_page.collapse_all()
    assert (
        check_box_page.is_result_hidden_or_empty()
    ), "Результат должен быть скрыт или пуст после сворачивания"
