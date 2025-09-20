"""
Локаторы для страницы Nested Frames.
Содержит селекторы для работы с вложенными iframe элементами.
"""


class NestedFramesLocators:
    """CSS селекторы для элементов страницы Nested Frames."""

    # Основные вложенные фреймы
    PARENT_FRAME = "iframe[srcdoc*='Parent frame']"  # Родительский фрейм
    CHILD_FRAME = (
        "iframe[srcdoc*='Child Iframe']"  # Дочерний фрейм внутри родительского
    )

    # Альтернативные селекторы по структуре
    PARENT_FRAME_ALT = "#frame1"  # Если есть ID у родительского
    CHILD_FRAME_ALT = "iframe"  # Дочерний внутри родительского

    # Содержимое фреймов
    PARENT_BODY = "body"  # Тело родительского фрейма
    CHILD_BODY = "body"  # Тело дочернего фрейма
    PARENT_TEXT = "p"  # Текст в родительском фрейме
    CHILD_TEXT = "p"  # Текст в дочернем фрейме

    # Контейнеры
    FRAMES_WRAPPER = "#framesWrapper"  # Общий контейнер фреймов
