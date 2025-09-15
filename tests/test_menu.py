from pages.menu_page import MenuPage
from playwright.sync_api import expect


# @pytest.fixture(scope="module")
def menu_page(page):
    menu = MenuPage(page)
    menu.goto()
    return menu


def test_menu1_visible(menu_page):
    count = menu_page.menu1_count()
    assert count > 0, "Menu level 1 is empty"
    for i in range(count):
        print(i)
        assert menu_page.is_menu1_visible(i), f"Menu1 item {i} is not visible"


def test_hover_all_menu(menu_page):
    count = menu_page.menu1_count()

    for i in range(count):
        menu_page.hover_menu1(i)


def test_menu2_and_3_visible(menu_page):
    menu_page.hover_menu1(1)  # "Main Item 2"

    menu2_count = menu_page.menu2_items.count()
    assert menu2_count > 0, "Menu level 2 is empty"

    for i in range(menu2_count):
        locator = menu_page.menu2_items.nth(i)
        expect(locator).to_be_visible(timeout=2000)
        menu_page.hover_menu2(i)

    # Наводим на пункт с подменю третьего уровня
    menu_page.hover_sub_sub_list()

    menu3_count = menu_page.menu3_items.count()
    assert menu3_count > 0, "Menu level 3 is empty"

    for j in range(menu3_count):
        locator3 = menu_page.menu3_items.nth(j)
        expect(locator3).to_be_visible(timeout=2000)
