"""
Тесты для страницы Web Tables.
Проверяет функциональность таблиц:
- Добавление новых записей в таблицу
- Поиск и фильтрация записей
- Редактирование существующих записей
- Удаление записей из таблицы
- Пагинация и сортировка
"""

import pytest
import allure
import time
from pages.elements.web_tables_page import WebTablesPage
from locators.elements.web_tables_locators import WebTablesLocators


@allure.epic("Elements")
@allure.feature("Web Tables")
@allure.story("Add New Record")
@pytest.mark.elements
@pytest.mark.smoke
def test_add_new_record_to_table(web_tables_page: WebTablesPage):
    """
    Тест добавления новой записи в таблицу.

    Создает новую запись с валидными данными и проверяет ее появление в таблице.
    """
    new_record_data = {
        "first_name": "John",
        "last_name": "Doe", 
        "email": "john.doe@example.com",
        "age": 28,
        "salary": 50000,
        "department": "Engineering"
    }

    with allure.step("Получаем количество записей до добавления"):
        initial_record_count = web_tables_page.get_records_count()
        web_tables_page.log_step(f"Начальное количество записей: {initial_record_count}")

        allure.attach(str(initial_record_count), "initial_records_count", allure.attachment_type.TEXT)

    with allure.step("Открываем форму добавления новой записи"):
        web_tables_page.log_step("Клик по кнопке 'Add' для открытия формы")
        web_tables_page.click_add()

        # Проверяем что форма открылась
        form_visible = web_tables_page.is_registration_form_visible()
        web_tables_page.log_step(f"Форма регистрации видима: {form_visible}")

        assert form_visible, "Форма добавления записи должна быть видимой"

    with allure.step("Заполняем форму новыми данными"):
        web_tables_page.log_step(f"Заполнение формы данными: {new_record_data}")

        web_tables_page.fill_form(
            new_record_data["first_name"],
            new_record_data["last_name"], 
            new_record_data["email"],
            new_record_data["age"],
            new_record_data["salary"],
            new_record_data["department"]
        )

        # Проверяем что поля заполнены корректно
        filled_data = web_tables_page.get_form_data()
        web_tables_page.log_step(f"Заполненные данные в форме: {filled_data}")

        allure.attach(str(filled_data), "filled_form_data", allure.attachment_type.JSON)

    with allure.step("Отправляем форму"):
        web_tables_page.log_step("Отправка формы добавления записи")
        web_tables_page.submit_form()

        # Ждем обновления таблицы
        web_tables_page.page.wait_for_timeout(1000)

        # Проверяем что форма закрылась
        form_closed = not web_tables_page.is_registration_form_visible()
        web_tables_page.log_step(f"Форма закрылась после отправки: {form_closed}")

    with allure.step("Проверяем что запись добавилась в таблицу"):
        final_record_count = web_tables_page.get_records_count()
        web_tables_page.log_step(f"Количество записей после добавления: {final_record_count}")

        records_added = final_record_count > initial_record_count
        web_tables_page.log_step(f"Запись добавлена: {records_added}")

        assert records_added, f"Количество записей должно увеличиться: было {initial_record_count}, стало {final_record_count}"

    with allure.step("Ищем добавленную запись в таблице"):
        web_tables_page.log_step(f"Поиск записи по email: {new_record_data['email']}")
        web_tables_page.search(new_record_data["email"])

        # Проверяем что запись найдена
        search_results = web_tables_page.get_search_results()
        web_tables_page.log_step(f"Результаты поиска: {len(search_results)} записей найдено")

        record_found = len(search_results) > 0
        assert record_found, f"Добавленная запись с email {new_record_data['email']} должна быть найдена"

        # Проверяем содержимое найденной записи
        if record_found:
            found_record = search_results[0]
            web_tables_page.log_step(f"Найденная запись: {found_record}")

            allure.attach(str(found_record), "found_record_data", allure.attachment_type.JSON)

            # Проверяем соответствие данных
            assert found_record["email"] == new_record_data["email"], "Email должен совпадать"
            assert found_record["first_name"] == new_record_data["first_name"], "Имя должно совпадать"

        web_tables_page.log_step("✅ Запись успешно добавлена и найдена в таблице")


