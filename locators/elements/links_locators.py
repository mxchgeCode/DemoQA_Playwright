"""
Локаторы для страницы Links.
Содержит селекторы для различных типов ссылок и API вызовов.
"""


class LinksLocators:
    """CSS селекторы для элементов страницы Links."""

    # === ОСНОВНЫЕ ССЫЛКИ ===
    SIMPLE_LINK = "a#simpleLink"  # Простая ссылка на главную страницу
    DYNAMIC_LINK = "a#dynamicLink"  # Динамическая ссылка на главную страницу

    # === API ССЫЛКИ С HTTP СТАТУС КОДАМИ ===
    # 2xx Success
    CREATED_LINK = "a#created"  # HTTP 201 Created
    NO_CONTENT_LINK = "a#no-content"  # HTTP 204 No Content

    # 3xx Redirection
    MOVED_LINK = "a#moved"  # HTTP 301 Moved Permanently

    # 4xx Client Error
    BAD_REQUEST_LINK = "a#bad-request"  # HTTP 400 Bad Request
    UNAUTHORIZED_LINK = "a#unauthorized"  # HTTP 401 Unauthorized
    FORBIDDEN_LINK = "a#forbidden"  # HTTP 403 Forbidden
    NOT_FOUND_LINK = "a#invalid-url"  # HTTP 404 Not Found

    # === РЕЗУЛЬТАТЫ И ОТВЕТЫ ===
    LINK_RESPONSE_MESSAGE = "p#linkResponse"  # Сообщение с ответом API

    # === СЕКЦИИ СТРАНИЦЫ ===
    NAVIGATION_LINKS_SECTION = ".left-pannel"  # Секция навигационных ссылок
    API_LINKS_SECTION = ".right-pannel"  # Секция API ссылок

    # === ДОПОЛНИТЕЛЬНЫЕ СЕЛЕКТОРЫ ===
    ALL_LINKS = "a"  # Все ссылки на странице
    EXTERNAL_LINKS = "a[target='_blank']"  # Внешние ссылки
    INTERNAL_LINKS = "a:not([target='_blank'])"  # Внутренние ссылки

    # === ИНДИКАТОРЫ СОСТОЯНИЯ ===
    LOADING_INDICATOR = ".loading"  # Индикатор загрузки
    SUCCESS_RESPONSE = ".response-success"  # Успешный ответ
    ERROR_RESPONSE = ".response-error"  # Ошибка ответа

    # === АТРИБУТЫ ССЫЛОК ===
    LINK_HREF_ATTRIBUTE = "href"  # Атрибут href ссылки
    LINK_TARGET_ATTRIBUTE = "target"  # Атрибут target ссылки
