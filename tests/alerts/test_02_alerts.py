"""
Тесты для страницы Alerts.
Проверяет функциональность различных типов JavaScript alert диалогов.
"""

import pytest
import allure


@allure.epic("Alerts, Frame & Windows")
@allure.feature("JavaScript Alerts")
@allure.story("Simple Alert")
@pytest.mark.alerts
@pytest.mark.smoke
def test_simple_alert(alerts_page):
    """
    Тест простого alert диалога.

    Шаги:
    1. Настроить обработчик alert диалога
    2. Кликнуть кнопку для вызова alert
    3. Проверить что alert был обработан
    """
    alert_text = None
    alert_triggered = False

    def handle_alert(dialog):
        nonlocal alert_text, alert_triggered
        alert_text = dialog.message
        alert_triggered = True
        dialog.accept()

    with allure.step("Настраиваем обработчик alert диалога"):
        alerts_page.page.on("dialog", handle_alert)

    with allure.step("Вызываем simple alert"):
        alerts_page.click_alert_button()

    with allure.step("Проверяем обработку alert диалога"):
        assert alert_triggered, "Alert диалог должен был быть вызван"
        assert alert_text is not None, "Alert должен содержать текст"
        assert len(alert_text) > 0, "Текст alert не должен быть пустым"

        allure.attach(alert_text, "alert_message_text")

    with allure.step("Очистка обработчика"):
        alerts_page.page.remove_listener("dialog", handle_alert)


@allure.epic("Alerts, Frame & Windows")
@allure.feature("JavaScript Alerts")
@allure.story("Timer Alert")
@pytest.mark.alerts
def test_timer_alert(alerts_page):
    """
    Тест alert диалога с задержкой в 5 секунд.

    Шаги:
    1. Настроить обработчик с увеличенным таймаутом
    2. Кликнуть кнопку timer alert
    3. Дождаться появления alert через 5 секунд
    4. Проверить успешную обработку
    """
    alert_handled = False
    alert_message = None

    def handle_timer_alert(dialog):
        nonlocal alert_handled, alert_message
        alert_message = dialog.message
        alert_handled = True
        dialog.accept()

    with allure.step("Настраиваем обработчик timer alert"):
        alerts_page.page.on("dialog", handle_timer_alert)

    with allure.step("Запускаем timer alert (ожидается задержка 5 сек)"):
        alerts_page.click_timer_alert_button()

    with allure.step("Ждем появления alert диалога"):
        # Ждем до 7 секунд для появления alert (5 сек задержка + буфер)
        alerts_page.page.wait_for_timeout(7000)

    with allure.step("Проверяем успешную обработку timer alert"):
        assert alert_handled, "Timer alert должен был появиться через 5 секунд"
        assert alert_message, "Timer alert должен содержать сообщение"

        allure.attach(alert_message, "timer_alert_message")
        allure.attach("5 seconds", "expected_delay")

    with allure.step("Очистка"):
        alerts_page.page.remove_listener("dialog", handle_timer_alert)


@allure.epic("Alerts, Frame & Windows")
@allure.feature("JavaScript Alerts")
@allure.story("Confirm Dialog")
@pytest.mark.alerts
@pytest.mark.regression
def test_confirm_accept(alerts_page):
    """
    Тест confirm диалога с выбором OK.

    Шаги:
    1. Настроить обработчик для подтверждения
    2. Вызвать confirm диалог
    3. Подтвердить диалог (OK)
    4. Проверить результат на странице
    """
    confirm_handled = False

    def handle_confirm_ok(dialog):
        nonlocal confirm_handled
        confirm_handled = True
        dialog.accept()  # Нажимаем OK

    with allure.step("Настраиваем обработчик confirm (OK)"):
        alerts_page.page.on("dialog", handle_confirm_ok)

    with allure.step("Вызываем confirm диалог"):
        alerts_page.click_confirm_button()

    with allure.step("Проверяем результат подтверждения"):
        assert confirm_handled, "Confirm диалог должен был быть обработан"

        # Проверяем результат на странице
        result_text = alerts_page.get_confirm_result()
        assert (
            "Ok" in result_text or "OK" in result_text
        ), f"Результат должен содержать 'Ok', получено: '{result_text}'"

        allure.attach(result_text, "confirm_result_text")

    with allure.step("Очистка"):
        alerts_page.page.remove_listener("dialog", handle_confirm_ok)