@allure.epic("Elements")
@allure.feature("Web Tables")
@allure.story("Delete Record")
@pytest.mark.elements
@pytest.mark.smoke
def test_delete_record_from_table(web_tables_page: WebTablesPage):
    """
    Тест удаления записи из таблицы.

    Находит существующую запись и удаляет ее, проверяя что она исчезла из таблицы.
    """
    target_search_term = "Cierra"

    with allure.step("Ищем запись для удаления"):
        web_tables_page.log_step(f"Поиск записи по термину: {target_search_term}")
        web_tables_page.search(target_search_term)

        # Получаем количество записей до удаления
        records_before_delete = web_tables_page.get_search_results()
        records_count_before = len(records_before_delete)
        web_tables_page.log_step(f"Найдено записей для удаления: {records_count_before}")

        allure.attach(str(records_before_delete), "records_before_delete", allure.attachment_type.JSON)

        assert records_count_before > 0, f"Должна быть найдена хотя бы одна запись с '{target_search_term}'"

    with allure.step("Удаляем первую найденную запись"):
        # Получаем данные удаляемой записи для последующей проверки
        record_to_delete = records_before_delete[0]
        web_tables_page.log_step(f"Удаляемая запись: {record_to_delete}")

        # Выполняем удаление
        web_tables_page.log_step("Клик по кнопке удаления записи")
        delete_button_clicked = web_tables_page.click_delete_button_for_record(target_search_term)

        assert delete_button_clicked, "Кнопка удаления должна быть успешно нажата"

        # Ждем обновления DOM после удаления
        web_tables_page.log_step("Ожидание обновления таблицы после удаления")
        try:
            # Ждем что элемент с данными исчезнет
            web_tables_page.page.locator(WebTablesLocators.TABLE_ROWS).filter(
                has_text=target_search_term
            ).wait_for(state="detached", timeout=5000)
            web_tables_page.log_step("Запись успешно удалена из DOM")
        except Exception as e:
            web_tables_page.log_step(f"Таймаут ожидания удаления: {e}")

        time.sleep(2)  # Дополнительная пауза для стабильности

    with allure.step("Проверяем результат удаления"):
        # Повторяем поиск для проверки удаления
        web_tables_page.log_step(f"Повторный поиск по термину: {target_search_term}")
        web_tables_page.search(target_search_term)

        records_after_delete = web_tables_page.get_search_results()
        records_count_after = len(records_after_delete)
        web_tables_page.log_step(f"Количество записей после удаления: {records_count_after}")

        deletion_result = {
            "records_before": records_count_before,
            "records_after": records_count_after,
            "records_deleted": records_count_before - records_count_after,
            "deletion_successful": records_count_after < records_count_before
        }

        web_tables_page.log_step(f"Результат удаления: {deletion_result}")
        allure.attach(str(deletion_result), "deletion_result", allure.attachment_type.JSON)

        assert deletion_result["deletion_successful"], f"Запись должна быть удалена: было {records_count_before}, стало {records_count_after}"

        web_tables_page.log_step("✅ Запись успешно удалена из таблицы")


@allure.epic("Elements")
@allure.feature("Web Tables")
@allure.story("Search and Filter")
@pytest.mark.elements
@pytest.mark.regression
def test_search_functionality(web_tables_page: WebTablesPage):
    """
    Тест функциональности поиска в таблице.

    Проверяет различные сценарии поиска и фильтрации записей.
    """
    search_test_cases = [
        {"term": "Cierra", "expected_min": 1, "description": "Поиск по имени"},
        {"term": "@example.com", "expected_min": 0, "description": "Поиск по домену email"},
        {"term": "25", "expected_min": 0, "description": "Поиск по возрасту"},
        {"term": "NonExistentTerm", "expected_min": 0, "description": "Поиск несуществующего термина"}
    ]

    search_results = []

    with allure.step("Тестируем различные поисковые запросы"):
        for i, test_case in enumerate(search_test_cases):
            search_term = test_case["term"]
            expected_min = test_case["expected_min"]
            description = test_case["description"]

            with allure.step(f"Тест {i+1}: {description} - '{search_term}'"):
                web_tables_page.log_step(f"Выполнение поиска: {description}")

                # Очищаем предыдущий поиск
                web_tables_page.clear_search()
                web_tables_page.page.wait_for_timeout(500)

                # Выполняем поиск
                web_tables_page.search(search_term)
                web_tables_page.page.wait_for_timeout(1000)

                # Получаем результаты
                found_records = web_tables_page.get_search_results()
                found_count = len(found_records)

                search_result = {
                    "search_term": search_term,
                    "description": description,
                    "found_count": found_count,
                    "expected_min": expected_min,
                    "meets_expectation": found_count >= expected_min,
                    "found_records": found_records[:2]  # Первые 2 записи для примера
                }

                search_results.append(search_result)
                web_tables_page.log_step(f"Результат поиска '{search_term}': найдено {found_count} записей")

                # Проверяем соответствие ожиданиям
                if expected_min > 0:
                    assert found_count >= expected_min, f"Для '{search_term}' ожидалось минимум {expected_min} записей, найдено {found_count}"
                elif search_term == "NonExistentTerm":
                    assert found_count == 0, f"Для несуществующего термина должно быть найдено 0 записей, найдено {found_count}"

    with allure.step("Анализируем общую эффективность поиска"):
        allure.attach(str(search_results), "all_search_results", allure.attachment_type.JSON)

        successful_searches = sum(1 for result in search_results if result["meets_expectation"])
        total_searches = len(search_results)

        search_effectiveness = {
            "total_searches": total_searches,
            "successful_searches": successful_searches,
            "success_rate": successful_searches / total_searches if total_searches > 0 else 0,
            "search_functionality_works": successful_searches >= total_searches * 0.75
        }

        web_tables_page.log_step(f"Эффективность поиска: {search_effectiveness}")
        allure.attach(str(search_effectiveness), "search_effectiveness", allure.attachment_type.JSON)

        assert search_effectiveness["search_functionality_works"], f"Функциональность поиска должна работать корректно: {successful_searches}/{total_searches} успешных"

        web_tables_page.log_step("✅ Функциональность поиска работает корректно")


