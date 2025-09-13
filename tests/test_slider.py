def test_slider_default_value(slider_page):
    """
    Тест: проверяет начальное значение слайдера.
    Внимание: Сайт demoqa.com по умолчанию устанавливает value="25",
    НЕсмотря на документацию, которая говорит "50".
    Это известный баг/особенность сайта.
    """

    assert slider_page.get_current_value() == "25", "Значение по умолчанию не равно 25"


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
    """Тест: перемещение слайдера в середину."""
    slider_page.move_to_middle()
    # Добавлена задержка 2 секунды для визуального наблюдения
    slider_page.page.wait_for_timeout(2000)
    assert slider_page.get_current_value() == "50"


def test_slider_keyboard_navigation(slider_page):
    """Тест: навигация слайдера с помощью клавиатуры."""
    initial_value = int(slider_page.get_current_value())

    # Увеличиваем значение
    slider_page.focus_and_press_arrow_right()
    # Добавлена задержка 2 секунды для визуального наблюдения
    slider_page.page.wait_for_timeout(2000)
    new_value = int(slider_page.get_current_value())
    assert new_value > initial_value

    # Уменьшаем значение
    slider_page.focus_and_press_arrow_left()
    # Добавлена задержка 2 секунды для визуального наблюдения
    slider_page.page.wait_for_timeout(2000)
    final_value = int(slider_page.get_current_value())
    assert final_value == initial_value or final_value == initial_value - 1

