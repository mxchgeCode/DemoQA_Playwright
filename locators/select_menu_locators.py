# locators/select_menu_locators.py
class SelectMenuLocators:
    # Основной контейнер
    MAIN_CONTAINER = "#app"

    # --- Select Value (Simple Select Menu) ---
    # Исправлено: добавлен недостающий локатор
    SELECT_VALUE = "#oldSelectMenu" # Это обычный select, используемый для "Select Value"
    SELECT_VALUE_OPTIONS = "#oldSelectMenu option"

    # --- Select One (React select) ---
    SELECT_ONE_CONTAINER = "#withOptGroup"
    SELECT_ONE_CONTROL = "#withOptGroup div[class*='control']"
    SELECT_ONE_INPUT = "#react-select-2-input" # Input внутри Select One

    # --- Old Style Select Menu (обычный select) ---
    OLD_STYLE_SELECT = "#oldSelectMenu" # Тот же элемент, что и SELECT_VALUE
    OLD_STYLE_SELECT_OPTIONS = "#oldSelectMenu option"

    # --- Multiselect drop down (React select) ---
    MULTISELECT = "#cars" # Это обычный select multiple
    MULTISELECT_OPTIONS = "#cars option"

    # --- Standard multi select (обычный select multiple) ---
    STANDARD_MULTI_SELECT = "#cars" # Это тот же элемент, что и MULTISELECT
    STANDARD_MULTI_SELECT_OPTIONS = "#cars option"

    # --- Общие элементы для dropdown опций и меню ---
    DROPDOWN_OPTION = "div[class*='option']"
    DROPDOWN_MENU = "div[class*='menu']"

    # --- Все select элементы (для подсчета) ---
    ALL_SELECTS = "#oldSelectMenu, #cars, #withOptGroup div[class*='control']"
