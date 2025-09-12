# pages/tool_tips_page.py
from playwright.sync_api import Page
from locators.tool_tips_locators import ToolTipsLocators


class ToolTipsPage:
    def __init__(self, page: Page):
        self.page = page

        # Hover elements
        self.hover_button = page.locator(ToolTipsLocators.HOVER_BUTTON)
        self.hover_field = page.locator(ToolTipsLocators.HOVER_FIELD)
        self.hover_link = page.locator(ToolTipsLocators.HOVER_LINK)
        self.hover_section_link = page.locator(ToolTipsLocators.HOVER_SECTION_LINK)

        # Tooltip elements
        self.tooltip = page.locator(ToolTipsLocators.TOOLTIP)
        self.tooltip_text = page.locator(ToolTipsLocators.TOOLTIP_TEXT)

    def hover_over_button(self):
        """Наводит курсор на кнопку."""
        self.hover_button.hover()
        self.page.wait_for_timeout(1000)

    def hover_over_field(self):
        """Наводит курсор на поле ввода."""
        self.hover_field.hover()
        self.page.wait_for_timeout(1000)

    def hover_over_link(self):
        """Наводит курсор на ссылку."""
        self.hover_link.hover()
        self.page.wait_for_timeout(1000)

    def hover_over_section_link(self):
        """Наводит курсор на ссылку в секции."""
        self.hover_section_link.hover()
        self.page.wait_for_timeout(1000)

    def is_tooltip_visible(self) -> bool:
        """Проверяет, виден ли тултип."""
        try:
            return self.tooltip.is_visible()
        except:
            return False

    def get_tooltip_text(self) -> str:
        """Получает текст тултипа."""
        try:
            if self.tooltip_text.is_visible():
                return self.tooltip_text.text_content().strip()
            return ""
        except:
            return ""

    def wait_for_tooltip(self, timeout: int = 5000):
        """Ждет появления тултипа."""
        try:
            self.tooltip.wait_for(state="visible", timeout=timeout)
            return True
        except:
            return False

    def wait_for_tooltip_hidden(self, timeout: int = 5000):
        """Ждет скрытия тултипа."""
        try:
            self.tooltip.wait_for(state="hidden", timeout=timeout)
            return True
        except:
            return False

    def get_button_text(self) -> str:
        """Получает текст кнопки."""
        try:
            return self.hover_button.text_content().strip()
        except:
            return ""

    def get_field_placeholder(self) -> str:
        """Получает placeholder поля ввода."""
        try:
            return self.hover_field.get_attribute("placeholder") or ""
        except:
            return ""

    def move_mouse_away(self):
        """Перемещает мышь в сторону, чтобы скрыть тултип."""
        try:
            # Наводим на произвольный элемент, чтобы скрыть тултип
            self.page.locator("body").hover(position={"x": 0, "y": 0})
            self.page.wait_for_timeout(500)
        except:
            pass
