# locators/select_menu_locators.py
class SelectMenuLocators:
    # Основной контейнер
    MAIN_CONTAINER = "#app"

    # --- Select Value (React select) ---
    SELECT_VALUE_CONTAINER = "#withOptGroup"
    SELECT_VALUE_INPUT = "#react-select-2-input"
    # Индикатор (стрелка) для клика, если input не работает
    SELECT_VALUE_INDICATOR = "#withOptGroup .css-tlfecz-indicatorContainer"

    # --- Select One (React select) ---
    SELECT_ONE_CONTAINER = "#selectOne"
    SELECT_ONE_INPUT = "#react-select-3-input"
    # Индикатор (стрелка)
    SELECT_ONE_INDICATOR = "#selectOne .css-tlfecz-indicatorContainer"

    # --- Old Style Select Menu (обычный select) ---
    OLD_STYLE_SELECT = "#oldSelectMenu"
    OLD_STYLE_SELECT_OPTIONS = "#oldSelectMenu option"

    # --- Multiselect drop down (React select) ---
    MULTISELECT_INPUT = "#react-select-4-input"
    # Индикатор (стрелка)
    MULTISELECT_INDICATOR = "div:has(> #react-select-4-input) .css-tlfecz-indicatorContainer"

    # --- Standard multi select (обычный select multiple) ---
    STANDARD_MULTI_SELECT = "#cars"
    STANDARD_MULTI_SELECT_OPTIONS = "#cars option"

    # --- Общие элементы для dropdown опций и меню ---
    DROPDOWN_OPTION = "div[class*='option']"
    DROPDOWN_MENU = "div[class*='menu']"

    # --- Все select элементы (для подсчета) ---
    ALL_SELECTS = "#oldSelectMenu, #cars, #withOptGroup div[class*='control'], #selectOne div[class*='control'], #react-select-4-input"
