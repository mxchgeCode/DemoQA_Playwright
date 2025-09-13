# locators/auto_complete_locators.py
class AutoCompleteLocators:
    # Основной контейнер
    # Исправлено: добавлен недостающий локатор
    MAIN_CONTAINER = "#app"

    # Поля ввода
    SINGLE_COLOR_INPUT = "#autoCompleteSingleInput"
    MULTI_COLOR_INPUT = "#autoCompleteMultipleInput"

    # Dropdown
    DROPDOWN_CONTAINER = ".auto-complete__menu" # Примерный селектор
    DROPDOWN_OPTIONS = ".auto-complete__option" # Примерный селектор
