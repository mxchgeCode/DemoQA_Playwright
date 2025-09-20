"""
Локаторы для страницы Broken Links Images.
Содержит селекторы для проверки работоспособности изображений и ссылок.
"""


class BrokenLinksLocators:
    """CSS селекторы для элементов страницы Broken Links Images."""

    # === ИЗОБРАЖЕНИЯ ===
    VALID_IMAGE = "img[src='/images/Toolsqa.jpg']"  # Рабочее изображение
    BROKEN_IMAGE = "img[src='/images/Toolsqa_1.jpg']"  # Сломанное изображение (404)

    # Альтернативные селекторы изображений
    VALID_IMAGE_ALT = "img[alt='Valid image']"  # По alt атрибуту
    BROKEN_IMAGE_ALT = "img[alt='Broken image']"  # По alt атрибуту

    # === ССЫЛКИ ===
    VALID_LINK = "a[href='http://demoqa.com']"  # Рабочая ссылка
    BROKEN_LINK = "a[href='http://the-internet.herokuapp.com/status_codes/500']"  # Сломанная ссылка (500)

    # Альтернативные селекторы ссылок
    VALID_LINK_ALT = "a:has-text('Valid Link')"  # По тексту ссылки
    BROKEN_LINK_ALT = "a:has-text('Broken Link')"  # По тексту ссылки

    # === КОНТЕЙНЕРЫ И СЕКЦИИ ===
    IMAGES_SECTION = ".col-md-6:has(img)"  # Секция с изображениями
    LINKS_SECTION = ".col-md-6:has(a)"  # Секция со ссылками

    # === ОБЩИЕ СЕЛЕКТОРЫ ===
    ALL_IMAGES = "img"  # Все изображения на странице
    ALL_LINKS = "a"  # Все ссылки на странице
    PAGE_CONTENT = ".col-12.col-md-6"  # Основной контент страницы
