"""Home page object."""

from pages.base_page import BasePage


class HomePage(BasePage):
    """Page object for the home page."""

    def open(self, url):
        """Navigate to the home page."""
        self.driver.get(url)
