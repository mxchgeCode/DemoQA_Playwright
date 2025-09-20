"""
Локаторы для страницы Browser Windows.
Содержит селекторы для кнопок открытия новых вкладок и окон браузера.
"""


class BrowserWindowsLocators:
    """CSS селекторы для элементов страницы Browser Windows."""

    # Кнопки для открытия новых окон и вкладок
    NEW_TAB_BUTTON = "button#tabButton"  # Открыть новую вкладку
    NEW_WINDOW_BUTTON = "button#windowButton"  # Открыть новое окно
    NEW_WINDOW_MESSAGE_BUTTON = "button#messageWindowButton"  # Окно с сообщением

    # Альтернативные селекторы по тексту
    NEW_TAB_BUTTON_ALT = "button:has-text('New Tab')"
    NEW_WINDOW_BUTTON_ALT = "button:has-text('New Window')"
    NEW_MESSAGE_BUTTON_ALT = "button:has-text('New Window Message')"

    # Контейнер кнопок
    BUTTONS_CONTAINER = ".col-12.mt-4.col-md-6"
