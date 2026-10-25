"""Bonus: Mobile device emulation (iPhone 12)."""
import allure
import pytest
from playwright.sync_api import expect

from config import settings


@allure.feature("Mobile")
@pytest.mark.mobile
class TestMobileHomepage:

    @allure.title("BONUS - Homepage works on an emulated iPhone 12")
    def test_mobile_homepage_and_book_navigation(self, mobile_home_page, book_details_page_for):
        home = mobile_home_page

        with allure.step("Open homepage on iPhone 12"):
            response = home.open_home()
            assert response is not None and response.ok
            expect(home.page).to_have_title(settings.HOME_TITLE)

        with allure.step("Verify mobile viewport is used"):
            assert home.page.evaluate("window.innerWidth") <= 500

        with allure.step("Verify books are displayed"):
            home.wait_for_books()
            expect(home.books_section).to_be_visible()
            assert home.get_book_count() >= 1

        with allure.step("Tap the first book and verify its title"):
            title = home.get_book_title(0)
            home.click_book(0)
            details = book_details_page_for(home.page)
            assert details.get_title() == title