from pages.alerts.modal_page import ModalDialogsPage


def test_small_modal(modal_page):
    modal_page.open_small_modal()
    assert modal_page.get_modal_title() == "Small Modal"
    modal_page.close_small_modal()


def test_large_modal(modal_page: ModalDialogsPage):
    modal_page.open_large_modal()
    assert modal_page.get_modal_title() == "Large Modal"
    assert len(modal_page.get_modal_body()) > 20
    modal_page.close_large_modal()
