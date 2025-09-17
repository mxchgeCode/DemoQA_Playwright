import pytest


def test_simple_alert(alerts_page):
    alerts_page.click_simple_alert()


def test_timer_alert(alerts_page):
    alerts_page.click_timer_alert()


@pytest.mark.parametrize(
    "accept_alert, expected_text",
    [
        (True, "You selected Ok"),
        (False, "You selected Cancel"),
    ],
)
def test_confirm_alert(alerts_page, accept_alert, expected_text):
    # Переопределяем обработчик для подтверждения, потому что глобальный принимает все
    def handle_dialog(dialog):
        assert dialog.type == "confirm"
        if accept_alert:
            dialog.accept()
        else:
            dialog.dismiss()

    alerts_page.page.once("dialog", handle_dialog)
    alerts_page.click_confirm_alert()
    text = alerts_page.get_confirm_result()
    assert expected_text in text


def test_prompt_alert(alerts_page):
    prompt_text = "Hello Playwright"

    def handle_dialog(dialog):
        assert dialog.type == "prompt"
        dialog.accept(prompt_text)

    alerts_page.page.once("dialog", handle_dialog)
    alerts_page.click_prompt_alert()
    result = alerts_page.get_prompt_result()
    assert prompt_text in result
