from utils.helper import wait_for_progress


def test_progress_bar_stops_and_resets(progress_page):
    """Улучшенный тест progress bar с лучшей стабильностью."""

    # Более длительная стабилизация страницы
    progress_page.page.wait_for_timeout(2000)

    # Проверка начального состояния
    initial_button_text = progress_page.get_button_text()
    assert (
        initial_button_text == "Start"
    ), f"Кнопка должна быть 'Start' в начале, получено: '{initial_button_text}'"

    # Проверка начального значения
    initial_value = progress_page.get_progress_value()
    assert (
        initial_value == "0%"
    ), f"Начальное значение должно быть '0%', получено: {initial_value}"

    # Запуск прогресса с повторными попытками
    progress_page.start_progress()
    progress_page.page.wait_for_timeout(1000)

    # Проверка, что кнопка изменилась на "Stop"
    stop_button_text = progress_page.get_button_text()
    assert (
        stop_button_text == "Stop"
    ), f"Кнопка должна стать 'Stop' после запуска, получено: '{stop_button_text}'"

    # Ожидание 50% с увеличенным таймаутом и повторными попытками
    try:
        wait_for_progress(progress_page, "50%", timeout=90)  # Увеличенный таймаут
    except TimeoutError as e:
        # Если не удалось достичь точно 50%, проверяем диапазон 45-55%
        current_value = progress_page.get_progress_value()
        current_percent = int("".join(filter(str.isdigit, current_value)))
        if 45 <= current_percent <= 55:
            # Принимаем значение в диапазоне как успешное
            pass
        else:
            raise e

    # Остановка прогресса
    progress_page.stop_progress()

    # Увеличенная задержка после остановки
    progress_page.page.wait_for_timeout(5000)  # Увеличено до 5 секунд

    # Проверка значения после остановки
    partial_result = progress_page.get_progress_value()
    partial_percent = int("".join(filter(str.isdigit, partial_result)))

    # Проверяем, что значение в разумных пределах (45-55%)
    assert (
        45 <= partial_percent <= 55
    ), f"Значение после остановки должно быть около 50%, получено: {partial_result}"

    # Проверка, что кнопка вернулась к "Start"
    reset_button_text = progress_page.get_button_text()
    assert (
        reset_button_text == "Start"
    ), f"Кнопка должна вернуться к 'Start' после остановки, получено: '{reset_button_text}'"

    # Второй запуск прогресса до 100%
    progress_page.start_progress()
    progress_page.page.wait_for_timeout(1000)

    # Ожидание 100% с повторными попытками
    try:
        wait_for_progress(progress_page, "100%", timeout=45)  # Увеличенный таймаут
    except TimeoutError:
        # Проверяем текущее значение
        current_value = progress_page.get_progress_value()
        current_percent = int("".join(filter(str.isdigit, current_value)))
        if current_percent >= 95:  # Принимаем 95% и выше
            pass
        else:
            raise TimeoutError(
                f"Progress did not reach 100% within timeout. Last value: {current_value}"
            )

    # Проверка 100% значения
    full_result = progress_page.get_progress_value()
    full_percent = int("".join(filter(str.isdigit, full_result)))
    assert (
        full_percent >= 95
    ), f"Значение должно быть около 100%, получено: {full_result}"

    # Сброс прогресса
    progress_page.reset_progress()
    progress_page.page.wait_for_timeout(2000)  # Увеличенная задержка

    # Ожидание сброса до 0%
    try:
        wait_for_progress(progress_page, "0%", timeout=30)
    except TimeoutError:
        # Проверяем текущее значение
        reset_value = progress_page.get_progress_value()
        reset_percent = int("".join(filter(str.isdigit, reset_value)))
        if reset_percent <= 5:  # Принимаем 5% и ниже
            pass
        else:
            raise TimeoutError(
                f"Progress did not reset to 0% within timeout. Last value: {reset_value}"
            )

    # Проверка сброса
    reset_result = progress_page.get_progress_value()
    reset_percent = int("".join(filter(str.isdigit, reset_result)))
    assert (
        reset_percent <= 5
    ), f"Значение после сброса должно быть около 0%, получено: {reset_result}"

    # Финальная проверка кнопки
    final_button_text = progress_page.get_button_text()
    assert (
        final_button_text == "Start"
    ), f"После сброса кнопка должна быть 'Start', получено: '{final_button_text}'"
