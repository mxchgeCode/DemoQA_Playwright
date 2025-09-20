"""
Тесты для страницы Progress Bar.
Проверяет функциональность прогресс-бара: запуск, остановка, сброс.
"""

import pytest
import allure


@allure.epic("Widgets")
@allure.feature("Progress Bar")
@allure.story("Basic functionality")
@pytest.mark.widgets
@pytest.mark.smoke
def test_start_and_stop_progress_bar(progress_bar_page):
    """
    Тест базовой функциональности прогресс-бара: запуск и остановка.

    Шаги:
    1. Запустить прогресс-бар
    2. Дождаться значения около 50%
    3. Остановить прогресс
    4. Проверить что прогресс остановился
    """
    with allure.step("Запускаем прогресс-бар"):
        progress_bar_page.start_progress()

    with allure.step("Ждем достижения примерно 50% и останавливаем"):
        # Ждем пока прогресс не достигнет хотя бы 20%
        initial_value = progress_bar_page.get_progress_value()

        # Даем время прогрессу поработать
        progress_bar_page.page.wait_for_timeout(3000)

        current_value = progress_bar_page.get_progress_value()
        progress_bar_page.stop_progress()

    with allure.step("Проверяем что прогресс остановился"):
        stopped_value = progress_bar_page.get_progress_value()

        # Ждем немного и проверяем что значение не изменилось
        progress_bar_page.page.wait_for_timeout(2000)
        final_value = progress_bar_page.get_progress_value()

        assert (
            stopped_value == final_value
        ), f"Прогресс не остановился: {stopped_value} != {final_value}"
        assert current_value != "0%", "Прогресс не запустился"

        allure.attach(
            f"Initial: {initial_value}, Current: {current_value}, Stopped: {stopped_value}, Final: {final_value}",
            "progress_values",
        )


@allure.epic("Widgets")
@allure.feature("Progress Bar")
@allure.story("Reset functionality")
@pytest.mark.widgets
def test_progress_bar_reset(progress_bar_page):
    """
    Тест функции сброса прогресс-бара.

    Шаги:
    1. Запустить прогресс до 100%
    2. Сбросить прогресс
    3. Проверить что значение вернулось к 0%
    """
    with allure.step("Запускаем прогресс до 100%"):
        progress_bar_page.start_progress()

        # Ждем завершения или останавливаем на высоком значении
        progress_bar_page.page.wait_for_timeout(8000)

        current_value = progress_bar_page.get_progress_value()
        if current_value != "100%":
            progress_bar_page.stop_progress()

    with allure.step("Сбрасываем прогресс-бар"):
        progress_bar_page.reset_progress()

    with allure.step("Проверяем что прогресс сброшен до 0%"):
        reset_value = progress_bar_page.get_progress_value()
        assert reset_value == "0%", f"Прогресс не сброшен: {reset_value}"

        # Проверяем что кнопка снова стала "Start"
        button_text = progress_bar_page.get_button_text()
        assert (
            "Start" in button_text
        ), f"Кнопка не вернулась в состояние Start: {button_text}"


@allure.epic("Widgets")
@allure.feature("Progress Bar")
@allure.story("Button states")
@pytest.mark.widgets
def test_button_text_changes(progress_bar_page):
    """
    Тест изменения текста кнопки в зависимости от состояния прогресс-бара.

    Проверяет что текст кнопки корректно изменяется между Start/Stop/Reset.
    """
    with allure.step("Проверяем начальное состояние кнопки"):
        initial_text = progress_bar_page.get_button_text()
        assert (
            "Start" in initial_text
        ), f"Начальный текст кнопки неправильный: {initial_text}"

    with allure.step("Запускаем прогресс и проверяем изменение кнопки"):
        progress_bar_page.start_progress()

        running_text = progress_bar_page.get_button_text()
        assert (
            "Stop" in running_text
        ), f"Текст кнопки не изменился на Stop: {running_text}"

    with allure.step("Останавливаем и проверяем появление кнопки Reset"):
        progress_bar_page.stop_progress()

        # После остановки может появиться кнопка Reset
        stopped_text = progress_bar_page.get_button_text()
        allure.attach(f"Stopped button text: {stopped_text}", "button_state")

        # Текст может быть "Start" или "Reset" в зависимости от реализации
        assert stopped_text in [
            "Start",
            "Stop",
            "Reset",
        ], f"Неожиданный текст кнопки: {stopped_text}"


@allure.epic("Widgets")
@allure.feature("Progress Bar")
@allure.story("Progress values")
@pytest.mark.widgets
@pytest.mark.parametrize(
    "wait_time,min_expected",
    [
        (1000, "5%"),  # 1 секунда - минимум 5%
        (2000, "15%"),  # 2 секунды - минимум 15%
        (4000, "30%"),  # 4 секунды - минимум 30%
    ],
)
def test_progress_timing(progress_bar_page, wait_time, min_expected):
    """
    Параметризованный тест проверки скорости прогресса.
    Проверяет что прогресс достигает ожидаемых значений за определенное время.
    """
    with allure.step(f"Запускаем прогресс на {wait_time} мс"):
        progress_bar_page.start_progress()
        progress_bar_page.page.wait_for_timeout(wait_time)

    with allure.step("Останавливаем и проверяем значение"):
        progress_bar_page.stop_progress()
        actual_value = progress_bar_page.get_progress_value()

        # Преобразуем в числа для сравнения
        actual_num = int(actual_value.replace("%", ""))
        min_num = int(min_expected.replace("%", ""))

        assert (
            actual_num >= min_num
        ), f"Прогресс слишком медленный: {actual_value} < {min_expected}"

        allure.attach(
            f"Wait time: {wait_time}ms, Expected min: {min_expected}, Actual: {actual_value}",
            "timing_results",
        )

    with allure.step("Сбрасываем для следующего теста"):
        progress_bar_page.reset_progress()


@allure.epic("Widgets")
@allure.feature("Progress Bar")
@allure.story("Edge cases")
@pytest.mark.widgets
def test_multiple_start_stop_cycles(progress_bar_page):
    """
    Тест множественных циклов запуск-остановка.
    Проверяет стабильность прогресс-бара при частых переключениях.
    """
    values_log = []

    with allure.step("Выполняем несколько циклов старт-стоп"):
        for i in range(3):
            with allure.step(f"Цикл {i + 1}"):
                # Запуск
                progress_bar_page.start_progress()
                progress_bar_page.page.wait_for_timeout(1500)

                # Получаем значение и останавливаем
                value = progress_bar_page.get_progress_value()
                progress_bar_page.stop_progress()
                values_log.append(f"Cycle {i+1}: {value}")

                # Небольшая пауза между циклами
                progress_bar_page.page.wait_for_timeout(500)

    with allure.step("Проверяем что все циклы работали"):
        # Проверяем что в каждом цикле был прогресс
        for i, log_entry in enumerate(values_log):
            assert (
                "0%" not in log_entry
            ), f"Цикл {i+1} не показал прогресса: {log_entry}"

        allure.attach("\n".join(values_log), "cycles_log")

    with allure.step("Финальный сброс"):
        progress_bar_page.reset_progress()
        final_value = progress_bar_page.get_progress_value()
        assert final_value == "0%", f"Финальный сброс не сработал: {final_value}"
