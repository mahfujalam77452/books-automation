"""Page object for a book details page."""
from playwright.sync_api import Page

from pages.base_page import BasePage


class BookDetailsPage(BasePage):
    """Locators and actions for a single book page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.title_heading = page.locator("div.product_main h1")
        self.price = page.locator("div.product_main p.price_color")
        self.info_table = page.locator("table.table-striped")
        self.info_rows = page.locator("table.table-striped tr")

    def get_title(self) -> str:
        """Return the H1 title (waits until it is visible)."""
        self.title_heading.wait_for(state="visible")
        return self.title_heading.inner_text().strip()

    def get_price(self) -> str:
        """Return the price text, e.g. '£51.77'."""
        self.price.wait_for(state="visible")
        return self.price.inner_text().strip()