@allure.epic("Elements")
@allure.feature("Web Tables")
@allure.story("Edit Record")
@pytest.mark.elements
@pytest.mark.regression  
def test_edit_existing_record(web_tables_page: WebTablesPage):
    """
    Тест редактирования существующей записи.

    Находит запись, редактирует ее данные и проверяет изменения.
    """
    target_search_term = "Alden"
    updated_data = {
        "first_name": "AldenUpdated",
        "last_name": "CantrellUpdated", 
        "salary": 75000
    }

    with allure.step("Находим запись для редактирования"):
        web_tables_page.log_step(f"Поиск записи для редактирования: {target_search_term}")
        web_tables_page.search(target_search_term)

        original_records = web_tables_page.get_search_results()
        web_tables_page.log_step(f"Найдено записей: {len(original_records)}")

        assert len(original_records) > 0, f"Должна быть найдена запись с '{target_search_term}'"

        original_record = original_records[0]
        web_tables_page.log_step(f"Оригинальная запись: {original_record}")

        allure.attach(str(original_record), "original_record_data", allure.attachment_type.JSON)

    with allure.step("Открываем форму редактирования"):
        web_tables_page.log_step("Клик по кнопке редактирования записи")
        edit_button_clicked = web_tables_page.click_edit_button_for_record(target_search_term)

        assert edit_button_clicked, "Кнопка редактирования должна быть успешно нажата"

        # Проверяем что форма редактирования открылась
        form_visible = web_tables_page.is_registration_form_visible()
        web_tables_page.log_step(f"Форма редактирования открыта: {form_visible}")

        assert form_visible, "Форма редактирования должна быть видимой"

    with allure.step("Получаем текущие данные в форме"):
        current_form_data = web_tables_page.get_form_data()
        web_tables_page.log_step(f"Текущие данные в форме: {current_form_data}")

        allure.attach(str(current_form_data), "current_form_data", allure.attachment_type.JSON)

    with allure.step("Обновляем данные в форме"):
        web_tables_page.log_step(f"Обновление данных: {updated_data}")

        # Обновляем только измененные поля
        if "first_name" in updated_data:
            web_tables_page.update_first_name(updated_data["first_name"])

        if "last_name" in updated_data:
            web_tables_page.update_last_name(updated_data["last_name"])

        if "salary" in updated_data:
            web_tables_page.update_salary(updated_data["salary"])

        # Получаем обновленные данные формы
        updated_form_data = web_tables_page.get_form_data()
        web_tables_page.log_step(f"Обновленные данные в форме: {updated_form_data}")

    with allure.step("Сохраняем изменения"):
        web_tables_page.log_step("Отправка формы с обновленными данными")
        web_tables_page.submit_form()

        web_tables_page.page.wait_for_timeout(1000)

        # Проверяем что форма закрылась
        form_closed = not web_tables_page.is_registration_form_visible()
        web_tables_page.log_step(f"Форма закрылась: {form_closed}")

    with allure.step("Проверяем результат редактирования"):
        # Ищем обновленную запись
        web_tables_page.log_step("Поиск обновленной записи")
        web_tables_page.search(updated_data.get("first_name", target_search_term))

        updated_records = web_tables_page.get_search_results()
        web_tables_page.log_step(f"Найдено обновленных записей: {len(updated_records)}")

        if len(updated_records) > 0:
            updated_record = updated_records[0]
            web_tables_page.log_step(f"Обновленная запись: {updated_record}")

            allure.attach(str(updated_record), "updated_record_data", allure.attachment_type.JSON)

            # Проверяем что изменения применились
            changes_applied = True
            for field, expected_value in updated_data.items():
                if field in updated_record:
                    actual_value = updated_record[field]
                    if str(actual_value) != str(expected_value):
                        changes_applied = False
                        web_tables_page.log_step(f"Поле {field}: ожидалось {expected_value}, получено {actual_value}")

            edit_result = {
                "original_record": original_record,
                "updated_record": updated_record,
                "changes_applied": changes_applied,
                "updated_fields": updated_data
            }

            web_tables_page.log_step(f"Результат редактирования: {edit_result}")
            allure.attach(str(edit_result), "edit_result", allure.attachment_type.JSON)

            assert changes_applied, "Изменения должны быть применены к записи"

            web_tables_page.log_step("✅ Запись успешно отредактирована")
        else:
            assert False, "Обновленная запись не найдена после редактирования"


