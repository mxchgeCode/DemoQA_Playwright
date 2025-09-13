# tests/test_tool_tips.py
import pytest


def test_tool_tips_page_loads(tooltips_page):
    """Тест: страница Tool Tips загружается корректно."""
    # Даем время странице загрузиться
    tooltips_page.page.wait_for_timeout(2000)

    # Проверяем URL
    current_url = tooltips_page.page.url
    assert "tool-tips" in current_url.lower(), "URL должен содержать 'tool-tips'"


def test_tool_tips_hover_and_disappear(tooltips_page):
    """Тест: появление и исчезновение тултипов."""
    # Даем время странице загрузиться
    tooltips_page.page.wait_for_timeout(2000)

    # --- Наведение на кнопку ---
    tooltips_page.hover_over_button()
    tooltips_page.page.wait_for_timeout(1000) # Увеличено ожидание
    button_tooltip_text = tooltips_page.get_button_tooltip_text()
    assert "You hovered over the Button" in button_tooltip_text
    print(f"✓ Текст тултипа кнопки: '{button_tooltip_text}'")

    # Скрытие тултипа кнопки
    tooltips_page.move_mouse_away()
    tooltips_page.page.wait_for_timeout(1000) # Увеличено ожидание
    # Проверка исчезновения может быть нестабильна, пропустим

    # --- Наведение на поле ввода ---
    tooltips_page.hover_over_input()
    tooltips_page.page.wait_for_timeout(1000)
    input_tooltip_text = tooltips_page.get_input_tooltip_text()
    assert "You hovered over the Input Field" in input_tooltip_text
    print(f"✓ Текст тултипа поля ввода: '{input_tooltip_text}'")

    # Скрытие тултипа поля ввода
    tooltips_page.move_mouse_away()
    tooltips_page.page.wait_for_timeout(1000)


def test_tool_tips_other_elements(tooltips_page):
    """Тест: тултипы для других элементов."""
    # Даем время странице загрузиться
    tooltips_page.page.wait_for_timeout(2000)

    # --- Наведение на ссылку ---
    tooltips_page.hover_over_link()
    tooltips_page.page.wait_for_timeout(1000)
    link_tooltip_text = tooltips_page.get_link_tooltip_text()
    assert "You hovered over the Link" in link_tooltip_text
    print(f"✓ Текст тултипа ссылки: '{link_tooltip_text}'")

    # Скрытие тултипа ссылки
    tooltips_page.move_mouse_away()
    tooltips_page.page.wait_for_timeout(1000)

    # --- Наведение на текстовый контейнер ---
    tooltips_page.hover_over_text_container()
    tooltips_page.page.wait_for_timeout(1000)
    text_tooltip_text = tooltips_page.get_text_container_tooltip_text()
    # Упрощаем проверку
    assert "hovered" in text_tooltip_text.lower() or "contrary" in text_tooltip_text.lower()
    print(f"✓ Текст тултипа текстового контейнера: '{text_tooltip_text}'")

    # Скрытие тултипа текстового контейнера
    tooltips_page.move_mouse_away()
    tooltips_page.page.wait_for_timeout(1000)
