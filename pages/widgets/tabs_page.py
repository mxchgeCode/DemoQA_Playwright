"""
Page Object для страницы Tabs.
Содержит методы для работы с вкладками и получения их содержимого.
"""

from playwright.sync_api import Page
from locators.widgets.tabs_locators import TabsLocators
from pages.widgets.base_page import WidgetBasePage


class TabsPage(WidgetBasePage):
    """
    Страница тестирования интерфейса вкладок.
    Поддерживает переключение между вкладками и получение их содержимого.
    """

    def __init__(self, page: Page):
        """
        Инициализация страницы Tabs.

        Args:
            page: Экземпляр страницы Playwright
        """
        super().__init__(page)

    def click_what_tab(self) -> None:
        """
        Кликает по вкладке "What".
        Postconditions: активна вкладка "What", отображается её содержимое.
        """
        self.log_step("Кликаем по вкладке What")
        self.safe_click(TabsLocators.WHAT_TAB)
        self.wait_for_animation_complete(500)

    def click_origin_tab(self) -> None:
        """
        Кликает по вкладке "Origin".
        Postconditions: активна вкладка "Origin", отображается её содержимое.
        """
        self.log_step("Кликаем по вкладке Origin")
        self.safe_click(TabsLocators.ORIGIN_TAB)
        self.wait_for_animation_complete(500)

    def click_use_tab(self) -> None:
        """
        Кликает по вкладке "Use".
        Postconditions: активна вкладка "Use", отображается её содержимое.
        """
        self.log_step("Кликаем по вкладке Use")
        self.safe_click(TabsLocators.USE_TAB)
        self.wait_for_animation_complete(500)

    def click_more_tab(self) -> None:
        """
        Кликает по вкладке "More".

        Note:
            Вкладка "More" может быть недоступна (disabled).
            Метод оставлен для тестирования поведения недоступных вкладок.
        """
        self.log_step("Пытаемся кликнуть по вкладке More (может быть отключена)")
        try:
            more_tab = self.page.locator(TabsLocators.MORE_TAB)
            if more_tab.is_visible() and more_tab.is_enabled():
                more_tab.click()
                self.wait_for_animation_complete(500)
            else:
                self.log_step("Вкладка More отключена или не видна")
        except Exception as e:
            self.log_step(f"Не удалось кликнуть по вкладке More: {e}")

    def get_what_content(self) -> str:
        """
        Получает содержимое вкладки "What".

        Returns:
            str: Текстовое содержимое вкладки "What"
        """
        return self.get_text_safe(TabsLocators.WHAT_CONTENT) or ""

    def get_origin_content(self) -> str:
        """
        Получает содержимое вкладки "Origin".

        Returns:
            str: Текстовое содержимое вкладки "Origin"
        """
        return self.get_text_safe(TabsLocators.ORIGIN_CONTENT) or ""

    def get_use_content(self) -> str:
        """
        Получает содержимое вкладки "Use".

        Returns:
            str: Текстовое содержимое вкладки "Use"
        """
        return self.get_text_safe(TabsLocators.USE_CONTENT) or ""

    def get_more_content(self) -> str:
        """
        Получает содержимое вкладки "More" (если доступна).

        Returns:
            str: Текстовое содержимое вкладки "More" или пустая строка
        """
        if self.is_more_tab_enabled():
            return self.get_text_safe(TabsLocators.MORE_CONTENT) or ""
        return ""

    def is_what_tab_active(self) -> bool:
        """
        Проверяет, активна ли вкладка "What".

        Returns:
            bool: True если вкладка "What" активна
        """
        what_tab = self.page.locator(TabsLocators.WHAT_TAB)
        tab_class = what_tab.get_attribute("class") or ""
        return "active" in tab_class or "selected" in tab_class

    def is_origin_tab_active(self) -> bool:
        """
        Проверяет, активна ли вкладка "Origin".

        Returns:
            bool: True если вкладка "Origin" активна
        """
        origin_tab = self.page.locator(TabsLocators.ORIGIN_TAB)
        tab_class = origin_tab.get_attribute("class") or ""
        return "active" in tab_class or "selected" in tab_class

    def is_use_tab_active(self) -> bool:
        """
        Проверяет, активна ли вкладка "Use".

        Returns:
            bool: True если вкладка "Use" активна
        """
        use_tab = self.page.locator(TabsLocators.USE_TAB)
        tab_class = use_tab.get_attribute("class") or ""
        return "active" in tab_class or "selected" in tab_class

    def is_more_tab_active(self) -> bool:
        """
        Проверяет, активна ли вкладка "More".

        Returns:
            bool: True если вкладка "More" активна
        """
        if self.is_more_tab_enabled():
            more_tab = self.page.locator(TabsLocators.MORE_TAB)
            tab_class = more_tab.get_attribute("class") or ""
            return "active" in tab_class or "selected" in tab_class
        return False

    def is_more_tab_enabled(self) -> bool:
        """
        Проверяет, доступна ли вкладка "More" для взаимодействия.

        Returns:
            bool: True если вкладка "More" доступна
        """
        more_tab = self.page.locator(TabsLocators.MORE_TAB)
        return more_tab.is_visible() and more_tab.is_enabled()

    def get_active_tab_name(self) -> str:
        """
        Получает название текущей активной вкладки.

        Returns:
            str: Название активной вкладки ("What", "Origin", "Use", "More" или "Unknown")
        """
        if self.is_what_tab_active():
            return "What"
        elif self.is_origin_tab_active():
            return "Origin"
        elif self.is_use_tab_active():
            return "Use"
        elif self.is_more_tab_active():
            return "More"
        else:
            return "Unknown"

    def get_all_tab_names(self) -> list[str]:
        """
        Получает названия всех доступных вкладок.

        Returns:
            list: Список названий всех вкладок
        """
        tab_names = []
        tab_elements = self.page.locator(".nav-tabs .nav-item")

        for i in range(tab_elements.count()):
            tab = tab_elements.nth(i)
            tab_text = tab.inner_text().strip()
            if tab_text:
                tab_names.append(tab_text)

        return tab_names

    def switch_to_tab_by_name(self, tab_name: str) -> bool:
        """
        Переключается на вкладку по её названию.

        Args:
            tab_name: Название вкладки для переключения

        Returns:
            bool: True если переключение прошло успешно

        Postconditions: активна указанная вкладка (если она существует и доступна)
        """
        self.log_step(f"Переключаемся на вкладку: {tab_name}")

        tab_name_lower = tab_name.lower()

        if tab_name_lower == "what":
            self.click_what_tab()
            return True
        elif tab_name_lower == "origin":
            self.click_origin_tab()
            return True
        elif tab_name_lower == "use":
            self.click_use_tab()
            return True
        elif tab_name_lower == "more" and self.is_more_tab_enabled():
            self.click_more_tab()
            return True
        else:
            self.log_step(f"Вкладка '{tab_name}' не найдена или недоступна")
            return False

    def get_current_content(self) -> str:
        """
        Получает содержимое текущей активной вкладки.

        Returns:
            str: Содержимое активной вкладки
        """
        active_tab = self.get_active_tab_name()

        if active_tab == "What":
            return self.get_what_content()
        elif active_tab == "Origin":
            return self.get_origin_content()
        elif active_tab == "Use":
            return self.get_use_content()
        elif active_tab == "More":
            return self.get_more_content()
        else:
            return ""

    def cycle_through_all_tabs(self) -> list[str]:
        """
        Проходит по всем доступным вкладкам и собирает их содержимое.

        Returns:
            list: Список содержимого всех вкладок

        Postconditions: проверены все доступные вкладки
        """
        contents = []

        # What tab
        self.click_what_tab()
        contents.append(self.get_what_content())

        # Origin tab
        self.click_origin_tab()
        contents.append(self.get_origin_content())

        # Use tab
        self.click_use_tab()
        contents.append(self.get_use_content())

        # More tab (если доступна)
        if self.is_more_tab_enabled():
            self.click_more_tab()
            contents.append(self.get_more_content())

        return contents

    # === Методы для совместимости с тестами ===

    def get_all_tabs_info(self) -> dict:
        """
        Получает информацию о всех вкладках.

        Returns:
            dict: Словарь с информацией о вкладках
        """
        tabs_info = {
            "what": {
                "active": self.is_what_tab_active(),
                "enabled": True,
                "content": self.get_what_content()
            },
            "origin": {
                "active": self.is_origin_tab_active(),
                "enabled": True,
                "content": self.get_origin_content()
            },
            "use": {
                "active": self.is_use_tab_active(),
                "enabled": True,
                "content": self.get_use_content()
            },
            "more": {
                "active": self.is_more_tab_active(),
                "enabled": self.is_more_tab_enabled(),
                "content": self.get_more_content()
            }
        }
        return tabs_info

    def are_tabs_keyboard_accessible(self) -> bool:
        """
        Проверяет доступность вкладок для клавиатурной навигации.

        Returns:
            bool: True если вкладки доступны для клавиатуры
        """
        # Проверяем наличие tabindex атрибутов у вкладок
        try:
            what_tab = self.page.locator(TabsLocators.WHAT_TAB)
            origin_tab = self.page.locator(TabsLocators.ORIGIN_TAB)
            use_tab = self.page.locator(TabsLocators.USE_TAB)

            what_tabindex = what_tab.get_attribute("tabindex")
            origin_tabindex = origin_tab.get_attribute("tabindex")
            use_tabindex = use_tab.get_attribute("tabindex")

            # Если хотя бы одна вкладка имеет tabindex, считаем доступными
            return (
                what_tabindex is not None or
                origin_tabindex is not None or
                use_tabindex is not None
            )
        except:
            return False
