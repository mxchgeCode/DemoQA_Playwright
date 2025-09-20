"""
Локаторы для страницы Modal Dialogs.
Содержит селекторы для работы с модальными диалоговыми окнами.
"""


class ModalLocators:
    """CSS селекторы для элементов страницы Modal Dialogs."""

    # Кнопки для открытия модальных окон
    SMALL_MODAL_BUTTON = "button#showSmallModal"  # Малый модальный диалог
    LARGE_MODAL_BUTTON = "button#showLargeModal"  # Большой модальный диалог

    # Структура модального окна
    MODAL_DIALOG = ".modal-dialog"  # Основной контейнер диалога
    MODAL_CONTENT = ".modal-content"  # Контент модального окна
    MODAL_HEADER = ".modal-header"  # Заголовок модального окна
    MODAL_TITLE = ".modal-title"  # Заголовок модального окна
    MODAL_BODY = ".modal-body"  # Тело модального окна
    MODAL_FOOTER = ".modal-footer"  # Подвал модального окна

    # Кнопки закрытия
    CLOSE_MODAL_X = ".modal-header .close"  # Кнопка X в заголовке
    CLOSE_MODAL_BUTTON = ".modal-footer .btn-secondary"  # Кнопка Close
    CLOSE_SMALL_MODAL = "#closeSmallModal"  # Кнопка закрытия малого диалога
    CLOSE_LARGE_MODAL = "#closeLargeModal"  # Кнопка закрытия большого диалога

    # Overlay и фон
    MODAL_BACKDROP = ".modal-backdrop"  # Затемненная область
    MODAL_FADE = ".modal.fade"  # Модальное окно с анимацией
    MODAL_SHOW = ".modal.show"  # Показанное модальное окно
