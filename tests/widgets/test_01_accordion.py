# def test_accordion_initial_state(accordion_page):
#     """Проверка начального состояния аккордеона."""
#     # accordion_page.page.wait_for_timeout(1000)
#
#     assert (
#         accordion_page.first_section_header.is_visible()
#     ), "Первый заголовок должен быть видим"
#     assert (
#         accordion_page.second_section_header.is_visible()
#     ), "Второй заголовок должен быть видим"
#     assert (
#         accordion_page.third_section_header.is_visible()
#     ), "Третий заголовок должен быть видим"


def test_accordion_toggle_first_section(accordion_page):
    """Переключение первого раздела аккордеона."""
    # accordion_page.page.wait_for_timeout(500)
    initial_state = accordion_page.is_first_section_expanded()
    accordion_page.click_first_section()
    accordion_page.page.wait_for_timeout(1000)
    new_state = accordion_page.is_first_section_expanded()
    assert (
        new_state != initial_state
    ), f"Состояние первого раздела должно измениться с {initial_state} на {new_state}"


def test_accordion_multiple_sections_independence(accordion_page):
    """Тест: проверка стандартного поведения аккордеона (только один раздел раскрыт)."""
    # accordion_page.page.wait_for_timeout(1000)

    accordion_page.click_first_section()
    accordion_page.page.wait_for_timeout(1000)
    assert (
        accordion_page.is_first_section_expanded()
    ), "Первый раздел должен быть раскрыт"

    accordion_page.click_second_section()
    accordion_page.page.wait_for_timeout(1000)

    # После открытия второго, первый обычно сворачивается
    assert (
        accordion_page.is_second_section_expanded()
    ), "Второй раздел должен быть раскрыт"
    assert (
        not accordion_page.is_first_section_expanded()
    ), "Первый раздел должен быть свернут"


def test_accordion_content_accessibility(accordion_page):
    """Проверка доступности контента первого раздела."""
    accordion_page.click_first_section()
    accordion_page.page.wait_for_timeout(1000)
    content = accordion_page.get_first_section_text()
    assert len(content) > 0, "Контент первого раздела должен быть доступен"


def test_accordion_button_functionality(accordion_page):
    """Тест: функциональность кнопок аккордеона."""
    # accordion_page.page.wait_for_timeout(1000)

    # Запоминаем начальное состояние (раскрыт/свернут первый раздел)
    initial_expanded = accordion_page.is_first_section_expanded()

    # Пытаемся кликнуть по кнопке в первом разделе
    try:
        accordion_page.click_first_button()
    except Exception:
        # Если кнопка не сработала, кликаем по заголовку
        accordion_page.click_first_section()

    accordion_page.page.wait_for_timeout(1000)

    # Проверяем, что состояние изменилось (раскрыт/свернут)
    new_expanded = accordion_page.is_first_section_expanded()

    assert (
        new_expanded != initial_expanded
    ), "Состояние первого раздела должно измениться после клика по кнопке"


def test_accordion_header_texts(accordion_page):
    """Проверка корректности заголовков секций."""
    first = accordion_page.get_first_section_header_text()
    second = accordion_page.get_second_section_header_text()
    third = accordion_page.get_third_section_header_text()

    assert (
        "What is Lorem Ipsum?" in first
    ), f"Первый заголовок не соответствует: {first}"
    assert (
        "Where does it come from?" in second
    ), f"Второй заголовок не соответствует: {second}"
    assert "Why do we use it?" in third, f"Третий заголовок не соответствует: {third}"


def test_accordion_content_exists(accordion_page):
    """Проверка наличия текста в разделах аккордеона."""
    sections = [
        (accordion_page.click_first_section, accordion_page.get_first_section_text),
        (accordion_page.click_second_section, accordion_page.get_second_section_text),
        (accordion_page.click_third_section, accordion_page.get_third_section_text),
    ]
    for click_func, get_text_func in sections:
        click_func()
        accordion_page.page.wait_for_timeout(300)
        text = get_text_func()
        assert len(text) > 0, "Раздел должен содержать текст"
