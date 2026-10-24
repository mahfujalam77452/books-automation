"""Test Case 2: Random book navigation validation."""
import allure
import pytest
from playwright.sync_api import expect

from config import settings


@allure.feature("Book Navigation")
@pytest.mark.regression
class TestBookNavigation:

    @allure.title("TC02 - 5 random books open the correct details page")
    def test_random_book_navigation(self, home_page, book_details_page):
        home_page.open_home()
        home_page.wait_for_books()
        indexes = home_page.get_random_book_indexes(settings.RANDOM_BOOK_COUNT)

        for index in indexes:
            title = home_page.get_book_title(index)

            with allure.step(f"Open book #{index}: {title}"):
                home_page.click_book(index)

            with allure.step("Verify details page is loaded"):
                expect(home_page.page).not_to_have_url(settings.HOME_URL)
                assert book_details_page.get_title() == title

            with allure.step("Verify book information is visible"):
                expect(book_details_page.info_table).to_be_visible()
                assert book_details_page.info_rows.count() > 0

            with allure.step("Go back to homepage"):
                book_details_page.go_back()
                expect(home_page.page).to_have_url(settings.HOME_URL)
                home_page.wait_for_books()