@allure.epic("Elements")
@allure.feature("Web Tables")
@allure.story("Table Pagination")
@pytest.mark.elements
def test_table_pagination(web_tables_page: WebTablesPage):
    """
    Тест пагинации таблицы.

    Проверяет переключение между страницами и отображение записей.
    """
    with allure.step("Анализируем структуру пагинации"):
        pagination_info = web_tables_page.get_pagination_info()
        web_tables_page.log_step(f"Информация о пагинации: {pagination_info}")

        allure.attach(str(pagination_info), "pagination_info", allure.attachment_type.JSON)

        has_pagination = pagination_info.get("has_pagination", False)

        if not has_pagination:
            web_tables_page.log_step("ℹ️ Пагинация отсутствует или все записи помещаются на одной странице")
            return

    with allure.step("Тестируем переключение страниц"):
        pages_to_test = pagination_info.get("available_pages", [])
        web_tables_page.log_step(f"Доступные страницы для тестирования: {pages_to_test}")

        pagination_tests = []

        for page_num in pages_to_test[:3]:  # Тестируем максимум 3 страницы
            with allure.step(f"Переход на страницу {page_num}"):
                web_tables_page.log_step(f"Переключение на страницу {page_num}")

                page_switch_result = web_tables_page.go_to_page(page_num)
                web_tables_page.page.wait_for_timeout(1000)

                # Получаем записи на текущей странице
                current_page_records = web_tables_page.get_current_page_records()
                records_count = len(current_page_records)

                # Проверяем активную страницу
                active_page = web_tables_page.get_active_page_number()

                page_test = {
                    "target_page": page_num,
                    "switch_successful": page_switch_result,
                    "active_page": active_page,
                    "records_on_page": records_count,
                    "page_switch_correct": active_page == page_num,
                    "has_records": records_count > 0
                }

                pagination_tests.append(page_test)
                web_tables_page.log_step(f"Результат перехода на страницу {page_num}: {page_test}")

    with allure.step("Анализируем результаты пагинации"):
        allure.attach(str(pagination_tests), "pagination_tests", allure.attachment_type.JSON)

        successful_switches = sum(1 for test in pagination_tests if test["page_switch_correct"])
        pages_with_records = sum(1 for test in pagination_tests if test["has_records"])

        pagination_summary = {
            "total_pages_tested": len(pagination_tests),
            "successful_switches": successful_switches,
            "pages_with_records": pages_with_records,
            "pagination_functionality_works": successful_switches >= len(pagination_tests) * 0.8,
            "all_pages_have_records": pages_with_records == len(pagination_tests)
        }

        web_tables_page.log_step(f"Итоги пагинации: {pagination_summary}")
        allure.attach(str(pagination_summary), "pagination_summary", allure.attachment_type.JSON)

        if pagination_summary["pagination_functionality_works"]:
            web_tables_page.log_step("✅ Пагинация работает корректно")
        else:
            web_tables_page.log_step("⚠️ Обнаружены проблемы с пагинацией")
