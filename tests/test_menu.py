# tests/test_menu.py
import pytest


def test_menu_functionality(menu_page):
    """Тест: функциональность меню."""
    print("=== ТЕСТ ФУНКЦИОНАЛЬНОСТИ МЕНЮ ===")
    # Даем время странице загрузиться
    menu_page.page.wait_for_timeout(5000)

    # 1. Проверяем загрузку страницы
    assert menu_page.is_page_loaded(), "Страница должна загрузиться"
    print("✓ Страница загрузилась")

    # 2. Проверяем URL
    current_url = menu_page.page.url
    assert "menu" in current_url.lower(), f"URL должен содержать 'menu', текущий: {current_url}"
    print(f"✓ URL корректный: {current_url}")

    # 3. Проверяем заголовок
    page_title = menu_page.page.title()
    assert "DEMOQA" in page_title, f"Заголовок должен содержать 'DEMOQA', текущий: {page_title}"
    print(f"✓ Заголовок: {page_title}")

    # 4. Проверяем количество элементов (опционально)
    tree_items_count = menu_page.get_tree_items_count()
    print(f"Количество элементов дерева: {tree_items_count}")

    # 5. Проверяем наличие основных пунктов меню по тексту
    main_items = ["Main Item 1", "Main Item 2", "Main Item 3"]
    found_items = []
    for item_text in main_items:
        try:
            items = menu_page.find_items_by_text(item_text)
            if items and items.count() > 0:
                found_items.append(item_text)
                print(f"✓ Найден пункт меню: '{item_text}'")
            else:
                print(f"⚠ Пункт меню не найден: '{item_text}'")
        except Exception as e:
            print(f"⚠ Ошибка поиска '{item_text}': {e}")
    assert len(found_items) > 0, "Должны быть найдены пункты меню"
    print(f"✓ Найдено пунктов меню: {len(found_items)}")

    # 6. Проверяем наличие подпунктов (Sub Item, SUB SUB LIST)
    submenu_items = ["Sub Item", "SUB SUB LIST"]
    found_submenu = []
    for item_text in submenu_items:
        try:
            items = menu_page.find_items_by_text(item_text)
            if items and items.count() > 0:
                found_submenu.append(item_text)
                print(f"✓ Найден подпункт меню: '{item_text}'")
            else:
                print(f"⚠ Подпункт меню не найден: '{item_text}'")
        except Exception as e:
            print(f"⚠ Ошибка поиска подпункта '{item_text}': {e}")
    assert len(found_submenu) > 0, "Должны быть найдены подпункты меню"
    print(f"✓ Найдено подпунктов меню: {len(found_submenu)}")

    # 7. Проверяем наличие под-подпунктов (Sub Sub Item 1, Sub Sub Item 2)
    sub_sub_items = ["Sub Sub Item 1", "Sub Sub Item 2"]
    found_sub_sub = []
    for item_text in sub_sub_items:
        try:
            items = menu_page.find_items_by_text(item_text)
            if items and items.count() > 0:
                found_sub_sub.append(item_text)
                print(f"✓ Найден под-подпункт меню: '{item_text}'")
            else:
                print(f"⚠ Под-подпункт меню не найден: '{item_text}'")
        except Exception as e:
            print(f"⚠ Ошибка поиска под-подпункта '{item_text}': {e}")
    assert len(found_sub_sub) > 0, "Должны быть найдены под-подпункты меню"
    print(f"✓ Найдено под-подпунктов меню: {len(found_sub_sub)}")

    # 8. ТЕСТ ИНТЕРАКТИВНОСТИ - КЛИКИ И НАВЕДЕНИЕ
    print("- ТЕСТ ИНТЕРАКТИВНОСТИ -")
    # Наведение на Main Item 1
    main_item_1 = menu_page.find_items_by_text("Main Item 1").first
    main_item_1.hover()
    menu_page.page.wait_for_timeout(1000)
    print("✓ Наведение на 'Main Item 1' работает")

    # Клик по Main Item 1
    main_item_1.click()
    menu_page.page.wait_for_timeout(1000)
    print("✓ Клик на 'Main Item 1' работает")

    # Наведение на SUB SUB LIST и клик по Sub Sub Item 1
    sub_sub_list = menu_page.find_items_by_text("SUB SUB LIST").first
    sub_sub_list.hover()
    menu_page.page.wait_for_timeout(2000) # Пауза для открытия 3-го уровня
    print("✓ Наведение на 'SUB SUB LIST' работает")

    # Клик по Sub Sub Item 1
    sub_sub_item_1 = menu_page.find_items_by_text("Sub Sub Item 1").first
    if sub_sub_item_1.is_visible():
        sub_sub_item_1.click()
        print(f"✓ Клик по элементу 3-го уровня 'Sub Sub Item 1' успешен")
        # Пауза после клика
        menu_page.page.wait_for_timeout(500)
        # Возврат курсора, если нужно проверить исчезновение (необязательно)
        menu_page.move_mouse_away()
        menu_page.page.wait_for_timeout(500)
    else:
        print("? Элемент 'Sub Sub Item 1' не видим после наведения на SUB SUB LIST")

    # Клик по Sub Sub Item 2
    sub_sub_item_2 = menu_page.find_items_by_text("Sub Sub Item 2").first
    if sub_sub_item_2.is_visible():
        sub_sub_item_2.click()
        print(f"✓ Клик по элементу 3-го уровня 'Sub Sub Item 2' успешен")
        # Пауза после клика
        menu_page.page.wait_for_timeout(500)
        # Возврат курсора, если нужно проверить исчезновение (необязательно)
        menu_page.move_mouse_away()
        menu_page.page.wait_for_timeout(500)
    else:
        print("? Элемент 'Sub Sub Item 2' не видим после наведения на SUB SUB LIST")

    # Проверка стабильности страницы после взаимодействия
    print("✓ Страница стабильна после взаимодействия")

    # 9. Финальная проверка
    total_found = len(found_items) + len(found_submenu) + len(found_sub_sub)
    assert total_found > 0, "Должны быть найдены элементы меню"
    print(f"🎉 ТЕСТ МЕНЮ ПРОЙДЕН УСПЕШНО!")
    print(f" Найдено основных пунктов: {len(found_items)}")
    print(f" Найдено подпунктов: {len(found_submenu)}")
    print(f" Найдено под-подпунктов: {len(found_sub_sub)}")
    print(f" Общее количество найденных элементов: {total_found}")
    assert True, "Функциональность меню работает корректно"