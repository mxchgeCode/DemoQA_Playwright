from data import URLs


def test_fill_form_and_submit(practice_form_page):
    practice_form_page.fill_first_name("John")
    practice_form_page.fill_last_name("Doe")
    practice_form_page.fill_email("john.doe@example.com")
    practice_form_page.select_gender("Male")
    practice_form_page.fill_mobile("1234567890")
    practice_form_page.fill_date_of_birth("10 Sep 1990")
    practice_form_page.fill_subjects(["Maths", "Physics"])
    practice_form_page.select_hobbies(["Sports", "Music"])
    practice_form_page.upload_picture(URLs.PICTURE_PATH)
    practice_form_page.fill_current_address("123 Main Street")
    practice_form_page.select_state("NCR")
    practice_form_page.select_city("Delhi")
    practice_form_page.submit_form()

    assert (
        practice_form_page.is_modal_visible()
    ), "Ожидался модальный диалог с результатами"
    practice_form_page.close_modal()
