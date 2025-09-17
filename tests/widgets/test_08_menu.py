from playwright.sync_api import expect


def test_menu1_visible(menu_page):
    count = menu_page.menu1_count()
    assert count > 0, "Menu level 1 is empty"
    for i in range(count):
        visible = menu_page.is_menu1_visible(i)
        assert visible, f"Menu1 item {i} должен быть видим"
        menu_page.hover_menu1(i)

        # Проверяем, что подменю (если есть) появилось, считается активным
        # Пример: у пункта с подменю проверяем наличие дочернего ul.menu-list с видимостью
        submenu_locator = menu_page.page.locator(
            f"ul#nav > li:nth-child({i+1}) ul.menu-list"
        )
        if submenu_locator.count() > 0:
            assert (
                submenu_locator.first.is_visible()
            ), f"Submenu для Menu1 item {i} должен быть видим после hover"


def test_menu2_and_3_visible(menu_page):
    menu_page.hover_menu1(1)  # "Main Item 2"

    menu2_count = menu_page.menu2_items.count()
    assert menu2_count > 0, "Menu level 2 пусто"

    for i in range(menu2_count):
        locator = menu_page.menu2_items.nth(i)
        expect(locator).to_be_visible(timeout=10000)

        menu_page.hover_menu2(i)

        # Проверяем видимость подменю третьего уровня, если есть
        submenu3_locator = menu_page.page.locator(
            f"ul#nav > li:nth-child(2) ul > li:nth-child({i+1}) ul.menu-list"
        )
        if submenu3_locator.count() > 0:
            assert (
                submenu3_locator.first.is_visible()
            ), f"Submenu 3 для Menu2 item {i} должен быть видим после hover"

    menu_page.hover_sub_sub_list()

    menu3_count = menu_page.menu3_items.count()
    assert menu3_count > 0, "Menu level 3 пусто"

    for j in range(menu3_count):
        locator3 = menu_page.menu3_items.nth(j)
        expect(locator3).to_be_visible(timeout=5000)
