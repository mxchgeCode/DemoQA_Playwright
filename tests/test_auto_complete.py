# tests/test_auto_complete.py
def test_auto_complete_elements_exist(autocomplete_page):
    """Тест: необходимые элементы существуют."""
    # Даем время странице загрузиться
    autocomplete_page.page.wait_for_timeout(1000)

    current_url = autocomplete_page.page.url
    assert (
        "auto-complete" in current_url
    ), "Страница должна содержать 'auto-complete' в URL"

    # Проверяем заголовок страницы
    title = autocomplete_page.page.title()
    assert len(title) > 0, "Страница должна иметь заголовок"

    # Проверяем, что поля ввода существуют и видимы
    assert (
        autocomplete_page.single_color_input.is_visible()
    ), "Поле single input должно быть видимо"
    assert (
        autocomplete_page.multi_color_input.is_visible()
    ), "Поле multi input должно быть видимо"


def test_auto_complete_multi_input_selection(autocomplete_page):
    """Тест: выбор опций в multi input."""
    # --- Первый выбор ---
    print("-> Первый выбор: Blue")
    autocomplete_page.fill_multiple_colors("Blue")
    if autocomplete_page.wait_for_dropdown(timeout=1000):
        options = autocomplete_page.get_dropdown_options_text()
        print(f"Опции в dropdown: {options}")
        if len(options) > 0:
            autocomplete_page.select_multi_color_option(0)
            autocomplete_page.page.wait_for_timeout(1500)  # Ждем установки
            print("✓ Первый выбор сделан")

    # --- Второй выбор ---
    print("-> Второй выбор: Green")
    # Вводим другой текст
    autocomplete_page.fill_multiple_colors("Green")
    if autocomplete_page.wait_for_dropdown(timeout=1000):
        options = autocomplete_page.get_dropdown_options_text()
        print(f"Опции в dropdown: {options}")
        if len(options) > 0:
            autocomplete_page.select_multi_color_option(0)
            autocomplete_page.page.wait_for_timeout(1500)  # Ждем установки
            print("✓ Второй выбор сделан")

    # Проверяем, что значения добавлены
    values = autocomplete_page.get_multi_color_values_correctly()
    print(f"Выбранные значения в multi input: {values}")
    assert len(values) > 0, "Список выбранных значений не должен быть пустым"


def test_auto_complete_single_input_selection(autocomplete_page):
    """Тест: выбор опции в single input."""
    autocomplete_page.fill_single_color("Red")
    selected_value = autocomplete_page.get_single_color_value_correctly()
    assert (
        len(selected_value) > 0
    ), f"Выбранное значение не должно быть пустым, получено: '{selected_value}'"
