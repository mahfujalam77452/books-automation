"""Shared fixtures. pytest loads this file automatically."""
import pytest
from playwright.sync_api import Page

from config import settings
from pages.home_page import HomePage


@pytest.fixture(autouse=True)
def configure_timeouts(page: Page) -> None:
    """Apply project-wide timeouts to every test's page."""
    page.set_default_timeout(settings.DEFAULT_TIMEOUT_MS)
    page.set_default_navigation_timeout(settings.NAVIGATION_TIMEOUT_MS)


@pytest.fixture
def home_page(page: Page) -> HomePage:
    """Provide a HomePage object (a fresh page per test)."""
    return HomePage(page)