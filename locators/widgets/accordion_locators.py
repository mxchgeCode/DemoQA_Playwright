"""
Локаторы для страницы Accordion.
Содержит селекторы для заголовков, содержимого и кнопок секций аккордеона.
"""


class AccordionLocators:
    """CSS селекторы для элементов страницы Accordion."""

    # Контейнер аккордеона
    ACCORDION_CONTAINER = "#accordionExample"

    # Первая секция
    FIRST_SECTION_HEADER = "#section1Heading"
    FIRST_SECTION_CONTENT = "#section1Content"
    FIRST_SECTION_BUTTON = "#section1Heading button"
    FIRST_SECTION_COLLAPSE = "#collapseOne"

    # Вторая секция
    SECOND_SECTION_HEADER = "#section2Heading"
    SECOND_SECTION_CONTENT = "#section2Content"
    SECOND_SECTION_BUTTON = "#section2Heading button"
    SECOND_SECTION_COLLAPSE = "#collapseTwo"

    # Третья секция
    THIRD_SECTION_HEADER = "#section3Heading"
    THIRD_SECTION_CONTENT = "#section3Content"
    THIRD_SECTION_BUTTON = "#section3Heading button"
    THIRD_SECTION_COLLAPSE = "#collapseThree"

    # Общие селекторы
    ALL_HEADERS = ".card-header"
    ALL_CONTENT = ".card-body"
    ALL_BUTTONS = ".card-header button"

    # Селекторы состояний
    EXPANDED_SECTION = ".collapse.show"
    COLLAPSED_SECTION = ".collapse:not(.show)"
    ACTIVE_BUTTON = "button[aria-expanded='true']"
