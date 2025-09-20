"""
Локаторы для страницы CheckBox.
Содержит селекторы для иерархического дерева чекбоксов с возможностью раскрытия.
"""


class CheckboxLocators:
    """CSS селекторы для элементов страницы CheckBox."""

    # === КНОПКИ УПРАВЛЕНИЯ ДЕРЕВОМ ===
    EXPAND_ALL_BUTTON = "button[title='Expand all']"  # Раскрыть все узлы
    COLLAPSE_ALL_BUTTON = "button[title='Collapse all']"  # Свернуть все узлы

    # === ОСНОВНЫЕ УЗЛЫ ДЕРЕВА ===
    # Корневой узел
    HOME_CHECKBOX = "label[for='tree-node-home'] span.rct-checkbox"  # Чекбокс Home
    HOME_UNCHECKBOX = (
        "label[for='tree-node-home'] span.rct-uncheckbox"  # Снятый чекбокс Home
    )
    HOME_TITLE = "label[for='tree-node-home'] span.rct-title"  # Текст Home

    # Узлы первого уровня
    DESKTOP_CHECKBOX = "label[for='tree-node-desktop'] span.rct-checkbox"  # Desktop
    DOCUMENTS_CHECKBOX = (
        "label[for='tree-node-documents'] span.rct-checkbox"  # Documents
    )
    DOWNLOADS_CHECKBOX = (
        "label[for='tree-node-downloads'] span.rct-checkbox"  # Downloads
    )

    # === УЗЛЫ ВТОРОГО УРОВНЯ (Desktop) ===
    NOTES_CHECKBOX = "label[for='tree-node-notes'] span.rct-checkbox"  # Notes
    COMMANDS_CHECKBOX = "label[for='tree-node-commands'] span.rct-checkbox"  # Commands

    # === УЗЛЫ ВТОРОГО УРОВНЯ (Documents) ===
    WORKSPACE_CHECKBOX = (
        "label[for='tree-node-workspace'] span.rct-checkbox"  # WorkSpace
    )
    OFFICE_CHECKBOX = "label[for='tree-node-office'] span.rct-checkbox"  # Office

    # === УЗЛЫ ТРЕТЬЕГО УРОВНЯ (WorkSpace) ===
    REACT_CHECKBOX = "label[for='tree-node-react'] span.rct-checkbox"  # React
    ANGULAR_CHECKBOX = "label[for='tree-node-angular'] span.rct-checkbox"  # Angular
    VEU_CHECKBOX = "label[for='tree-node-veu'] span.rct-checkbox"  # Veu

    # === УЗЛЫ ТРЕТЬЕГО УРОВНЯ (Office) ===
    PUBLIC_CHECKBOX = "label[for='tree-node-public'] span.rct-checkbox"  # Public
    PRIVATE_CHECKBOX = "label[for='tree-node-private'] span.rct-checkbox"  # Private
    CLASSIFIED_CHECKBOX = (
        "label[for='tree-node-classified'] span.rct-checkbox"  # Classified
    )
    GENERAL_CHECKBOX = "label[for='tree-node-general'] span.rct-checkbox"  # General

    # === УЗЛЫ ВТОРОГО УРОВНЯ (Downloads) ===
    WORD_FILE_CHECKBOX = (
        "label[for='tree-node-wordFile'] span.rct-checkbox"  # Word File.doc
    )
    EXCEL_FILE_CHECKBOX = (
        "label[for='tree-node-excelFile'] span.rct-checkbox"  # Excel File.doc
    )

    # === РЕЗУЛЬТАТЫ И ВЫВОД ===
    CHECKBOX_RESULT = "#result"  # Блок вывода результатов
    RESULT_TEXT = "#result span"  # Текст результатов

    # === ОБЩИЕ СЕЛЕКТОРЫ ===
    ALL_CHECKBOXES = "span.rct-checkbox"  # Все чекбоксы
    ALL_TITLES = "span.rct-title"  # Все заголовки узлов
    TREE_CONTAINER = ".rct-tree"  # Контейнер дерева
    EXPAND_ICON = ".rct-icon.rct-icon-expand-close"  # Иконка раскрытия
    COLLAPSE_ICON = ".rct-icon.rct-icon-expand-open"  # Иконка сворачивания
