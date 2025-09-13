# locators/tool_tips_locators.py
class ToolTipsLocators:
    # Основной контейнер
    # Исправлено: добавлен недостающий локатор
    MAIN_CONTAINER = "#app"

    # Элементы, на которые наводим
    HOVER_BUTTON = "#toolTipButton"
    HOVER_FIELD = "#toolTipTextField"
    HOVER_LINK = "#texToolLink"
    TEXT_CONTAINER = "#textContent"

    # Тултипы (могут быть динамическими)
    TOOLTIP_BUTTON = "#buttonToolTip"
    TOOLTIP_FIELD = "#textFieldToolTip"
    TOOLTIP_LINK = "div[role='tooltip']" # Примерный селектор, может потребоваться уточнение
    TOOLTIP_TEXT = "div[role='tooltip']" # Примерный селектор, может потребоваться уточнение
