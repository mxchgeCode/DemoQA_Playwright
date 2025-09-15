def test_tool_tips_button_hover(tooltips_page):
    tooltips_page.hover_over_button()
    assert tooltips_page.is_tooltip_visible()
    text = tooltips_page.get_tooltip_text()
    assert len(text) > 0


def test_tool_tips_field_hover(tooltips_page):
    tooltips_page.move_mouse_away()
    tooltips_page.page.wait_for_timeout(500)
    tooltips_page.hover_over_field()
    assert tooltips_page.is_tooltip_visible()
    text = tooltips_page.get_tooltip_text()
    assert len(text) > 0


def test_tool_tips_link_hover(tooltips_page):
    tooltips_page.move_mouse_away()
    tooltips_page.page.wait_for_timeout(500)

    tooltips_page.hover_over_link()
    if tooltips_page.is_tooltip_visible():
        text = tooltips_page.get_tooltip_text()
        assert len(text) > 0

    tooltips_page.hover_over_section_link()
    if tooltips_page.is_tooltip_visible():
        text = tooltips_page.get_tooltip_text()
        assert len(text) > 0
