def test_valid_image_not_broken(broken_links_page):
    assert (
        not broken_links_page.valid_image_broken()
    ), "Valid image should not be broken"


def test_broken_image_is_broken(broken_links_page):
    assert (
        broken_links_page.broken_image_broken()
    ), "Broken image should be detected as broken"


def test_valid_link_not_broken(broken_links_page):
    assert broken_links_page.is_valid_link_broken(), "Valid link should not be broken"


def test_broken_link_is_broken(broken_links_page):
    assert (
        broken_links_page.is_broken_link_broken()
    ), "Broken link should be detected as broken"
