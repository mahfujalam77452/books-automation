"""Test 1 : Homepage validation"""

import allure
import pytest
from playwright.sync_api import expect
from config import settings


@allure.feature("Homepage")
@pytest.mark.smoke

class TestHomePage:
    @allure.title("TC01 - Homepage loads with correct URL,tittle,headings and books")
    def test_homepage_validation(self,home_page):
        with allure.step("Open the homepage"):
            response = home_page.open_home()
            assert response is not None and response.ok,(
                f"Homepage did not load successfully. Status: {response.status if response else 'No response'}"
            )

        with allure.step("Verify page URL and title"):
            expect(home_page.page).to_have_url(settings.HOME_URL)
            expect(home_page.page).to_have_title(settings.HOME_TITLE)

        with allure.step("Verify main heading is visible"):
            expect(home_page.main_heading).to_be_visible()
            expect(home_page.main_heading).to_have_text(settings.HOME_MAIN_HEADING)
        with allure.step("Verify all visible headings (h1-h6) have text"):
            headings = home_page.get_visible_headings()
            assert headings, "No visible headings found on the homepage"
            empty = [tag for tag, text in headings if not text]
            assert not empty, f"{len(empty)} visible heading(s) have empty text: {empty}"

        with allure.step("Verify books section is visible"):
            expect(home_page.books_section).to_be_visible()

        with allure.step("Verify at least one book item is displayed"):
            expect(home_page.book_items.first).to_be_visible()
            assert home_page.get_book_count() >= 1, "Book list is empty"