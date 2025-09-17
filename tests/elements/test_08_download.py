import os
import tempfile


def test_file_upload(upload_download_page):
    # Создаём временный файл для загрузки
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
        f.write(b"Hello, DemoQA!")
        tmp_file_path = f.name

    upload_download_page.upload_file(tmp_file_path)
    file_path_text = upload_download_page.get_uploaded_files_path_text()
    assert os.path.basename(tmp_file_path) in file_path_text

    os.remove(tmp_file_path)  # удаляем временный файл


def test_file_download(upload_download_page, tmp_path):
    download_path = str(tmp_path)
    saved_file = upload_download_page.download_file(download_path)
    assert os.path.exists(saved_file)
    assert os.path.getsize(saved_file) > 0
