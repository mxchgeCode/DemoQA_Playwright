"""
Локаторы для страницы Modal Dialogs.

Содержит все селекторы для взаимодействия с модальными окнами,
включая кнопки открытия/закрытия, содержимое и overlay элементы.
"""

from dataclasses import dataclass


@dataclass
class ModalDialogsLocators:
    """
    Класс локаторов для страницы Modal Dialogs.

    Содержит CSS селекторы для всех элементов модальных окон:
    - Кнопки открытия модальных окон
    - Элементы содержимого модальных окон  
    - Кнопки закрытия модальных окон
    - Overlay и вспомогательные элементы
    """

    # === КНОПКИ ОТКРЫТИЯ МОДАЛЬНЫХ ОКОН ===

    # Кнопка открытия малого модального окна
    SMALL_MODAL_BUTTON: str = "#showSmallModal"

    # Кнопка открытия большого модального окна
    LARGE_MODAL_BUTTON: str = "#showLargeModal"

    # === КОНТЕЙНЕРЫ МОДАЛЬНЫХ ОКОН ===

    # Основной контейнер модального окна
    MODAL_CONTAINER: str = ".modal"

    # Активное (видимое) модальное окно
    MODAL_ACTIVE: str = ".modal.show"

    # Диалог модального окна
    MODAL_DIALOG: str = ".modal-dialog"

    # Содержимое модального окна
    MODAL_CONTENT: str = ".modal-content"

    # Малое модальное окно
    SMALL_MODAL: str = "#example-modal-sizes-title-sm"

    # Большое модальное окно  
    LARGE_MODAL: str = "#example-modal-sizes-title-lg"

    # === ЭЛЕМЕНТЫ СОДЕРЖИМОГО МОДАЛЬНОГО ОКНА ===

    # Заголовок модального окна
    MODAL_TITLE: str = ".modal-title"

    # Тело модального окна
    MODAL_BODY: str = ".modal-body"

    # Футер модального окна
    MODAL_FOOTER: str = ".modal-footer"

    # === КНОПКИ ЗАКРЫТИЯ ===

    # Основная кнопка закрытия (крестик)
    MODAL_CLOSE_BUTTON: str = ".modal-header .close"

    # Альтернативная кнопка закрытия
    MODAL_CLOSE_BUTTON_ALT: str = "button[data-dismiss='modal']"

    # Кнопка закрытия в футере
    MODAL_FOOTER_CLOSE: str = ".modal-footer .btn-secondary"

    # Кнопка закрытия малого модального окна
    SMALL_MODAL_CLOSE: str = "#closeSmallModal"

    # Кнопка закрытия большого модального окна
    LARGE_MODAL_CLOSE: str = "#closeLargeModal"

    # === OVERLAY И ФОНОВЫЕ ЭЛЕМЕНТЫ ===

    # Overlay (фон) модального окна
    MODAL_BACKDROP: str = ".modal-backdrop"

    # Активный overlay
    MODAL_BACKDROP_ACTIVE: str = ".modal-backdrop.show"

    # Статический overlay (не закрывается при клике)
    MODAL_BACKDROP_STATIC: str = ".modal-backdrop.modal-static"

    # === СПЕЦИФИЧНЫЕ ЭЛЕМЕНТЫ ===

    # Контейнер для малого модального окна
    SMALL_MODAL_CONTAINER: str = "#smallModal"

    # Контейнер для большого модального окна
    LARGE_MODAL_CONTAINER: str = "#largeModal"

    # Заголовок малого модального окна
    SMALL_MODAL_TITLE: str = "#example-modal-sizes-title-sm"

    # Заголовок большого модального окна
    LARGE_MODAL_TITLE: str = "#example-modal-sizes-title-lg"

    # === ARIA И ДОСТУПНОСТЬ ===

    # Элементы с ARIA атрибутами
    MODAL_ARIA_LABELED: str = "[aria-labelledby]"
    MODAL_ARIA_MODAL: str = "[aria-modal='true']"
    MODAL_ROLE_DIALOG: str = "[role='dialog']"

    # === СОСТОЯНИЯ МОДАЛЬНЫХ ОКОН ===

    # Модальное окно в процессе открытия
    MODAL_FADE_IN: str = ".modal.fade.show"

    # Модальное окно в процессе закрытия
    MODAL_FADE_OUT: str = ".modal.fade"

    # Скрытое модальное окно
    MODAL_HIDDEN: str = ".modal[style*='display: none']"

    # === ДОПОЛНИТЕЛЬНЫЕ СЕЛЕКТОРЫ ===

    # Любая кнопка в модальном окне
    MODAL_BUTTONS: str = ".modal button"

    # Любая ссылка в модальном окне
    MODAL_LINKS: str = ".modal a"

    # Форма в модальном окне (если есть)
    MODAL_FORM: str = ".modal form"

    # Изображения в модальном окне
    MODAL_IMAGES: str = ".modal img"

    # === РАЗМЕРЫ МОДАЛЬНЫХ ОКОН ===

    # Малое модальное окно (размер SM)
    MODAL_SIZE_SM: str = ".modal-sm"

    # Большое модальное окно (размер LG) 
    MODAL_SIZE_LG: str = ".modal-lg"

    # Очень большое модальное окно (размер XL)
    MODAL_SIZE_XL: str = ".modal-xl"
