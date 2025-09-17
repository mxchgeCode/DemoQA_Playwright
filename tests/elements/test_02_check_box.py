def test_check_home_checkbox(check_box_page):
    check_box_page.expand_all()
    check_box_page.check_home()
    result = check_box_page.get_result_text()
    assert "home" in result.lower()
    assert "desktop" in result.lower()
    assert "documents" in result.lower()
    assert "downloads" in result.lower()


def test_collapse_all_checkbox(check_box_page):
    print("Test started: expand all checkboxes")
    check_box_page.expand_all()
    print("All checkboxes expanded")
    check_box_page.collapse_all()
    print("All checkboxes collapsed")
    result_hidden_or_empty = check_box_page.is_result_hidden_or_empty()
    print(f"Result hidden or empty: {result_hidden_or_empty}")
    assert (
        result_hidden_or_empty
    ), "Результат должен быть скрыт или пуст после сворачивания"
    print("Test finished successfully")