@allure.epic("Alerts, Frame & Windows")
@allure.feature("JavaScript Alerts")
@allure.story("Confirm Dialog")
@pytest.mark.alerts
def test_confirm_cancel(alerts_page):
    """
    Тест confirm диалога с выбором Cancel.

    Шаги:
    1. Настроить обработчик для отмены
    2. Вызвать confirm диалог
    3. Отменить диалог (Cancel)
    4. Проверить результат отмены на странице
    """
    confirm_handled = False

    def handle_confirm_cancel(dialog):
        nonlocal confirm_handled
        confirm_handled = True
        dialog.dismiss()  # Нажимаем Cancel

    with allure.step("Настраиваем обработчик confirm (Cancel)"):
        alerts_page.page.on("dialog", handle_confirm_cancel)

    with allure.step("Вызываем confirm диалог"):
        alerts_page.click_confirm_button()

    with allure.step("Проверяем результат отмены"):
        assert confirm_handled, "Confirm диалог должен был быть обработан"

        # Проверяем результат на странице
        result_text = alerts_page.get_confirm_result()
        assert (
            "Cancel" in result_text
        ), f"Результат должен содержать 'Cancel', получено: '{result_text}'"

        allure.attach(result_text, "confirm_cancel_result")

    with allure.step("Очистка"):
        alerts_page.page.remove_listener("dialog", handle_confirm_cancel)


@allure.epic("Alerts, Frame & Windows")
@allure.feature("JavaScript Alerts")
@allure.story("Prompt Dialog")
@pytest.mark.alerts
@pytest.mark.parametrize(
    "test_text,expected_result",
    [
        ("Hello World", "Hello World"),
        ("Test123", "Test123"),
        ("", ""),  # Пустой ввод
        ("Special chars: @#$%", "Special chars: @#$%"),
    ],
)
def test_prompt_with_text(alerts_page, test_text, expected_result):
    """
    Параметризованный тест prompt диалога с вводом текста.

    Проверяет различные варианты текстового ввода в prompt.
    """
    prompt_handled = False
    prompt_message = None

    def handle_prompt(dialog):
        nonlocal prompt_handled, prompt_message
        prompt_message = dialog.message
        prompt_handled = True
        dialog.accept(test_text)  # Вводим тестовый текст

    with allure.step(f"Настраиваем обработчик prompt с текстом: '{test_text}'"):
        alerts_page.page.on("dialog", handle_prompt)

    with allure.step("Вызываем prompt диалог"):
        alerts_page.click_prompt_button()

    with allure.step("Проверяем результат ввода в prompt"):
        assert prompt_handled, "Prompt диалог должен был быть обработан"

        # Проверяем результат на странице
        result_text = alerts_page.get_prompt_result()

        if test_text:
            assert (
                expected_result in result_text
            ), f"Результат должен содержать '{expected_result}', получено: '{result_text}'"
        else:
            # Для пустого ввода может быть специальное сообщение
            assert result_text, "Должен быть какой-то результат даже для пустого ввода"

        allure.attach(test_text, "input_text")
        allure.attach(result_text, "prompt_result")

    with allure.step("Очистка"):
        alerts_page.page.remove_listener("dialog", handle_prompt)


@allure.epic("Alerts, Frame & Windows")
@allure.feature("JavaScript Alerts")
@allure.story("Prompt Dialog")
@pytest.mark.alerts
def test_prompt_cancel(alerts_page):
    """
    Тест prompt диалога с отменой.

    Шаги:
    1. Настроить обработчик для отмены prompt
    2. Вызвать prompt диалог
    3. Отменить prompt (Cancel)
    4. Проверить результат отмены
    """
    prompt_handled = False

    def handle_prompt_cancel(dialog):
        nonlocal prompt_handled
        prompt_handled = True
        dialog.dismiss()  # Отменяем prompt

    with allure.step("Настраиваем обработчик prompt (Cancel)"):
        alerts_page.page.on("dialog", handle_prompt_cancel)

    with allure.step("Вызываем prompt диалог"):
        alerts_page.click_prompt_button()

    with allure.step("Проверяем результат отмены prompt"):
        assert prompt_handled, "Prompt диалог должен был быть обработан"

        # Проверяем результат на странице
        result_text = alerts_page.get_prompt_result()
        # При отмене prompt обычно результат содержит null или cancel
        assert result_text, "Должен быть результат отмены prompt"

        allure.attach(result_text, "prompt_cancel_result")

    with allure.step("Очистка"):
        alerts_page.page.remove_listener("dialog", handle_prompt_cancel)
