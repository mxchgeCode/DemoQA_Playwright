# locators/menu_locators.py
class MenuLocators:
    # Main container
    MAIN_CONTAINER = "#app"

    # Menu tree structure
    MENU_TREE = ".MuiTree-root"
    TREE_ITEMS = ".MuiTreeItem-root"

    # Text content of tree items
    TREE_ITEM_CONTENT = ".MuiTreeItem-content"
    TREE_ITEM_LABEL = ".MuiTreeItem-label"

    # Specific items by text (более гибкий подход)
    MAIN_ITEM_1 = ":has-text('Main Item 1')"
    MAIN_ITEM_2 = ":has-text('Main Item 2')"
    MAIN_ITEM_3 = ":has-text('Main Item 3')"
    SUB_ITEM = ":has-text('Sub Item')"
    SUB_SUB_LIST = ":has-text('SUB SUB LIST')"
    SUB_SUB_ITEM_1 = ":has-text('Sub Sub Item 1')"
    SUB_SUB_ITEM_2 = ":has-text('Sub Sub Item 2')"

    # All clickable menu items
    CLICKABLE_ITEMS = ".MuiTreeItem-content, .MuiTreeItem-label"
