from utils.helper import wait_for_progress
import re


def test_progress_bar_stops_and_resets(progress_page):
    # Небольшая задержка для стабилизации
    progress_page.page.wait_for_timeout(1000)

    # Проверка начального состояния
    assert (
        progress_page.get_button_text() == "Start"
    ), "Кнопка должна быть 'Start' в начале"

    progress_page.start_progress()

    # Небольшая задержка после клика
    progress_page.page.wait_for_timeout(500)

    # Проверка после запуска
    assert (
        progress_page.get_button_text() == "Stop"
    ), "Кнопка должна стать 'Stop' после запуска"

    wait_for_progress(progress_page, target="50%", timeout=60)
    progress_page.stop_progress()

    # Увеличенная задержка после остановки
    progress_page.page.wait_for_timeout(3000)

    partial_result = progress_page.get_progress_value()
    assert re.search(r"(50|51)%", partial_result)

    # Проверка после остановки
    assert (
        progress_page.get_button_text() == "Start"
    ), "Кнопка должна вернуться к 'Start' после остановки"

    progress_page.start_progress()
    # Небольшая задержка после второго запуска
    progress_page.page.wait_for_timeout(500)

    wait_for_progress(progress_page, target="100%", timeout=30)

    full_result = progress_page.get_progress_value()
    assert "100%" in full_result

    progress_page.reset_progress()
    # Увеличенная задержка после сброса
    progress_page.page.wait_for_timeout(1000)

    wait_for_progress(progress_page, target="0%", timeout=30)
    reset_result = progress_page.get_progress_value()
    assert reset_result == "0%"

    # Проверка после сброса
    assert (
        progress_page.get_button_text() == "Start"
    ), "После сброса кнопка должна быть 'Start'"
