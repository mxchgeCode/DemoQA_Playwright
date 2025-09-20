"""
Page Object для страницы Menu.
Содержит методы для работы с многоуровневым навигационным меню.
"""

import time
from playwright.sync_api import Page
from locators.widgets.menu_locators import MenuLocators
from pages.widgets.base_page import WidgetBasePage


class MenuPage(WidgetBasePage):
    """
    Страница тестирования многоуровневого меню.
    Поддерживает наведение на пункты меню и навигацию по подменю.
    """

    def __init__(self, page: Page):
        """
        Инициализация страницы Menu.

        Args:
            page: Экземпляр страницы Playwright
        """
        super().__init__(page)

    def hover_main_item_1(self) -> None:
        """
        Наводит курсор на первый пункт главного меню.
        Postconditions: появляется подменю первого уровня.
        """
        self.log_step("Наводим курсор на Main Item 1")
        self.hover_and_wait(MenuLocators.MAIN_ITEM_1)

    def hover_main_item_2(self) -> None:
        """
        Наводит курсор на второй пункт главного меню.
        Postconditions: появляется подменю первого уровня.
        """
        self.log_step("Наводим курсор на Main Item 2")
        self.hover_and_wait(MenuLocators.MAIN_ITEM_2)

    def hover_main_item_3(self) -> None:
        """
        Наводит курсор на третий пункт главного меню.
        Postconditions: появляется подменю первого уровня.
        """
        self.log_step("Наводим курсор на Main Item 3")
        self.hover_and_wait(MenuLocators.MAIN_ITEM_3)

    def hover_sub_item(self, sub_item_selector: str) -> None:
        """
        Наводит курсор на элемент подменю.

        Args:
            sub_item_selector: CSS селектор элемента подменю

        Postconditions: если есть подменю второго уровня, оно появляется
        """
        self.log_step(f"Наводим курсор на элемент подменю: {sub_item_selector}")
        self.hover_and_wait(sub_item_selector)

    def click_menu_item(self, item_selector: str) -> None:
        """
        Кликает по элементу меню.

        Args:
            item_selector: CSS селектор элемента меню для клика

        Postconditions: выполнено действие, связанное с пунктом меню
        """
        self.log_step(f"Кликаем по элементу меню: {item_selector}")
        self.safe_click(item_selector)

    def navigate_to_sub_sub_menu(self) -> None:
        """
        Навигирует к подменю третьего уровня.
        Выполняет последовательность: Main Item 2 -> Sub Sub List -> Sub Sub Item 1.
        Postconditions: достигнуто подменю третьего уровня.
        """
        self.log_step("Навигируем к подменю третьего уровня")

        # Наводим на Main Item 2
        self.hover_main_item_2()
        time.sleep(500)

        # Наводим на Sub Sub List
        self.hover_sub_item(MenuLocators.SUB_SUB_LIST)
        time.sleep(500)

        # Теперь должно быть видно подменю третьего уровня

    def is_submenu_visible(self, submenu_selector: str) -> bool:
        """
        Проверяет видимость подменю.

        Args:
            submenu_selector: CSS селектор подменю

        Returns:
            bool: True если подменю видимо
        """
        return self.page.locator(submenu_selector).is_visible()

    def get_visible_menu_items(self) -> list[str]:
        """
        Получает список видимых элементов меню.

        Returns:
            list: Список текстов видимых элементов меню
        """
        visible_items = []
        menu_items = self.page.locator("ul[role='menubar'] a")

        for i in range(menu_items.count()):
            item = menu_items.nth(i)
            if item.is_visible():
                visible_items.append(item.inner_text().strip())

        return visible_items

    def wait_for_submenu_to_appear(
        self, submenu_selector: str, timeout: int = 3000
    ) -> bool:
        """
        Ожидает появления указанного подменю.

        Args:
            submenu_selector: CSS селектор подменю
            timeout: Максимальное время ожидания в миллисекундах

        Returns:
            bool: True если подменю появилось
        """
        self.log_step(f"Ожидаем появления подменю: {submenu_selector}")
        return self.wait_for_dropdown_to_appear(submenu_selector, timeout)

    def navigate_and_click(self, navigation_path: list[str]) -> None:
        """
        Выполняет навигацию по меню согласно указанному пути и кликает на конечный элемент.

        Args:
            navigation_path: Список CSS селекторов для последовательной навигации

        Example:
            navigation_path = [
                MenuLocators.MAIN_ITEM_2,
                MenuLocators.SUB_SUB_LIST,
                MenuLocators.SUB_SUB_ITEM_1
            ]

        Postconditions: выполнена навигация и клик по конечному элементу
        """
        self.log_step(f"Выполняем навигацию по пути: {navigation_path}")

        # Наводим курсор на все элементы кроме последнего
        for i, selector in enumerate(navigation_path[:-1]):
            self.hover_and_wait(selector)

        # Кликаем по последнему элементу
        if navigation_path:
            self.click_menu_item(navigation_path[-1])

    def get_menu_item_text(self, item_selector: str) -> str:
        """
        Получает текст элемента меню.

        Args:
            item_selector: CSS селектор элемента меню

        Returns:
            str: Текст элемента меню
        """
        return self.get_text_safe(item_selector) or ""

    def is_menu_item_enabled(self, item_selector: str) -> bool:
        """
        Проверяет, доступен ли элемент меню для взаимодействия.

        Args:
            item_selector: CSS селектор элемента меню

        Returns:
            bool: True если элемент доступен
        """
        try:
            menu_item = self.page.locator(item_selector)
            return menu_item.is_enabled() and menu_item.is_visible()
        except:
            return
