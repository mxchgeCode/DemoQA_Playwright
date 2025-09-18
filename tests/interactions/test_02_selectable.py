import logging

logger = logging.getLogger(__name__)


def test_select_list_items(selectable_page):
    selectable_page.activate_list_tab()
    items = selectable_page.get_list_items()
    logger.info(f"Доступные элементы списка: {items}")
    # Выбираем несколько элементов, например 0 и 2
    selectable_page.select_list_item(0)
    selectable_page.select_list_item(2)
    selected = selectable_page.get_selected_list_items()
    logger.info(f"Выбранные элементы списка после выбора: {selected}")
    assert items[0] in selected
    assert items[2] in selected


def test_select_grid_items(selectable_page):
    selectable_page.activate_grid_tab()
    items = selectable_page.get_grid_items()
    logger.info(f"Доступные элементы сетки: {items}")
    # Выбираем несколько элементов, например 3 и 5
    selectable_page.select_grid_item(3)
    selectable_page.select_grid_item(5)
    selected = selectable_page.get_selected_grid_items()
    logger.info(f"Выбранные элементы сетки после выбора: {selected}")
    assert items[3] in selected
    assert items[5] in selected
