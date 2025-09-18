from playwright.sync_api import Page
import logging

from locators.interactions.selectable_locators import SelectableLocators

logger = logging.getLogger(__name__)


class SelectablePage:
    def __init__(self, page: Page):
        self.page = page

    def open(self):
        logger.info("Открытие страницы selectable")
        self.page.goto("https://demoqa.com/selectable", wait_until="domcontentloaded")

    def activate_list_tab(self):
        logger.info("Активируем вкладку List")
        self.page.click(SelectableLocators.LIST_TAB_BUTTON)
        self.page.wait_for_selector(
            SelectableLocators.LIST_TAB_CONTENT, state="visible", timeout=10000
        )

    def activate_grid_tab(self):
        logger.info("Активируем вкладку Grid")
        self.page.click(SelectableLocators.GRID_TAB_BUTTON)
        self.page.wait_for_selector(
            SelectableLocators.GRID_TAB_CONTENT, state="visible", timeout=10000
        )

    def get_list_items(self):
        locator = self.page.locator(SelectableLocators.LIST_TAB_CONTENT)
        locator.first.wait_for(state="visible", timeout=10000)
        texts = [el.inner_text().strip() for el in locator.all()]
        logger.info(f"Элементы списка: {texts}")
        return texts

    def select_list_item(self, index: int):
        logger.info(f"Выбираем элемент списка под индексом {index}")
        self.page.locator(SelectableLocators.LIST_TAB_CONTENT).nth(index).click()

    def get_selected_list_items(self):
        locator = self.page.locator(f"{SelectableLocators.LIST_TAB_CONTENT}.active")
        selected_texts = [el.inner_text().strip() for el in locator.all()]
        logger.info(f"Выбранные элементы списка: {selected_texts}")
        return selected_texts

    def get_grid_items(self):
        locator = self.page.locator(SelectableLocators.GRID_TAB_CONTENT)
        locator.first.wait_for(state="visible", timeout=10000)
        texts = [el.inner_text().strip() for el in locator.all()]
        logger.info(f"Элементы сетки: {texts}")
        return texts

    def select_grid_item(self, index: int):
        logger.info(f"Выбираем элемент сетки под индексом {index}")
        self.page.locator(SelectableLocators.GRID_TAB_CONTENT).nth(index).click()

    def get_selected_grid_items(self):
        locator = self.page.locator(f"{SelectableLocators.GRID_TAB_CONTENT}.active")
        selected_texts = [el.inner_text().strip() for el in locator.all()]
        logger.info(f"Выбранные элементы сетки: {selected_texts}")
        return selected_texts
