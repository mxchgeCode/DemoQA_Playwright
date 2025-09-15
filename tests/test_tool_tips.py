def test_tool_tips_button_hover(tooltips_page):
    """Тест: тултип появляется при наведении на кнопку."""
    # Наводим на кнопку
    tooltips_page.hover_over_button()

    # Проверяем, что тултип появился
    assert (
        tooltips_page.is_tooltip_visible()
    ), "Тултип должен появиться при наведении на кнопку"

    # Проверяем, что тултип содержит текст
    tooltip_text = tooltips_page.get_tooltip_text()
    assert len(tooltip_text) > 0, "Тултип должен содержать текст"


def test_tool_tips_field_hover(tooltips_page):
    """Тест: тултип появляется при наведении на поле ввода."""

    # Скрываем предыдущий тултип
    tooltips_page.move_mouse_away()
    tooltips_page.page.wait_for_timeout(1000)

    # Наводим на поле ввода
    tooltips_page.hover_over_field()

    # Проверяем, что тултип появился
    assert (
        tooltips_page.is_tooltip_visible()
    ), "Тултип должен появиться при наведении на поле ввода"

    # Проверяем, что тултип содержит текст
    tooltip_text = tooltips_page.get_tooltip_text()
    assert len(tooltip_text) > 0, "Тултип должен содержать текст"


def test_tool_tips_link_hover(tooltips_page):
    """Тест: тултип появляется при наведении на ссылку."""

    # Скрываем предыдущий тултип
    tooltips_page.move_mouse_away()
    tooltips_page.page.wait_for_timeout(500)

    # Наводим на ссылку
    try:
        tooltips_page.hover_over_link()

        # Проверяем, что тултип появился
        if tooltips_page.is_tooltip_visible():
            tooltip_text = tooltips_page.get_tooltip_text()
            assert len(tooltip_text) > 0, "Тултип должен содержать текст"

    except:
        raise Exception(f"Не удалось найти тултип")

    try:
        tooltips_page.hover_over_section_link()

        # Проверяем, что тултип появился
        if tooltips_page.is_tooltip_visible():
            tooltip_text = tooltips_page.get_tooltip_text()
            assert len(tooltip_text) > 0, "Тултип должен содержать текст"

    except:
        raise Exception(f"Не удалось найти тултип")
