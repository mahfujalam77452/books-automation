
from __future__ import annotations
from playwright.sync_api import Page, Response
from config import settings
from pages.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.main_heading = page.locator("h1")
        self.headings = page.locator("h1, h2, h3, h4, h5, h6")
        self.books_section = page.locator("ol.row")
        self.book_items = page.locator("article.product_pod")

    def open_home(self) -> Response | None:
        """Open the homepage."""
        return self.open(settings.HOME_URL)

    def get_visible_headings(self) -> list[tuple[str, str]]:
        """
        Return (tag_name, trimmed_text) for every visible heading (h1-h6).
        Waits until at least one heading is visible, so the result is never
        read from a half-loaded page. Hidden headings are ignored.
        """
        self.headings.first.wait_for(state="visible")
        result = []
        for heading in self.headings.all():
            if heading.is_visible():
                tag = heading.evaluate("el => el.tagName").lower()
                result.append((tag, heading.inner_text().strip()))
        return result

    def get_book_count(self) -> int:
        """Return the number of books displayed on the homepage."""
        return self.book_items.count()