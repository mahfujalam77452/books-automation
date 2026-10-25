
from __future__ import annotations
from playwright.sync_api import Page, Response
from config import settings
from pages.base_page import BasePage
import random

class HomePage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.main_heading = page.locator("h1")
        self.headings = page.locator("h1, h2, h3, h4, h5, h6")
        self.books_section = page.locator("ol.row")
        self.book_items = page.locator("article.product_pod")
        self.product_images = page.locator("article.product_pod img")
        self.next_button = page.locator("li.next a")
        self.current_page_label = page.locator("li.current")

    def open_home(self) -> Response | None:
        """Open the homepage."""
        return self.open(settings.HOME_URL)
    
    def wait_for_books(self) -> None:
        """Wait until the first book is visible."""
        self.book_items.first.wait_for(state="visible")

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
    def get_random_book_indexes(self, count: int) -> list[int]:
        """Return `count` different random book positions (0-based)."""
        total = self.get_book_count()
        return random.sample(range(total), min(count, total))

    def get_book_title(self, index: int) -> str:
        """Return the full book title (the visible text is shortened with '...')."""
        link = self.book_items.nth(index).locator("h3 a")
        return link.get_attribute("title").strip()

    def get_book_price(self, index: int) -> str:
        """Return the price text, e.g. '£51.77'."""
        return self.book_items.nth(index).locator("p.price_color").inner_text().strip()

    def click_book(self, index: int) -> None:
        """Click the book at the given position."""
        self.book_items.nth(index).locator("h3 a").click()

    def get_unique_link_urls(self) -> list[str]:
        """Return all unique http(s) link URLs on the page (fragments removed)."""
        hrefs = self.page.locator("a").evaluate_all("els => els.map(e => e.href)")
        urls = {href.split("#")[0] for href in hrefs if href.startswith("http")}
        return sorted(urls)

    def get_image_errors(self) -> list[str]:
        """Check every product image and return a list of problems (empty = all good)."""
        self.page.wait_for_load_state("load")
        self.product_images.first.wait_for(state="visible")
        errors = []
        for i in range(self.product_images.count()):
            image = self.product_images.nth(i)
            name = f"image #{i + 1}"
            if not image.is_visible():
                errors.append(f"{name}: not visible")
            if not (image.get_attribute("src") or "").strip():
                errors.append(f"{name}: src is missing or empty")
            if not (image.get_attribute("alt") or "").strip():
                errors.append(f"{name}: alt is missing or empty")
            if "thumbnail" not in (image.get_attribute("class") or "").split():
                errors.append(f"{name}: class does not contain 'thumbnail'")
            if not image.evaluate("el => el.complete && el.naturalWidth > 0"):
                errors.append(f"{name}: image did not render")
        return errors

    def has_next_page(self) -> bool:
        """Return True if a Next button exists."""
        return self.next_button.count() > 0

    def click_next(self) -> None:
        """Click the Next button."""
        self.next_button.click()