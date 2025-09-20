"""
Локаторы для страницы Frames.
Содержит селекторы для работы с iframe элементами разного размера.
"""


class FramesLocators:
    """CSS селекторы для элементов страницы Frames."""

    # Основные iframe элементы
    BIG_FRAME = "#frame1"  # Большой iframe (500x350px)
    SMALL_FRAME = "#frame2"  # Малый iframe (100x100px)

    # Содержимое внутри iframe
    FRAME_HEADING = "#sampleHeading"  # Заголовок внутри каждого фрейма
    FRAME_BODY = "body"  # Тело фрейма

    # Альтернативные селекторы
    BIG_FRAME_ALT = "iframe[src='/sampleiframe']"  # По атрибуту src
    SMALL_FRAME_ALT = "iframe[width='100']"  # По ширине

    # Общие селекторы
    ALL_FRAMES = "iframe"  # Все iframe на странице
    FRAME_CONTAINER = "#framesWrapper"  # Контейнер всех фреймов
