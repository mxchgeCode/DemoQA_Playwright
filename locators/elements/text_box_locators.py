"""
Локаторы для страницы Text Box.
Содержит CSS селекторы для полей ввода и областей вывода.
"""


class TextBoxLocators:
    """CSS селекторы для элементов страницы Text Box."""

    # Поля ввода
    USER_NAME = "#userName"
    USER_EMAIL = "#userEmail"
    CURRENT_ADDRESS = "#currentAddress"
    PERMANENT_ADDRESS = "#permanentAddress"

    # Кнопка отправки
    SUBMIT_BUTTON = "#submit"

    # Область вывода результатов
    OUTPUT_CONTAINER = "#output"
    OUTPUT_NAME = "#output #name"
    OUTPUT_EMAIL = "#output #email"
    OUTPUT_CURRENT_ADDRESS = "#output #currentAddress"
    OUTPUT_PERMANENT_ADDRESS = "#output #permanentAddress"

    # Альтернативные селекторы для областей вывода
    OUTPUT_NAME_ALT = "#output p[id='name']"
    OUTPUT_EMAIL_ALT = "#output p[id='email']"
    OUTPUT_CURRENT_ADDRESS_ALT = "#output p[id='currentAddress']"
    OUTPUT_PERMANENT_ADDRESS_ALT = "#output p[id='permanentAddress']"
