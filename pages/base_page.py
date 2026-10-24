"""Base class that holds actions common to every page object."""

from __future__ import annotations

from playwright.sync_api import Page, Response


class BasePage:
   

    def __init__(self, page: Page) -> None:
        self.page = page

    def open(self, url: str) -> Response | None:

        """Navigate to the given URL and return the main-frame response."""

        return self.page.goto(url, wait_until="domcontentloaded")

    def go_back(self) -> None:

        """Go one step back in the browser history."""
        
        self.page.go_back(wait_until="domcontentloaded")

    @property
    def current_url(self) -> str:
        return self.page.url