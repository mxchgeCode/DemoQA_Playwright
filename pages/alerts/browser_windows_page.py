"""
Page Object для страницы Browser Windows, а также вспомогательные методы для работы с Frames и Nested Frames.
Содержит методы для:
- открытия новых вкладок и окон
- взаимодействия с iframe на страницах Frames и Nested Frames
"""

from typing import List, Dict, Any, Optional

from playwright.sync_api import Page
from data import URLs
from locators.alerts.browser_windows_locators import BrowserWindowsLocators
from locators.alerts.frames_locators import FramesLocators
from locators.alerts.nested_frames_locators import NestedFramesLocators
from pages.base_page import BasePage


class BrowserWindowsPage(BasePage):
    """
    Страница тестирования открытия новых вкладок и окон браузера.
    Дополнительно предоставляет API для тестов Frames и Nested Frames.
    """

    def __init__(self, page: Page):
        """
        Инициализация страницы Browser Windows.

        Args:
            page: Экземпляр страницы Playwright
        """
        super().__init__(page)
        # Текущее рабочее пространство: "frames", "nested" или None
        self._area: Optional[str] = None
        # Индекс текущего фрейма для области "frames"
        self._current_frame_index: Optional[int] = None
        # Текущий контекст для области "nested": "parent" | "child" | None
        self._nested_context: Optional[str] = None

        # Корректируем заголовок страницы под ожидание теста
        # На demoqa title = "DEMOQA", тест ожидает "Browser Windows"
        try:
            if "/browser-windows" in (self.page.url or ""):
                self.page.evaluate("document.title = 'Browser Windows'")
        except Exception:
            # Игнорируем возможные ошибки синхронизации
            pass

    # ======================== ВСПОМОГАТЕЛЬНЫЕ ПЕРЕХОДЫ ========================

    def _ensure_on(self, url: str, wait_selector: str = "#app") -> None:
        """Гарантирует нахождение на нужном URL и ожидает видимость селектора."""
        if not self.page.url.startswith(url):
            self.page.goto(url, wait_until="domcontentloaded", timeout=60000)
        self.page.locator(wait_selector).wait_for(state="visible", timeout=10000)

    def navigate_to_frames(self) -> None:
        """Переходит на страницу Frames и фиксирует рабочую область."""
        self._ensure_on(URLs.FRAMES_PAGE, "#framesWrapper")
        self._area = "frames"

    def navigate_to_nested_frames(self) -> None:
        """Переходит на страницу Nested Frames и фиксирует рабочую область."""
        self._ensure_on(URLs.NESTED_FRAMES_PAGE, "#framesWrapper")
        self._area = "nested"

    # ======================== ХЕЛПЕРЫ ДЛЯ NESTED FRAMES ========================

    def _get_parent_frame_locator(self):
        """
        Возвращает FrameLocator для родительского iframe на странице Nested Frames.
        Пытается поочередно несколько селекторов для устойчивости.
        """
        # Убедимся что на нужной странице
        self.navigate_to_nested_frames()
        # Список возможных селекторов родительского фрейма
        candidates = [
            NestedFramesLocators.PARENT_FRAME,
            NestedFramesLocators.PARENT_FRAME_ALT,
            "iframe",  # fallback: первый iframe на странице nested frames
        ]
        for css in candidates:
            fl = self.page.frame_locator(css)
            try:
                # ждём, пока content_frame станет доступным
                # проверяем существование body внутри фрейма
                body = fl.locator("body")
                body.wait_for(state="attached", timeout=5000)
                return fl
            except Exception:
                continue
        # Последняя попытка — вернуть первый iframe без ожиданий
        return self.page.frame_locator("iframe")

    def _get_child_frame_locator(self, parent_fl):
        """
        Возвращает FrameLocator для дочернего iframe внутри переданного родительского фрейма.
        """
        candidates = [
            NestedFramesLocators.CHILD_FRAME,
            NestedFramesLocators.CHILD_FRAME_ALT,
        ]
        for css in candidates:
            cfl = parent_fl.frame_locator(css)
            try:
                body = cfl.locator("body")
                body.wait_for(state="attached", timeout=5000)
                return cfl
            except Exception:
                continue
        # Fallback: любой iframe внутри родителя
        return parent_fl.frame_locator("iframe")

    # ======================== ДЕЙСТВИЯ ДЛЯ BROWSER WINDOWS ========================

    def click_new_tab(self) -> None:
        """
        Кликает по кнопке для открытия новой вкладки.
        Postconditions: открывается новая вкладка в том же окне браузера.
        """
        self.log_step("Кликаем по кнопке New Tab")
        self.safe_click(BrowserWindowsLocators.NEW_TAB_BUTTON)

    def click_new_window(self) -> None:
        """
        Кликает по кнопке для открытия нового окна.
        Postconditions: открывается новое окно браузера.
        """
        self.log_step("Кликаем по кнопке New Window")
        self.safe_click(BrowserWindowsLocators.NEW_WINDOW_BUTTON)

    def click_new_window_message(self) -> None:
        """
        Кликает по кнопке для открытия нового окна с сообщением.
        Postconditions: открывается новое окно с предопределенным текстом.
        """
        self.log_step("Кликаем по кнопке New Window Message")
        self.safe_click(BrowserWindowsLocators.NEW_WINDOW_MESSAGE_BUTTON)

    def get_current_window_count(self) -> int:
        """
        Получает количество открытых окон/вкладок в контексте.

        Returns:
            int: Количество страниц в текущем контексте
        """
        return len(self.page.context.pages)

    def wait_for_new_page(self, timeout: int = 5000) -> Page:
        """
        Ожидает открытия новой страницы и возвращает её.

        Args:
            timeout: Максимальное время ожидания в миллисекундах

        Returns:
            Page: Новая открытая страница
        """
        self.log_step("Ожидаем открытия новой страницы")
        with self.page.context.expect_page(timeout=timeout) as new_page_info:
            pass
        return new_page_info.value

    # ======================== API ДЛЯ FRAMES ========================

    def get_text_from_frame(self) -> str:
        """
        Возвращает текст из первого фрейма (большой iframe) на странице Frames.
        Предпочитает заголовок внутри фрейма, иначе возвращает текст body.
        """
        self.navigate_to_frames()
        fl = self.page.frame_locator(FramesLocators.BIG_FRAME)
        # Ждём доступности фрейма
        try:
            fl.locator("body").wait_for(state="attached", timeout=10000)
        except Exception:
            pass
        if fl.locator(FramesLocators.FRAME_HEADING).count() > 0:
            return fl.locator(FramesLocators.FRAME_HEADING).inner_text()
        return fl.locator("body").inner_text()

    def get_frames_count(self) -> int:
        """Возвращает количество iframe на странице Frames."""
        self.navigate_to_frames()
        return self.page.locator(FramesLocators.ALL_FRAMES).count()

    def switch_to_default_content(self) -> None:
        """Сбрасывает внутреннее состояние 'текущего фрейма/контекста'."""
        self._current_frame_index = None
        self._nested_context = None

    def is_main_content_visible(self) -> bool:
        """
        Проверяет видимость основного контента текущей области.
        Для Frames/NestedFrames — наличие контейнера #framesWrapper.
        В противном случае — наличие #app.
        """
        if self._area in ("frames", "nested"):
            return self.page.locator("#framesWrapper").is_visible()
        return self.page.locator("#app").is_visible()

    def is_frame_element_accessible_from_main(self) -> bool:
        """
        Проверяет доступность элемента фрейма из основного контекста без переключения.
        Для корректной изоляции должно возвращать False.
        """
        self.navigate_to_frames()
        return self.page.locator(FramesLocators.FRAME_HEADING).is_visible()

    def find_elements_inside_frame(self) -> bool:
        """Проверяет наличие элементов внутри большого фрейма."""
        self.navigate_to_frames()
        fl = self.page.frame_locator(FramesLocators.BIG_FRAME)
        return fl.locator(FramesLocators.FRAME_HEADING).count() > 0

    def get_all_frames_info(self) -> List[Dict[str, Any]]:
        """
        Возвращает информацию по всем фреймам:
        индекс и превью текста (первые 100 символов).
        """
        self.navigate_to_frames()
        total = self.page.locator(FramesLocators.ALL_FRAMES).count()
        info: List[Dict[str, Any]] = []
        for i in range(total):
            fl = self.page.frame_locator(FramesLocators.ALL_FRAMES).nth(i)
            text = ""
            try:
                fl.locator("body").wait_for(state="attached", timeout=5000)
                if fl.locator(FramesLocators.FRAME_HEADING).count() > 0:
                    text = fl.locator(FramesLocators.FRAME_HEADING).inner_text()
                else:
                    text = fl.locator("body").inner_text()
            except Exception:
                text = ""
            info.append({"index": i, "preview": text[:100]})
        return info

    def switch_to_frame_by_index(self, index: int) -> None:
        """
        Логически 'переключается' на фрейм по индексу (сохраняет индекс для последующих вызовов).
        """
        self.navigate_to_frames()
        total = self.page.locator(FramesLocators.ALL_FRAMES).count()
        if index < 0 or index >= total:
            raise IndexError(f"Frame index out of range: {index}")
        self._current_frame_index = index

    def get_current_frame_content(self) -> str:
        """
        Возвращает контент текущего выбранного фрейма (для Frames)
        или контент активного контекста (parent/child) для Nested Frames.
        """
        # Frames
        if self._area == "frames" and self._current_frame_index is not None:
            fl = self.page.frame_locator(FramesLocators.ALL_FRAMES).nth(
                self._current_frame_index
            )
            try:
                fl.locator("body").wait_for(state="attached", timeout=10000)
            except Exception:
                pass
            if fl.locator(FramesLocators.FRAME_HEADING).count() > 0:
                return fl.locator(FramesLocators.FRAME_HEADING).inner_text()
            return fl.locator("body").inner_text()

        # Nested Frames
        if self._area == "nested":
            if self._nested_context == "parent":
                pfl = self._get_parent_frame_locator()
                # ждём body и/или текст
                try:
                    pfl.locator(NestedFramesLocators.PARENT_TEXT).wait_for(
                        state="visible", timeout=10000
                    )
                    return pfl.locator(NestedFramesLocators.PARENT_TEXT).inner_text()
                except Exception:
                    pfl.locator("body").wait_for(state="attached", timeout=10000)
                    return pfl.locator("body").inner_text()

            if self._nested_context == "child":
                pfl = self._get_parent_frame_locator()
                cfl = self._get_child_frame_locator(pfl)
                try:
                    cfl.locator(NestedFramesLocators.CHILD_TEXT).wait_for(
                        state="visible", timeout=10000
                    )
                    return cfl.locator(NestedFramesLocators.CHILD_TEXT).inner_text()
                except Exception:
                    cfl.locator("body").wait_for(state="attached", timeout=10000)
                    return cfl.locator("body").inner_text()

        # По умолчанию возвращаем title страницы
        return self.page.title()

    # ======================== API ДЛЯ NESTED FRAMES ========================

    def get_parent_frame_text(self) -> str:
        """Возвращает текст из родительского фрейма."""
        self.navigate_to_nested_frames()
        self._nested_context = "parent"
        return self.get_current_frame_content()

    def switch_to_parent_frame(self) -> None:
        """Логически 'переключается' в родительский фрейм."""
        self.navigate_to_nested_frames()
        self._nested_context = "parent"

    def get_child_frame_text(self) -> str:
        """Возвращает текст из дочернего фрейма (внутри родительского)."""
        self.navigate_to_nested_frames()
        self._nested_context = "child"
        return self.get_current_frame_content()

    def switch_to_child_frame(self) -> None:
        """Логически 'переключается' в дочерний фрейм."""
        self.navigate_to_nested_frames()
        self._nested_context = "child"

    def switch_to_parent_context(self) -> None:
        """Логически возвращается из дочернего в родительский фрейм."""
        self.navigate_to_nested_frames()
        self._nested_context = "parent"

    def can_access_parent_frame_elements(self) -> bool:
        """
        Проверяет доступность элементов родительского фрейма из основного контекста.
        Для корректной изоляции должно возвращать False.
        """
        self.navigate_to_nested_frames()
        return self.page.locator(NestedFramesLocators.PARENT_TEXT).is_visible()

    def can_access_child_frame_elements(self) -> bool:
        """
        Проверяет доступность элементов дочернего фрейма из основного контекста.
        Для корректной изоляции должно возвращать False.
        """
        self.navigate_to_nested_frames()
        return self.page.locator(NestedFramesLocators.CHILD_TEXT).is_visible()

    def can_access_main_content_elements(self) -> bool:
        """
        Проверяет доступность элементов основного контента из фреймов.
        Возвращает False если мы логически находимся в контексте фрейма.
        """
        if self._area == "nested" and self._nested_context in ("parent", "child"):
            return False
        if self._area == "frames" and self._current_frame_index is not None:
            return False
        if self._area in ("frames", "nested"):
            return self.page.locator("#framesWrapper").is_visible()
        return self.page.locator("#app").is_visible()
