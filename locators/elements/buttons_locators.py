"""
Локаторы для страницы Buttons.
Содержит селекторы для кнопок различных типов кликов и сообщений результата.
"""


class ButtonsLocators:
    """CSS селекторы для элементов страницы Buttons."""

    # Кнопки для различных типов кликов
    DOUBLE_CLICK_BUTTON = "#doubleClickBtn"
    RIGHT_CLICK_BUTTON = "#rightClickBtn"
    CLICK_ME_BUTTON = "button.btn.btn-primary:nth-child(3)"

    # Альтернативные селекторы кнопок
    DOUBLE_CLICK_BUTTON_ALT = "button:has-text('Double Click Me')"
    RIGHT_CLICK_BUTTON_ALT = "button:has-text('Right Click Me')"
    CLICK_ME_BUTTON_ALT = (
        "button:has-text('Click Me'):not(#doubleClickBtn):not(#rightClickBtn)"
    )

    # Сообщения результатов кликов
    DOUBLE_CLICK_MESSAGE = "#doubleClickMessage"
    RIGHT_CLICK_MESSAGE = "#rightClickMessage"
    CLICK_ME_MESSAGE = "#dynamicClickMessage"

    # Контейнер для всех кнопок
    BUTTONS_CONTAINER = ".btn-group-vertical"

    # Общий селектор для всех кнопок
    ALL_BUTTONS = "button.btn.btn-primary"
