from playwright.sync_api import Page

from data import URLs
from locators.alerts.modal_locators import ModalDialogsLocators


class ModalDialogsPage:
    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto(URLs.MODAL_DIALOGS)

    def open_small_modal(self):
        self.page.click(ModalDialogsLocators.SMALL_MODAL_BUTTON)
        self.page.wait_for_selector(ModalDialogsLocators.MODAL_CONTENT)

    def open_large_modal(self):
        self.page.click(ModalDialogsLocators.LARGE_MODAL_BUTTON)
        self.page.wait_for_selector(ModalDialogsLocators.MODAL_CONTENT)

    def get_modal_title(self) -> str:
        return self.page.text_content(ModalDialogsLocators.MODAL_TITLE).strip()

    def get_modal_body(self) -> str:
        return self.page.text_content(ModalDialogsLocators.MODAL_BODY).strip()

    def close_small_modal(self):
        self.page.click(ModalDialogsLocators.CLOSE_SMALL_MODAL_BUTTON)
        self.page.wait_for_selector(ModalDialogsLocators.MODAL_CONTENT, state="hidden")

    def close_large_modal(self):
        self.page.click(ModalDialogsLocators.CLOSE_LARGE_MODAL_BUTTON)
        self.page.wait_for_selector(ModalDialogsLocators.MODAL_CONTENT, state="hidden")
