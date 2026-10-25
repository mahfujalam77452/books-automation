"""Test Case 6: Login functionality and Logout link validation (manual credentials)."""
import logging

import allure
import pytest
from playwright.sync_api import expect

from config import settings

logger = logging.getLogger(__name__)


@allure.feature("Login")
@pytest.mark.manual
class TestQuotesLogin:

    @allure.title("TC06 - Login succeeds and the Logout link is visible and enabled")
    def test_login_and_logout_link(self, quotes_login_page):
        login = quotes_login_page

        with allure.step("Open Quotes to Scrape homepage"):
            response = login.open_home()
            assert response is not None and response.ok, f"Homepage failed: {response}"
            expect(login.page).to_have_title(settings.QUOTES_TITLE)

        with allure.step("Click the Login link"):
            expect(login.login_link).to_be_visible()
            login.click_login_link()

        with allure.step("Verify login page is loaded"):
            expect(login.page).to_have_url(settings.QUOTES_LOGIN_URL)
            expect(login.username_input).to_be_visible()
            expect(login.password_input).to_be_visible()

        with allure.step("Type username and password in the browser and click Login"):
            logger.info(
                ">>> ACTION NEEDED: type username + password in the browser and click Login "
                "(waiting up to %s seconds)", settings.MANUAL_LOGIN_TIMEOUT_MS // 1000
            )
            login_response = login.wait_for_manual_login()
            assert login_response.status < 400, (
                f"Login request failed with HTTP {login_response.status}"
            )

        with allure.step("Verify authenticated state"):
            expect(login.page).to_have_url(settings.QUOTES_BASE_URL)
            expect(login.login_link).to_be_hidden()

        with allure.step("Verify Logout link is visible and enabled"):
            expect(login.logout_link).to_be_visible()
            expect(login.logout_link).to_be_enabled()