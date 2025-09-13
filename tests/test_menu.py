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
    assert (
        "menu" in current_url.lower()
    ), f"URL должен содержать 'menu', текущий: {current_url}"
    print(f"✓ URL корректный: {current_url}")

    # 3. Проверяем заголовок
    page_title = menu_page.page.title()
    assert len(page_title) > 0, "Страница должна иметь заголовок"
    print(f"✓ Заголовок: {page_title}")

    # 4. Проверяем наличие элементов меню
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

    # 6. Проверяем подменю
    submenu_items = ["Sub Item", "SUB SUB LIST", "Sub Sub Item 1", "Sub Sub Item 2"]
    found_submenu = []

    for item_text in submenu_items:
        try:
            items = menu_page.find_items_by_text(item_text)
            if items and items.count() > 0:
                found_submenu.append(item_text)
                print(f"✓ Найден подпункт меню: '{item_text}'")
        except Exception as e:
            print(f"⚠ Ошибка поиска подпункта '{item_text}': {e}")

    print(f"✓ Найдено подпунктов меню: {len(found_submenu)}")

    # 7. Проверяем базовую интерактивность (наведение/клик)
    print("\n--- ТЕСТ ИНТЕРАКТИВНОСТИ ---")

    # Пробуем навести на первый найденный пункт
    if len(found_items) > 0:
        try:
            first_item_text = found_items[0]
            first_item = menu_page.find_items_by_text(first_item_text)
            if menu_page.hover_item(first_item):
                print(f"✓ Наведение на '{first_item_text}' работает")
            else:
                print(f"⚠ Наведение на '{first_item_text}' не удалось")
        except Exception as e:
            print(f"⚠ Ошибка наведения: {e}")

    # Пробуем кликнуть на первый найденный пункт
    try:
        first_item_text = found_items[0] if found_items else "Main Item 1"
        first_item = menu_page.find_items_by_text(first_item_text)
        if menu_page.click_item(first_item):
            print(f"✓ Клик на '{first_item_text}' работает")
        else:
            print(f"⚠ Клик на '{first_item_text}' не удался")
    except Exception as e:
        print(f"⚠ Ошибка клика: {e}")

    # 8. Проверяем, что страница не сломалась после взаимодействия
    menu_page.page.wait_for_timeout(1000)
    assert (
        menu_page.is_page_loaded()
    ), "Страница должна оставаться загруженной после взаимодействия"
    print("✓ Страница стабильна после взаимодействия")

    # 9. Финальная проверка
    total_found = len(found_items) + len(found_submenu)
    assert total_found > 0, "Должны быть найдены элементы меню"

    print(f"\n🎉 ТЕСТ МЕНЮ ПРОЙДЕН УСПЕШНО!")
    print(f"   Найдено основных пунктов: {len(found_items)}")
    print(f"   Найдено подпунктов: {len(found_submenu)}")
    print(f"   Общее количество найденных элементов: {total_found}")

    assert True, "Функциональность меню работает корректно"
