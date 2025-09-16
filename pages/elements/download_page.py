import os
from playwright.sync_api import Page
from locators.elements.download_locators import UploadDownloadLocators
from data import URLs


class UploadDownloadPage:
    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto(URLs.DOWNLOAD)

    def upload_file(self, file_path: str):
        self.page.set_input_files(UploadDownloadLocators.UPLOAD_INPUT, file_path)

    def get_uploaded_files_path_text(self) -> str:
        return self.page.locator(UploadDownloadLocators.UPLOAD_PATH_TEXT).inner_text()

    def download_file(self, download_path: str) -> str:
        with self.page.expect_download() as download_info:
            self.page.click(UploadDownloadLocators.DOWNLOAD_BUTTON)
        download = download_info.value
        path = os.path.join(download_path, download.suggested_filename)
        download.save_as(path)
        return path
