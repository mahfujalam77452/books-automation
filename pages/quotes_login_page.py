"""Page object for Quotes to Scrape login flow."""
from __future__ import annotations

from playwright.sync_api import Page, Response

from config import settings
from pages.base_page import BasePage


class QuotesLoginPage(BasePage):
    """Locators and actions for the Quotes to Scrape login and logout."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.login_link = page.get_by_role("link", name="Login")
        self.logout_link = page.get_by_role("link", name="Logout")
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")

    def open_home(self) -> Response | None:
        """Open the Quotes to Scrape homepage."""
        return self.open(settings.QUOTES_BASE_URL)

    def click_login_link(self) -> None:
        """Click the Login link in the header."""
        self.login_link.click()

    def wait_for_manual_login(self) -> Response:
        """
        Wait until the person types the credentials in the browser and
        submits the form. Returns the login (POST) response.
        """
        return self.page.wait_for_event(
            "response",
            predicate=lambda r: r.request.method == "POST" and r.url.endswith("/login"),
            timeout=settings.MANUAL_LOGIN_TIMEOUT_MS,
        )