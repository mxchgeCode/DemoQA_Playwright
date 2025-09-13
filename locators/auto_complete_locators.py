# locators/auto_complete_locators.py
class AutoCompleteLocators:
    # Основной контейнер
    MAIN_CONTAINER = "#app"

    # Поля ввода
    # Исправлено: Реальные ID с сайта https://demoqa.com/auto-complete
    SINGLE_COLOR_INPUT = "#autoCompleteSingleInput"
    MULTI_COLOR_INPUT = "#autoCompleteMultipleInput"

    # Dropdown
    DROPDOWN_OPTIONS = "div[role='option']" # Общий селектор для всех опций в выпадающем списке