from locators.elements.dynamic_locators import DynamicPropertiesLocators


def test_enable_after_button(dynamic_properties_page):
    # Проверяем, что кнопка disables или enabled динамически
    initially_enabled = dynamic_properties_page.is_enable_after_enabled()
    if not initially_enabled:
        assert dynamic_properties_page.wait_and_check_enable_after()
    else:
        assert initially_enabled


def test_visible_after_button(dynamic_properties_page):
    initially_visible = dynamic_properties_page.page.locator(
        DynamicPropertiesLocators.VISIBLE_AFTER_BUTTON
    ).is_visible()
    if not initially_visible:
        assert dynamic_properties_page.is_visible_after_visible()
    else:
        assert initially_visible


def test_color_change_button(dynamic_properties_page):
    assert (
        dynamic_properties_page.wait_for_text_color_change()
    ), "Цвет текста кнопки не изменился"
