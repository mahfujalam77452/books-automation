"""Shared fixtures. pytest loads this file automatically."""
import pytest
from playwright.sync_api import Page

from config import settings
from pages.book_details_page import BookDetailsPage
from pages.home_page import HomePage
from pages.quotes_login_page import QuotesLoginPage

@pytest.fixture(autouse=True)
def configure_timeouts(page: Page) -> None:
    """Apply project-wide timeouts to every test's page."""
    page.set_default_timeout(settings.DEFAULT_TIMEOUT_MS)
    page.set_default_navigation_timeout(settings.NAVIGATION_TIMEOUT_MS)


@pytest.fixture
def home_page(page: Page) -> HomePage:
    """Provide a HomePage object (a fresh page per test)."""
    return HomePage(page)
@pytest.fixture
def book_details_page(page: Page) -> BookDetailsPage:
    return BookDetailsPage(page)


@pytest.fixture
def quotes_login_page(page: Page) -> QuotesLoginPage:
    return QuotesLoginPage(page)

@pytest.fixture
def mobile_home_page(browser, playwright) -> HomePage:
    """HomePage opened in an iPhone 12 emulated context."""
    context = browser.new_context(**playwright.devices["iPhone 12"])
    mobile_page = context.new_page()
    mobile_page.set_default_timeout(settings.DEFAULT_TIMEOUT_MS)
    mobile_page.set_default_navigation_timeout(settings.NAVIGATION_TIMEOUT_MS)
    yield HomePage(mobile_page)
    context.close()
@pytest.fixture
def book_details_page_for():
    """Return a factory that builds a BookDetailsPage for any given page."""
    return BookDetailsPage