"""
Page Object для страницы Resizable.
Содержит методы для изменения размеров элементов через drag handle.
"""

from playwright.sync_api import Page
from locators.interactions.resizable_locators import ResizableLocators
from pages.base_page import BasePage


class ResizablePage(BasePage):
    """
    Страница тестирования изменения размеров элементов.
    Содержит resizable box с ограничениями и без ограничений.
    """

    def __init__(self, page: Page):
        """
        Инициализация страницы Resizable.

        Args:
            page: Экземпляр страницы Playwright
        """
        super().__init__(page)

    def resize_box_with_restriction(self, x_offset: int, y_offset: int) -> None:
        """
        Изменяет размер ограниченного resizable box.

        Args:
            x_offset: Изменение ширины в пикселях
            y_offset: Изменение высоты в пикселях

        Postconditions: размер box изменен в пределах ограничений (150x150 - 500x300)
        """
        self.log_step(f"Изменяем размер ограниченного box на ({x_offset}, {y_offset})")
        resize_handle = self.page.locator(ResizableLocators.RESIZE_HANDLE_RESTRICTED)

        # Получаем позицию handle
        handle_box = resize_handle.bounding_box()
        handle_x = handle_box["x"] + handle_box["width"] / 2
        handle_y = handle_box["y"] + handle_box["height"] / 2

        # Выполняем drag для resize
        self.page.mouse.move(handle_x, handle_y)
        self.page.mouse.down()
        self.page.mouse.move(handle_x + x_offset, handle_y + y_offset, steps=5)
        self.page.mouse.up()

    def resize_box_no_restriction(self, x_offset: int, y_offset: int) -> None:
        """
        Изменяет размер неограниченного resizable box.

        Args:
            x_offset: Изменение ширины в пикселях
            y_offset: Изменение высоты в пикселях

        Postconditions: размер box изменен без ограничений
        """
        self.log_step(
            f"Изменяем размер неограниченного box на ({x_offset}, {y_offset})"
        )
        resize_handle = self.page.locator(
            ResizableLocators.RESIZE_HANDLE_NO_RESTRICTION
        )

        handle_box = resize_handle.bounding_box()
        handle_x = handle_box["x"] + handle_box["width"] / 2
        handle_y = handle_box["y"] + handle_box["height"] / 2

        self.page.mouse.move(handle_x, handle_y)
        self.page.mouse.down()
        self.page.mouse.move(handle_x + x_offset, handle_y + y_offset, steps=5)
        self.page.mouse.up()

    def get_restricted_box_size(self) -> tuple[int, int]:
        """
        Получает текущий размер ограниченного resizable box.

        Returns:
            tuple: (ширина, высота) в пикселях
        """
        box = self.page.locator(ResizableLocators.RESIZABLE_BOX_RESTRICTED)
        bounding_box = box.bounding_box()
        return int(bounding_box["width"]), int(bounding_box["height"])

    def get_no_restriction_box_size(self) -> tuple[int, int]:
        """
        Получает текущий размер неограниченного resizable box.

        Returns:
            tuple: (ширина, высота) в пикселях
        """
        box = self.page.locator(ResizableLocators.RESIZABLE_BOX_NO_RESTRICTION)
        bounding_box = box.bounding_box()
        return int(bounding_box["width"]), int(bounding_box["height"])

    def is_resize_handle_visible(self, restricted: bool = True) -> bool:
        """
        Проверяет видимость resize handle.

        Args:
            restricted: True для ограниченного box, False для неограниченного

        Returns:
            bool: True если handle видим
        """
        locator = (
            ResizableLocators.RESIZE_HANDLE_RESTRICTED
            if restricted
            else ResizableLocators.RESIZE_HANDLE_NO_RESTRICTION
        )
        return self.page.locator(locator).is_visible()
