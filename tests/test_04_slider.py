def test_slider_default_value(slider_page):
    """Проверка значения слайдера по умолчанию."""
    assert (
        slider_page.get_current_value() == "25"
    ), "Значение по умолчанию должно быть 25"


def test_slider_move_to_max(slider_page):
    slider_page.move_to_max()
    assert slider_page.get_current_value() == "100"


def test_slider_move_to_min(slider_page):
    slider_page.move_to_min()
    assert slider_page.get_current_value() == "0"


def test_slider_set_specific_value(slider_page):
    slider_page.set_value(75)
    assert slider_page.get_current_value() == "75"


def test_slider_move_to_middle(slider_page):
    slider_page.move_to_middle()
    slider_page.page.wait_for_timeout(500)
    assert slider_page.get_current_value() == "50"


def test_slider_keyboard_navigation(slider_page):
    initial = int(slider_page.get_current_value())
    slider_page.focus_and_press_arrow_right()
    slider_page.page.wait_for_timeout(500)
    increased = int(slider_page.get_current_value())
    assert increased > initial, "Значение должно увеличиться"

    slider_page.focus_and_press_arrow_left()
    slider_page.page.wait_for_timeout(500)
    decreased = int(slider_page.get_current_value())
    assert decreased in (
        initial,
        initial - 1,
    ), "Значение должно уменьшиться или остаться прежним"
