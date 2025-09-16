def test_auto_complete_elements_exist(autocomplete_page):
    autocomplete_page.page.wait_for_timeout(500)
    assert (
        "auto-complete" in autocomplete_page.page.url
    ), "URL страницы должен содержать 'auto-complete'"
    assert (
        autocomplete_page.single_color_input.is_visible()
    ), "Поле single input должно быть видно"
    assert (
        autocomplete_page.multi_color_input.is_visible()
    ), "Поле multi input должно быть видно"


def test_auto_complete_multi_input_selection(autocomplete_page):
    for color in ["Blue", "Green"]:
        autocomplete_page.fill_multiple_colors(color)
    values = autocomplete_page.get_multi_color_values_correctly()
    assert len(values) > 1, "Список выбранных значений не должен быть пустым"


def test_auto_complete_single_input_selection(autocomplete_page):
    autocomplete_page.fill_single_color("Red")
    selected_value = autocomplete_page.get_single_color_value_correctly()
    assert len(selected_value) > 0, "Выбранное значение не должно быть пустым"
