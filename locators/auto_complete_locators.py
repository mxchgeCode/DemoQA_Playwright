class AutoCompleteLocators:
    # Single color input
    SINGLE_COLOR_INPUT = "#autoCompleteSingleInput"
    SINGLE_COLOR_VALUE = ".auto-complete__single-value"

    # Multiple color input
    MULTI_COLOR_INPUT = "#autoCompleteMultipleInput"
    MULTI_COLOR_VALUES = ".css-12jo7m5"  # Selected values
    MULTI_COLOR_REMOVE_BUTTON = (
        ".css-12jo7m5 .css-19bqh2r"  # Remove button for selected items
    )

    # Dropdown options
    DROPDOWN_OPTIONS = ".auto-complete__option"
    DROPDOWN_MENU = ".auto-complete__menu"

    # Clear buttons
    CLEAR_SINGLE_BUTTON = ".auto-complete__clear-indicator"
    CLEAR_MULTI_BUTTON = ".css-1hb7zxy-IndicatorsContainer"  # Это контейнер, внутри которого clear button

    # Common elements
    PLACEHOLDER = ".auto-complete__placeholder"
