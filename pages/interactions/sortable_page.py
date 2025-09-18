from playwright.sync_api import Page
import logging

logger = logging.getLogger(__name__)


class SortablePage:
    def __init__(self, page: Page):
        self.page = page

    def open(self):
        logger.info("Открытие страницы sortable")
        self.page.goto("https://demoqa.com/sortable", wait_until="domcontentloaded")

    def activate_list_tab(self):
        logger.info("Активируем вкладку List")
        self.page.click("#demo-tab-list")
        self.page.wait_for_selector(
            "#demo-tabpane-list .list-group-item", state="visible", timeout=10000
        )

    def activate_grid_tab(self):
        logger.info("Активируем вкладку Grid")
        self.page.click("#demo-tab-grid")
        self.page.wait_for_selector(
            "#demo-tabpane-grid .list-group-item", state="visible", timeout=10000
        )

    def get_item_texts(self):
        locator = self.page.locator("#demo-tabpane-list .list-group-item")
        locator.first.wait_for(state="visible", timeout=10000)
        texts = [el.inner_text().strip() for el in locator.all()]
        logger.info(f"Тексты списка: {texts}")
        return texts

    def drag_and_drop_item(self, source_index: int, target_index: int):
        logger.info(
            f"Перетаскиваем в List элемент с позиции {source_index} на позицию {target_index}"
        )
        source = self.page.locator("#demo-tabpane-list .list-group-item").nth(
            source_index
        )
        target = self.page.locator("#demo-tabpane-list .list-group-item").nth(
            target_index
        )
        source.drag_to(target)
        logger.info("Перетаскивание List элемента завершено")

    def get_grid_item_texts(self):
        locator = self.page.locator("#demo-tabpane-grid .list-group-item")
        locator.first.wait_for(state="visible", timeout=10000)
        texts = [el.inner_text().strip() for el in locator.all()]
        logger.info(f"Тексты сетки: {texts}")
        return texts

    def drag_and_drop_grid_item(self, source_index: int, target_index: int):
        logger.info(
            f"Перетаскиваем в Grid элемент с позиции {source_index} на позицию {target_index}"
        )
        source = self.page.locator("#demo-tabpane-grid .list-group-item").nth(
            source_index
        )
        target = self.page.locator("#demo-tabpane-grid .list-group-item").nth(
            target_index
        )
        source.drag_to(target)
        logger.info("Перетаскивание Grid элемента завершено")
