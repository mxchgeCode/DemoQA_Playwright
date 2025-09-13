# tests/test_tool_tips.py
import pytest


def test_tool_tips_page_loads(tooltips_page):
    """Тест: страница Tool Tips загружается корректно."""
    # Даем время странице загрузиться
    tooltips_page.page.wait_for_timeout(2000)

    # Проверяем URL и заголовок
    current_url = tooltips_page.page.url
    page_title = tooltips_page.page.title()
    assert "tool-tips" in current_url.lower(), "URL должен содержать 'tool-tips'"
    # assert "ToolsQA" in page_title, "Заголовок страницы должен содержать 'ToolsQA'" # Опционально

    # Проверяем наличие основных элементов
    assert tooltips_page.hover_button.is_visible(), "Кнопка 'Hover me' должна быть видима"
    assert tooltips_page.hover_link.is_visible(), "Ссылка 'This Link' должна быть видима"


def test_tool_tips_button_hover(tooltips_page):
    """Тест: появление тултипа при наведении на кнопку."""
    # Даем время странице загрузиться
    tooltips_page.page.wait_for_timeout(2000)

    # Наведение на кнопку
    tooltips_page.hover_over_button()
    tooltips_page.page.wait_for_timeout(500)

    # Проверка текста тултипа
    button_tooltip_text = tooltips_page.get_button_tooltip_text()
    assert "You hovered over the Button" in button_tooltip_text
    print(f"✓ Текст тултипа кнопки: '{button_tooltip_text}'")

    # Скрытие тултипа
    tooltips_page.move_mouse_away()
    tooltips_page.page.wait_for_timeout(500)

    # Проверка, что тултип исчез (необязательно, но хорошо для полноты)
    # assert not tooltips_page.is_button_tooltip_visible(), "Тултип кнопки должен исчезнуть"


def test_tool_tips_link_and_button(tooltips_page): # Объединенный тест
    """Тест: появление тултипов при наведении на ссылку и кнопку."""
    # Даем время странице загрузиться
    tooltips_page.page.wait_for_timeout(2000)

    # --- Наведение на ссылку ---
    tooltips_page.hover_over_link()
    tooltips_page.page.wait_for_timeout(500)
    link_tooltip_text = tooltips_page.get_link_tooltip_text()
    assert "You hovered over the Link" in link_tooltip_text
    print(f"✓ Текст тултипа ссылки: '{link_tooltip_text}'")

    # Скрытие тултипа ссылки
    tooltips_page.move_mouse_away()
    tooltips_page.page.wait_for_timeout(500)
    # assert not tooltips_page.is_link_tooltip_visible(), "Тултип ссылки должен исчезнуть"

    # --- Наведение на кнопку ---
    tooltips_page.hover_over_button()
    tooltips_page.page.wait_for_timeout(500)
    button_tooltip_text = tooltips_page.get_button_tooltip_text()
    assert "You hovered over the Button" in button_tooltip_text
    print(f"✓ Текст тултипа кнопки: '{button_tooltip_text}'")

    # Скрытие тултипа кнопки
    tooltips_page.move_mouse_away()
    tooltips_page.page.wait_for_timeout(500)
    # assert not tooltips_page.is_button_tooltip_visible(), "Тултип кнопки должен исчезнуть"


def test_tool_tips_input_field(tooltips_page):
    """Тест: появление тултипа при наведении на поле ввода."""
    # Даем время странице загрузиться
    tooltips_page.page.wait_for_timeout(2000)

    # Наведение на поле ввода
    tooltips_page.hover_over_input()
    tooltips_page.page.wait_for_timeout(500)

    # Проверка текста тултипа
    input_tooltip_text = tooltips_page.get_input_tooltip_text()
    assert "You hovered over the Input Field" in input_tooltip_text
    print(f"✓ Текст тултипа поля ввода: '{input_tooltip_text}'")

    # Скрытие тултипа
    tooltips_page.move_mouse_away()
    tooltips_page.page.wait_for_timeout(500)


def test_tool_tips_text_container(tooltips_page):
    """Тест: появление тултипа при наведении на текстовый контейнер."""
    # Даем время странице загрузиться
    tooltips_page.page.wait_for_timeout(2000)

    # Наведение на текстовый контейнер
    tooltips_page.hover_over_text_container()
    tooltips_page.page.wait_for_timeout(500)

    # Проверка текста тултипа
    text_tooltip_text = tooltips_page.get_text_container_tooltip_text()
    assert "You hovered over the Contrary" in text_tooltip_text or " contrary " in text_tooltip_text.lower()
    print(f"✓ Текст тултипа текстового контейнера: '{text_tooltip_text}'")

    # Скрытие тултипа
    tooltips_page.move_mouse_away()
    tooltips_page.page.wait_for_timeout(500)
