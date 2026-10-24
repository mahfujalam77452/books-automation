"""Test Case 3: Book data consistency validation."""
import allure
import pytest
from playwright.sync_api import expect

from config import settings


@allure.feature("Data Consistency")
@pytest.mark.regression
class TestBookDataConsistency:

    @allure.title("TC03 - Homepage title and price match the details page (5 random books)")
    def test_book_data_consistency(self, home_page, book_details_page):
        home_page.open_home()
        home_page.wait_for_books()
        indexes = home_page.get_random_book_indexes(settings.RANDOM_BOOK_COUNT)

        for index in indexes:
            home_title = home_page.get_book_title(index)
            home_price = home_page.get_book_price(index)

            with allure.step(f"Open book #{index}: {home_title}"):
                home_page.click_book(index)
                details_title = book_details_page.get_title()
                details_price = book_details_page.get_price()

            with allure.step("Compare homepage and details page data"):
                assert home_title == details_title, (
                    f"Title mismatch: home={home_title!r}, details={details_title!r}"
                )
                assert home_price == details_price, (
                    f"Price mismatch: home={home_price!r}, details={details_price!r}"
                )

            with allure.step("Go back to homepage"):
                book_details_page.go_back()
                expect(home_page.page).to_have_url(settings.HOME_URL)
                home_page.wait_for_books()