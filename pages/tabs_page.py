# pages/tabs_page.py
from playwright.sync_api import Page
from locators.tabs_locators import TabsLocators


class TabsPage:
    def __init__(self, page: Page):
        self.page = page

        # Tab header elements
        self.tab_what = page.locator(TabsLocators.TAB_WHAT)
        self.tab_origin = page.locator(TabsLocators.TAB_ORIGIN)
        self.tab_use = page.locator(TabsLocators.TAB_USE)
        self.tab_more = page.locator(TabsLocators.TAB_MORE)

        # Tab content panel elements
        self.panel_what = page.locator(TabsLocators.PANEL_WHAT)
        self.panel_origin = page.locator(TabsLocators.PANEL_ORIGIN)
        self.panel_use = page.locator(TabsLocators.PANEL_USE)
        self.panel_more = page.locator(TabsLocators.PANEL_MORE)

        # Content elements
        self.panel_what_content = page.locator(TabsLocators.PANEL_WHAT_CONTENT)
        self.panel_origin_content = page.locator(TabsLocators.PANEL_ORIGIN_CONTENT)
        self.panel_use_content = page.locator(TabsLocators.PANEL_USE_CONTENT)
        self.panel_more_content = page.locator(TabsLocators.PANEL_MORE_CONTENT)

    def click_what_tab(self):
        """Клик по вкладке 'What'."""
        self.tab_what.click(force=True)
        self.page.wait_for_timeout(1000)

    def click_origin_tab(self):
        """Клик по вкладке 'Origin'."""
        self.tab_origin.click(force=True)
        self.page.wait_for_timeout(1000)

    def click_use_tab(self):
        """Клик по вкладке 'Use'."""
        self.tab_use.click(force=True)
        self.page.wait_for_timeout(1000)

    def click_more_tab(self):
        """Клик по вкладке 'More'."""
        try:
            if self.tab_more.is_enabled():
                self.tab_more.click(force=True)
                self.page.wait_for_timeout(1000)
        except:
            pass

    def is_what_tab_active(self) -> bool:
        """Проверяет, активна ли вкладка 'What'."""
        try:
            classes = self.tab_what.get_attribute("class") or ""
            return "active" in classes
        except:
            return False

    def is_origin_tab_active(self) -> bool:
        """Проверяет, активна ли вкладка 'Origin'."""
        try:
            classes = self.tab_origin.get_attribute("class") or ""
            return "active" in classes
        except:
            return False

    def is_use_tab_active(self) -> bool:
        """Проверяет, активна ли вкладка 'Use'."""
        try:
            classes = self.tab_use.get_attribute("class") or ""
            return "active" in classes
        except:
            return False

    def is_more_tab_active(self) -> bool:
        """Проверяет, активна ли вкладка 'More'."""
        try:
            classes = self.tab_more.get_attribute("class") or ""
            return "active" in classes
        except:
            return False

    def is_what_panel_visible(self) -> bool:
        """Проверяет, видна ли панель 'What'."""
        try:
            return self.panel_what.is_visible() and "display: none" not in (
                self.panel_what.get_attribute("style") or ""
            )
        except:
            return False

    def is_origin_panel_visible(self) -> bool:
        """Проверяет, видна ли панель 'Origin'."""
        try:
            return self.panel_origin.is_visible() and "display: none" not in (
                self.panel_origin.get_attribute("style") or ""
            )
        except:
            return False

    def is_use_panel_visible(self) -> bool:
        """Проверяет, видна ли панель 'Use'."""
        try:
            return self.panel_use.is_visible() and "display: none" not in (
                self.panel_use.get_attribute("style") or ""
            )
        except:
            return False

    def is_more_panel_visible(self) -> bool:
        """Проверяет, видна ли панель 'More'."""
        try:
            return self.panel_more.is_visible() and "display: none" not in (
                self.panel_more.get_attribute("style") or ""
            )
        except:
            return False

    def get_what_panel_content(self) -> str:
        """Получает текст содержимого панели 'What'."""
        try:
            # Ждем, пока панель станет видимой
            self.panel_what.wait_for(state="visible", timeout=3000)
            content = self.panel_what_content.text_content()
            return content.strip() if content else ""
        except:
            return ""

    def get_origin_panel_content(self) -> str:
        """Получает текст содержимого панели 'Origin'."""
        try:
            # Ждем, пока панель станет видимой
            self.panel_origin.wait_for(state="visible", timeout=3000)
            content = self.panel_origin_content.text_content()
            return content.strip() if content else ""
        except:
            return ""

    def get_use_panel_content(self) -> str:
        """Получает текст содержимого панели 'Use'."""
        try:
            # Ждем, пока панель станет видимой
            self.panel_use.wait_for(state="visible", timeout=3000)
            content = self.panel_use_content.text_content()
            return content.strip() if content else ""
        except:
            return ""

    def get_more_panel_content(self) -> str:
        """Получает текст содержимого панели 'More'."""
        try:
            content = self.panel_more_content.text_content()
            return content.strip() if content else ""
        except:
            return ""

    def is_more_tab_disabled(self) -> bool:
        """Проверяет, отключена ли вкладка 'More'."""
        try:
            classes = self.tab_more.get_attribute("class") or ""
            return "disabled" in classes
        except:
            return False

    def get_active_tab_text(self) -> str:
        """Получает текст активной вкладки."""
        try:
            if self.is_what_tab_active():
                return "What"
            elif self.is_origin_tab_active():
                return "Origin"
            elif self.is_use_tab_active():
                return "Use"
            elif self.is_more_tab_active():
                return "More"
        except:
            pass
        return ""

    def switch_to_tab_by_name(self, tab_name: str):
        """Переключается на вкладку по имени."""
        tab_map = {
            "What": self.click_what_tab,
            "Origin": self.click_origin_tab,
            "Use": self.click_use_tab,
            "More": self.click_more_tab,
        }

        if tab_name in tab_map:
            tab_map[tab_name]()
