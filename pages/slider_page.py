from playwright.sync_api import Page
from locators.slider_locators import SLIDER_HANDLE


class SliderPage:
    def __init__(self, page: Page):
        self.page = page
        self.slider_handle = page.locator(SLIDER_HANDLE)
        self.page.wait_for_timeout(1000)  # Даем странице загрузиться

    def get_current_value(self) -> str:
        """Возвращает значение из input.value — это источник истины"""
        value = self.page.evaluate(
            """
            const input = document.querySelector('.range-slider');
            if (input && input.value !== null && input.value !== undefined) {
                input.value;
            } else {
                "0";
            }
        """
        )
        return str(value).strip() if value is not None else "0"

    def set_value(self, target_value: int) -> None:
        if not isinstance(target_value, int) or target_value < 0 or target_value > 100:
            raise ValueError(
                f"Значение должно быть целым числом от 0 до 100, получено: {target_value}"
            )

        print(
            f"[DEBUG] Setting value {target_value} via JS (setting both input.value and --value)"
        )

        self.page.evaluate(
            f"""
            const input = document.querySelector('{SLIDER_HANDLE}');
            if (input) {{
                input.value = {target_value};
                input.style.setProperty('--value', '{target_value}');
                input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                input.dispatchEvent(new Event('change', {{ bubbles: true }}));
                input.dispatchEvent(new Event('mouseup', {{ bubbles: true }}));
                input.dispatchEvent(new Event('blur', {{ bubbles: true }}));
            }}
        """
        )

        # Ждём, пока input.value действительно установится — это наша цель
        self.page.wait_for_function(
            f"""
            () => {{
                const input = document.querySelector('{SLIDER_HANDLE}');
                return input && input.value === '{target_value}';
            }}
        """,
            timeout=5000,
        )

    def move_to_max(self) -> None:
        self.set_value(100)

    def move_to_min(self) -> None:
        self.set_value(0)

    def move_to_middle(self) -> None:
        self.set_value(50)

    def focus_and_press_arrow_right(self) -> None:
        self.slider_handle.focus()
        self.page.press(SLIDER_HANDLE, "ArrowRight")
        self.page.wait_for_timeout(300)

    def focus_and_press_arrow_left(self) -> None:
        self.slider_handle.focus()
        self.page.press(SLIDER_HANDLE, "ArrowLeft")
        self.page.wait_for_timeout(300)
