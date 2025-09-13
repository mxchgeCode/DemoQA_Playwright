# pages/menu_page.py
from playwright.sync_api import Page
from locators.menu_locators import MenuLocators


class MenuPage:
    def __init__(self, page: Page):
        self.page = page

        # Основные элементы
        self.main_container = page.locator(MenuLocators.MAIN_CONTAINER)
        self.menu_tree = page.locator(MenuLocators.MENU_TREE)
        self.tree_items = page.locator(MenuLocators.TREE_ITEMS)
        self.tree_item_contents = page.locator(MenuLocators.TREE_ITEM_CONTENT)

        # Конкретные элементы по тексту
        self.main_item_1 = page.locator(MenuLocators.MAIN_ITEM_1)
        self.main_item_2 = page.locator(MenuLocators.MAIN_ITEM_2)
        self.main_item_3 = page.locator(MenuLocators.MAIN_ITEM_3)
        self.sub_item = page.locator(MenuLocators.SUB_ITEM)
        self.sub_sub_list = page.locator(MenuLocators.SUB_SUB_LIST)
        self.sub_sub_item_1 = page.locator(MenuLocators.SUB_SUB_ITEM_1)
        self.sub_sub_item_2 = page.locator(MenuLocators.SUB_SUB_ITEM_2)

    def get_tree_items_count(self) -> int:
        """Получает количество элементов дерева."""
        try:
            count = self.tree_items.count()
            return count
        except:
            return 0

    def get_item_text(self, item_locator) -> str:
        """Получает текст элемента."""
        try:
            if item_locator.count() > 0:
                # Пробуем разные способы получения текста
                try:
                    return (
                        item_locator.first.locator(".MuiTreeItem-label")
                        .text_content()
                        .strip()
                    )
                except:
                    pass
                try:
                    return item_locator.first.text_content().strip()
                except:
                    pass
            return ""
        except:
            return ""

    def click_item(self, item_locator) -> bool:
        """Кликает по элементу меню."""
        try:
            if item_locator.count() > 0:
                # Пробуем кликнуть по разным частям элемента
                try:
                    item_locator.first.locator(".MuiTreeItem-content").click()
                    self.page.wait_for_timeout(500)
                    return True
                except:
                    pass
                try:
                    item_locator.first.click()
                    self.page.wait_for_timeout(500)
                    return True
                except:
                    pass
            return False
        except:
            return False

    def hover_item(self, item_locator) -> bool:
        """Наводит курсор на элемент меню."""
        try:
            if item_locator.count() > 0:
                try:
                    item_locator.first.hover()
                    self.page.wait_for_timeout(500)
                    return True
                except:
                    pass
            return False
        except:
            return False

    def is_page_loaded(self) -> bool:
        """Проверяет, загрузилась ли страница."""
        try:
            return self.main_container.is_visible()
        except:
            return False

    def find_items_by_text(self, text: str):
        """Находит элементы по тексту."""
        try:
            return self.page.locator(f":has-text('{text}')")
        except:
            return None
