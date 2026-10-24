"""Project settings."""

from urllib.parse import urljoin

BOOKS_BASE_URL =  "https://books.toscrape.com/"
HOME_URL = urljoin(BOOKS_BASE_URL, "index.html")
HOME_TITLE = "All products | Books to Scrape - Sandbox"
HOME_MAIN_HEADING = "All products"

DEFAULT_TIMEOUT_MS = 15_000
NAVIGATION_TIMEOUT_MS = 30_000
