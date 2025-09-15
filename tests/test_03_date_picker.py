def test_date_picker_page_loads(datepicker_page):
    """Тест: страница Date Picker загружается корректно."""
    datepicker_page.page.wait_for_timeout(2000)

    current_url = datepicker_page.page.url
    assert "date-picker" in current_url, "URL должен содержать 'date-picker'"

    assert (
        datepicker_page.date_input.is_visible()
    ), "Поле выбора даты должно быть видимо"
    assert (
        datepicker_page.date_time_input.is_visible()
    ), "Поле выбора даты и времени должно быть видимо"


def test_date_picker_initial_state(datepicker_page):
    """Тест: начальное состояние элементов Date Picker."""
    date_value = datepicker_page.get_selected_date()
    assert len(date_value) > 0, "Значение даты не должно быть пустым"

    datetime_value = datepicker_page.get_selected_date_time()
    assert len(datetime_value) > 0, "Значение даты/времени не должно быть пустым"


def test_date_picker_opens(datepicker_page):
    """Тест: календарь открывается при клике на поле даты."""
    datepicker_page.click_date_input()
    datepicker_page.page.wait_for_timeout(2000)

    assert (
        datepicker_page.is_calendar_visible()
    ), "Календарь должен появиться после клика"
    assert (
        datepicker_page.calendar_month_select.is_visible()
    ), "Dropdown месяца должен быть видим"
    assert (
        datepicker_page.calendar_year_select.is_visible()
    ), "Dropdown года должен быть видим"


def test_date_time_picker_opens(datepicker_page):
    """Тест: календарь и время открываются при клике на поле даты/времени."""
    datepicker_page.click_date_time_input()
    datepicker_page.page.wait_for_timeout(2000)

    assert datepicker_page.is_calendar_visible(), "Календарь должен появиться"
    assert (
        datepicker_page.time_picker_list.is_visible()
    ), "Список времени должен быть видим"


def test_date_picker_calendar_elements(datepicker_page):
    """Тест: проверка элементов календаря."""
    datepicker_page.click_date_input()
    datepicker_page.page.wait_for_timeout(2000)

    datepicker_page.wait_for_calendar()

    days_count = datepicker_page.get_available_dates_count()
    assert days_count > 0, "В календаре должны быть дни"

    assert (
        datepicker_page.calendar_next_month_button.is_visible()
    ), "Кнопка следующего месяца должна быть видима"
    assert (
        datepicker_page.calendar_prev_month_button.is_visible()
    ), "Кнопка предыдущего месяца должна быть видима"


def test_date_picker_select_today(datepicker_page):
    """Тест: выбор сегодняшней даты."""
    datepicker_page.click_date_input()
    datepicker_page.wait_for_calendar()

    datepicker_page.select_today()
    datepicker_page.page.wait_for_timeout(2000)

    new_date_value = datepicker_page.get_selected_date()
    assert len(new_date_value) > 0, "Дата должна быть установлена после выбора"


def test_date_picker_input_fields_functionality(datepicker_page):
    """Тест: функциональность полей ввода."""
    date_value_before = datepicker_page.get_selected_date()

    # Выбрать 1-е число месяца (скорее всего отличается от сегодняшней даты)
    datepicker_page.click_date_input()
    datepicker_page.wait_for_calendar()
    datepicker_page.select_date_by_day(1)
    datepicker_page.wait_for_calendar_hidden()

    date_value_after = datepicker_page.get_selected_date()
    datetime_value_after = datepicker_page.get_selected_date_time()

    assert (
        date_value_after != date_value_before
    ), "Дата должна измениться после выбора другой даты"
    assert len(datetime_value_after) > 0, "Дата/время должны быть заданы"


def test_date_picker_select_specific_day(datepicker_page):
    """Тест: выбор конкретного дня."""
    datepicker_page.click_date_input()
    datepicker_page.wait_for_calendar()

    datepicker_page.select_date_by_day(15)
    datepicker_page.wait_for_calendar_hidden()

    selected_date = datepicker_page.get_selected_date()
    assert len(selected_date) > 0, "Дата должна быть выбрана"


def test_date_picker_navigation(datepicker_page):
    """Тест: навигация между месяцами."""
    datepicker_page.click_date_input()
    datepicker_page.wait_for_calendar()

    initial_month = datepicker_page.get_calendar_month()

    datepicker_page.navigate_to_next_month()
    next_month = datepicker_page.get_calendar_month()
    assert next_month != initial_month, "Месяц должен измениться после перехода вперёд"

    datepicker_page.navigate_to_prev_month()
    prev_month = datepicker_page.get_calendar_month()
    assert (
        prev_month == initial_month
    ), "Месяц должен вернуться к исходному после перехода назад"


def test_date_picker_month_year_selection(datepicker_page):
    """Тест: выбор месяца и года."""
    datepicker_page.click_date_input()
    datepicker_page.wait_for_calendar()

    assert (
        datepicker_page.calendar_month_select.is_visible()
    ), "Dropdown месяца должен быть доступен"
    assert (
        datepicker_page.calendar_year_select.is_visible()
    ), "Dropdown года должен быть доступен"

    month = datepicker_page.get_calendar_month()
    year = datepicker_page.get_calendar_year()

    assert len(month) > 0, "Месяц должен быть определен"
    assert len(year) > 0, "Год должен быть определен"
