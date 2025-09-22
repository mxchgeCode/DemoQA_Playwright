"""
Page Object для страницы Web Tables.
Содержит методы для работы с интерактивной таблицей: добавление, редактирование, удаление записей.
"""

from playwright.sync_api import Page
from locators.elements.web_tables_locators import WebTablesLocators
from pages.base_page import BasePage


class WebTablesPage(BasePage):
    """
    Страница тестирования интерактивных веб-таблиц.
    Поддерживает CRUD операции с записями таблицы и поиск по содержимому.
    """

    def __init__(self, page: Page):
        """
        Инициализация страницы Web Tables.

        Args:
            page: Экземпляр страницы Playwright
        """
        super().__init__(page)

    def click_add_button(self) -> None:
        """
        Кликает по кнопке Add для добавления новой записи.
        Postconditions: открывается модальное окно для ввода данных новой записи.
        """
        self.log_step("Кликаем по кнопке Add")
        self.safe_click(WebTablesLocators.ADD_BUTTON)

    def fill_registration_form(
        self,
        first_name: str,
        last_name: str,
        email: str,
        age: str,
        salary: str,
        department: str,
    ) -> None:
        """
        Заполняет форму регистрации новой записи или редактирования существующей.

        Args:
            first_name: Имя
            last_name: Фамилия
            email: Email адрес
            age: Возраст
            salary: Зарплата
            department: Отдел

        Postconditions: все поля формы заполнены указанными значениями
        """
        self.log_step(f"Заполняем форму регистрации: {first_name} {last_name}")
        self.safe_fill(WebTablesLocators.FIRST_NAME_INPUT, first_name)
        self.safe_fill(WebTablesLocators.LAST_NAME_INPUT, last_name)
        self.safe_fill(WebTablesLocators.EMAIL_INPUT, email)
        self.safe_fill(WebTablesLocators.AGE_INPUT, age)
        self.safe_fill(WebTablesLocators.SALARY_INPUT, salary)
        self.safe_fill(WebTablesLocators.DEPARTMENT_INPUT, department)

    def submit_form(self) -> None:
        """
        Отправляет форму регистрации/редактирования.
        Postconditions: форма отправлена, модальное окно закрыто, запись добавлена/обновлена в таблице.
        """
        self.log_step("Отправляем форму регистрации")
        self.safe_click(WebTablesLocators.SUBMIT_BUTTON)
    
    def search_table(self, search_term: str) -> None:
        """
        Выполняет поиск в таблице по указанному термину.
    
        Args:
            search_term: Термин для поиска в таблице
    
        Postconditions: таблица отфильтрована по поисковому запросу
        """
        self.log_step(f"Выполняем поиск в таблице: {search_term}")
        # Исправлено соответствие локаторам: используем SEARCH_INPUT
        self.safe_fill(WebTablesLocators.SEARCH_INPUT, search_term)

    def clear_search(self) -> None:
        """
        Очищает поисковое поле.
        Postconditions: поиск очищен, отображаются все записи таблицы.
        """
        self.log_step("Очищаем поиск")
        self.safe_fill(WebTablesLocators.SEARCH_BOX, "")

    def get_table_data(self) -> list[dict]:
        """
        Получает все данные из таблицы в виде списка словарей.

        Returns:
            list: Список словарей с данными строк таблицы

        Example:
            [
                {'first_name': 'John', 'last_name': 'Doe', 'email': 'john@example.com', ...},
                {'first_name': 'Jane', 'last_name': 'Smith', 'email': 'jane@example.com', ...}
            ]
        """
        self.log_step("Получаем данные из таблицы")
        rows = []
        table_rows = self.page.locator(WebTablesLocators.TABLE_ROWS)

        for i in range(table_rows.count()):
            row = table_rows.nth(i)
            cells = row.locator("td")

            if cells.count() >= 6:  # Проверяем что строка не пустая
                row_data = {
                    "first_name": cells.nth(0).inner_text().strip(),
                    "last_name": cells.nth(1).inner_text().strip(),
                    "age": cells.nth(2).inner_text().strip(),
                    "email": cells.nth(3).inner_text().strip(),
                    "salary": cells.nth(4).inner_text().strip(),
                    "department": cells.nth(5).inner_text().strip(),
                }
                rows.append(row_data)

        return rows

    def get_row_count(self) -> int:
        """
        Получает количество строк в таблице (исключая заголовок).

        Returns:
            int: Количество строк данных в таблице
        """
        table_rows = self.page.locator(WebTablesLocators.TABLE_ROWS)
        # Исключаем пустые строки
        count = 0
        for i in range(table_rows.count()):
            row = table_rows.nth(i)
            cells = row.locator("td")
            if cells.count() >= 6 and cells.nth(0).inner_text().strip():
                count += 1
        return count

    def delete_row(self, row_index: int) -> None:
        """
        Удаляет строку таблицы по индексу.

        Args:
            row_index: Индекс строки для удаления (начиная с 0)

        Postconditions: указанная строка удалена из таблицы
        """
        self.log_step(f"Удаляем строку с индексом {row_index}")
        delete_buttons = self.page.locator(WebTablesLocators.DELETE_BUTTON)
        if delete_buttons.count() > row_index:
            delete_buttons.nth(row_index).click()

    def edit_row(self, row_index: int) -> None:
        """
        Открывает форму редактирования для строки таблицы по индексу.

        Args:
            row_index: Индекс строки для редактирования (начиная с 0)

        Postconditions: открывается модальное окно с данными для редактирования
        """
        self.log_step(f"Редактируем строку с индексом {row_index}")
        edit_buttons = self.page.locator(WebTablesLocators.EDIT_BUTTON)
        if edit_buttons.count() > row_index:
            edit_buttons.nth(row_index).click()

    def is_modal_visible(self) -> bool:
        """
        Проверяет видимость модального окна формы.

        Returns:
            bool: True если модальное окно видимо
        """
        return self.page.locator(WebTablesLocators.REGISTRATION_FORM).is_visible()

    def close_modal(self) -> None:
        """
        Закрывает модальное окно без сохранения изменений.
        Postconditions: модальное окно закрыто.
        """
        self.log_step("Закрываем модальное окно")
        close_button = self.page.locator(".close, .btn-secondary")
        if close_button.is_visible():
            close_button.click()
    
    def find_row_by_email(self, email: str) -> int:
        """
        Находит индекс строки по email адресу.
    
        Args:
            email: Email для поиска
    
        Returns:
            int: Индекс найденной строки или -1 если не найдена
        """
        table_data = self.get_table_data()
        for i, row in enumerate(table_data):
            if row["email"] == email:
                return i
        return -1
    
    def verify_row_data(self, expected_data: dict) -> bool:
        """
        Проверяет наличие строки с указанными данными в таблице.
    
        Args:
            expected_data: Словарь с ожидаемыми данными строки
    
        Returns:
            bool: True если строка с такими данными найдена
        """
        table_data = self.get_table_data()
        for row in table_data:
            if all(row.get(key) == value for key, value in expected_data.items()):
                return True
        return False
    
    def add_new_person(self, person_data: dict) -> None:
        """
        Добавляет новую запись в таблицу одним методом.
    
        Args:
            person_data: Словарь с данными человека
    
        Example:
            person_data = {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'age': '30',
                'salary': '50000',
                'department': 'IT'
            }
    
        Postconditions: новая запись добавлена в таблицу
        """
        self.log_step(
            f"Добавляем новую запись: {person_data.get('first_name')} {person_data.get('last_name')}"
        )
        self.click_add_button()
        self.wait_for_visible(WebTablesLocators.REGISTRATION_FORM, timeout=5000)
    
        self.fill_registration_form(
            person_data.get("first_name", ""),
            person_data.get("last_name", ""),
            person_data.get("email", ""),
            person_data.get("age", ""),
            person_data.get("salary", ""),
            person_data.get("department", ""),
        )
        self.submit_form()
    
    # ======== Совместимость с ожидаемым API тестов ========
    # Имена методов-алиасов, возвращающие/делающие то же самое
    
    # counts
    def get_records_count(self) -> int:
        return self.get_row_count()
    
    # add button
    def click_add(self) -> None:
        self.click_add_button()
    
    # registration form visibility
    def is_registration_form_visible(self) -> bool:
        return self.is_modal_visible()
    
    # fill form (alias)
    def fill_form(
        self,
        first_name: str,
        last_name: str,
        email: str,
        age,
        salary,
        department: str,
    ) -> None:
        self.fill_registration_form(
            str(first_name),
            str(last_name),
            str(email),
            str(age),
            str(salary),
            str(department),
        )
    
    # read current form data
    def get_form_data(self) -> dict:
        def _val(sel: str) -> str:
            try:
                return self.page.locator(sel).input_value()
            except Exception:
                return ""
    
        return {
            "first_name": _val(WebTablesLocators.FIRST_NAME_INPUT),
            "last_name": _val(WebTablesLocators.LAST_NAME_INPUT),
            "email": _val(WebTablesLocators.EMAIL_INPUT),
            "age": _val(WebTablesLocators.AGE_INPUT),
            "salary": _val(WebTablesLocators.SALARY_INPUT),
            "department": _val(WebTablesLocators.DEPARTMENT_INPUT),
        }
    
    # search (alias)
    def search(self, term: str) -> None:
        self.search_table(term)
    
    def clear(self) -> None:
        self.clear_search()
    
    # results after current filter
    def get_search_results(self) -> list[dict]:
        return self.get_table_data()
    
    # click delete/edit button for a record containing term
    def click_delete_button_for_record(self, term: str) -> bool:
        rows = self.page
        locator = rows.locator(WebTablesLocators.TABLE_ROWS).filter(has_text=term)
        if locator.count() == 0:
            return False
        try:
            row = locator.first
            # кнопка удаления внутри строки
            btn = row.locator(WebTablesLocators.DELETE_BUTTON)
            if btn.count() == 0:
                btn = row.locator(WebTablesLocators.DELETE_BUTTONS)
            if btn.count() > 0:
                btn.first.click()
                return True
            return False
        except Exception:
            return False
    
    def click_edit_button_for_record(self, term: str) -> bool:
        rows = self.page
        locator = rows.locator(WebTablesLocators.TABLE_ROWS).filter(has_text=term)
        if locator.count() == 0:
            return False
        try:
            row = locator.first
            btn = row.locator(WebTablesLocators.EDIT_BUTTON)
            if btn.count() == 0:
                btn = row.locator(WebTablesLocators.EDIT_BUTTONS)
            if btn.count() > 0:
                btn.first.click()
                return True
            return False
        except Exception:
            return False
    
    # pagination helpers (best-effort; demoqa webtables обычно без пагинации)
    def get_pagination_info(self) -> dict:
        info = {
            "has_pagination": False,
            "available_pages": [],
        }
        try:
            container = self.page.locator(WebTablesLocators.PAGINATION_CONTAINER)
            if container.count() > 0 and container.is_visible():
                buttons = self.page.locator(WebTablesLocators.PAGE_BUTTONS)
                pages = []
                for i in range(buttons.count()):
                    txt = (buttons.nth(i).inner_text() or "").strip()
                    if txt.isdigit():
                        pages.append(int(txt))
                info["has_pagination"] = len(pages) > 1
                info["available_pages"] = pages
        except Exception:
            pass
        return info
    
    def go_to_page(self, page_num: int) -> bool:
        try:
            buttons = self.page.locator(WebTablesLocators.PAGE_BUTTONS)
            for i in range(buttons.count()):
                if (buttons.nth(i).inner_text() or "").strip() == str(page_num):
                    buttons.nth(i).click()
                    return True
        except Exception:
            return False
        return False
    
    def get_current_page_records(self) -> list[dict]:
        return self.get_table_data()
    
    def get_active_page_number(self) -> int:
        try:
            active = self.page.locator(WebTablesLocators.ACTIVE_PAGE)
            txt = (active.inner_text() or "").strip()
            return int(txt) if txt.isdigit() else 1
        except Exception:
            return 1
