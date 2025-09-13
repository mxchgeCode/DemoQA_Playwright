# pages/tool_tips_page.py
from playwright.sync_api import Page
from locators.tool_tips_locators import ToolTipsLocators


class ToolTipsPage:
    def __init__(self, page: Page):
        self.page = page
        # Основной контейнер
        self.main_container = page.locator(ToolTipsLocators.MAIN_CONTAINER)

        # Элементы, на которые наводим
        self.hover_button = page.locator(ToolTipsLocators.HOVER_BUTTON)
        self.hover_field = page.locator(ToolTipsLocators.HOVER_FIELD)
        self.hover_link = page.locator(ToolTipsLocators.HOVER_LINK)
        self.text_container = page.locator(ToolTipsLocators.TEXT_CONTAINER)

        # Тултипы (могут быть динамическими)
        self.tooltip_button = page.locator(ToolTipsLocators.TOOLTIP_BUTTON)
        self.tooltip_field = page.locator(ToolTipsLocators.TOOLTIP_FIELD)
        self.tooltip_link = page.locator(ToolTipsLocators.TOOLTIP_LINK)
        self.tooltip_text = page.locator(ToolTipsLocators.TOOLTIP_TEXT)

    def is_page_loaded(self) -> bool:
        try:
            return self.main_container.is_visible()
        except:
            return False

    # --- Hover Actions ---
    def hover_over_button(self):
        """Наводит курсор на кнопку."""
        self.hover_button.hover()
        self.page.wait_for_timeout(500)

    def hover_over_field(self):
        """Наводит курсор на поле ввода."""
        self.hover_field.hover()
        self.page.wait_for_timeout(500)

    def hover_over_link(self):
        """Наводит курсор на ссылку."""
        self.hover_link.hover()
        self.page.wait_for_timeout(500)

    def hover_over_text_container(self):
        """Наводит курсор на текстовый контейнер."""
        self.text_container.hover()
        self.page.wait_for_timeout(500)

    def move_mouse_away(self):
        """Перемещает курсор в сторону, чтобы тултипы исчезли."""
        # Кликаем в левый верхний угол страницы
        self.page.mouse.move(10, 10)
        self.page.wait_for_timeout(500)

    # --- Tooltip Visibility ---
    def is_button_tooltip_visible(self) -> bool:
        """Проверяет, виден ли тултип кнопки."""
        try:
            self.tooltip_button.wait_for(state="visible", timeout=3000)
            return True
        except:
            return False

    def is_field_tooltip_visible(self) -> bool:
        """Проверяет, виден ли тултип поля."""
        try:
            self.tooltip_field.wait_for(state="visible", timeout=3000)
            return True
        except:
            return False

    def is_link_tooltip_visible(self) -> bool:
        """Проверяет, виден ли тултип ссылки."""
        try:
            self.tooltip_link.wait_for(state="visible", timeout=3000)
            return True
        except:
            return False

    def is_text_tooltip_visible(self) -> bool:
        """Проверяет, виден ли тултип текста."""
        try:
            self.tooltip_text.wait_for(state="visible", timeout=3000)
            return True
        except:
            return False

    # --- Tooltip Text ---
    def get_button_tooltip_text(self) -> str:
        """Получает текст тултипа кнопки."""
        try:
            self.tooltip_button.wait_for(state="visible", timeout=5000)
            return self.tooltip_button.text_content().strip()
        except Exception as e:
            print(f"Ошибка получения текста тултипа кнопки: {e}")
            return ""

    def get_field_tooltip_text(self) -> str:
        """Получает текст тултипа поля."""
        try:
            self.tooltip_field.wait_for(state="visible", timeout=5000)
            return self.tooltip_field.text_content().strip()
        except Exception as e:
            print(f"Ошибка получения текста тултипа поля: {e}")
            return ""

    def get_link_tooltip_text(self) -> str:
        """Получает текст тултипа ссылки."""
        try:
            self.tooltip_link.wait_for(state="visible", timeout=5000)
            return self.tooltip_link.text_content().strip()
        except Exception as e:
            print(f"Ошибка получения текста тултипа ссылки: {e}")
            return ""

    def get_text_container_tooltip_text(self) -> str:
        """Получает текст тултипа текстового контейнера."""
        try:
            self.tooltip_text.wait_for(state="visible", timeout=5000)
            return self.tooltip_text.text_content().strip()
        except Exception as e:
            print(f"Ошибка получения текста тултипа текста: {e}")
            # fallback: пробуем найти тултип глобально по тексту
            try:
                fallback_tooltip = self.page.locator("div[role='tooltip']").first
                fallback_tooltip.wait_for(state="visible", timeout=2000)
                return fallback_tooltip.text_content().strip()
            except:
                return ""
