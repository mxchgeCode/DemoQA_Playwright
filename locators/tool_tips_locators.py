# locators/tool_tips_locators.py
class ToolTipsLocators:
    # Основной контейнер
    MAIN_CONTAINER = "#app"

    # Элементы, на которые наводим
    # Исправлено: Реальные ID с сайта https://demoqa.com/tool-tips
    HOVER_BUTTON = "#toolTipButton"
    HOVER_FIELD = "#toolTipTextField"
    HOVER_LINK = "#texToolLink" # Исправлено: "texToolLink", а не "toolTipLink"
    TEXT_CONTAINER = "#contraryText"

    # Тултипы (могут быть динамическими)
    # Исправлено: Тултипы рендерятся в портале, поэтому используем общий селектор
    TOOLTIP_TEXT = "div[role='tooltip']" # Все тултипы имеют этот атрибут