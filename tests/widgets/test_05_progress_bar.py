from utils.helper import wait_for_progress


def test_progress_bar_stops_and_resets(progress_bar_page):
    progress_bar_page.page.wait_for_timeout(2000)

    assert (
        progress_bar_page.get_button_text() == "Start"
    ), "Кнопка должна быть 'Start' в начале"
    assert (
        progress_bar_page.get_progress_value() == "0%"
    ), "Начальное значение прогресса должно быть 0%"

    progress_bar_page.start_progress()
    progress_bar_page.page.wait_for_timeout(1000)
    assert (
        progress_bar_page.get_button_text() == "Stop"
    ), "Кнопка должна смениться на 'Stop' после запуска"

    try:
        wait_for_progress(progress_bar_page, "50%", timeout=90)
    except TimeoutError as e:
        current_value = progress_bar_page.get_progress_value()
        current_percent = int("".join(filter(str.isdigit, current_value)))
        assert (
            45 <= current_percent <= 55
        ), f"Прогресс около 50%, получено {current_value}"

    progress_bar_page.stop_progress()
    progress_bar_page.page.wait_for_timeout(5000)
    partial_result = progress_bar_page.get_progress_value()
    partial_percent = int("".join(filter(str.isdigit, partial_result)))
    assert 45 <= partial_percent <= 55, "Значение после стопа около 50%"

    assert (
        progress_bar_page.get_button_text() == "Start"
    ), "Кнопка должна вернуться к 'Start' после стопа"

    progress_bar_page.start_progress()
    progress_bar_page.page.wait_for_timeout(1000)
    try:
        wait_for_progress(progress_bar_page, "100%", timeout=45)
    except TimeoutError:
        current_value = progress_bar_page.get_progress_value()
        current_percent = int("".join(filter(str.isdigit, current_value)))
        assert current_percent >= 95, f"Прогресс около 100%, получено {current_value}"

    full_result = progress_bar_page.get_progress_value()
    full_percent = int("".join(filter(str.isdigit, full_result)))
    assert full_percent >= 95, "Значение должно быть около 100%"

    progress_bar_page.reset_progress()
    progress_bar_page.page.wait_for_timeout(30000)
    try:
        wait_for_progress(progress_bar_page, "0%", timeout=30)
    except TimeoutError:
        reset_value = progress_bar_page.get_progress_value()
        reset_percent = int("".join(filter(str.isdigit, reset_value)))
        assert (
            reset_percent <= 5
        ), f"Прогресс должен сброситься до 0%, текущее значение: {reset_value}"

    reset_result = progress_bar_page.get_progress_value()
    reset_percent = int("".join(filter(str.isdigit, reset_result)))

    assert reset_percent <= 5, "Значение после сброса около 0%"

    assert (
        progress_bar_page.get_button_text() == "Start"
    ), "Кнопка должна быть 'Start' после сброса"
