"""Project settings."""

from urllib.parse import urljoin

BOOKS_BASE_URL =  "https://books.toscrape.com/"
HOME_URL = urljoin(BOOKS_BASE_URL, "index.html")
HOME_TITLE = "All products | Books to Scrape - Sandbox"
HOME_MAIN_HEADING = "All products"

QUOTES_BASE_URL = "https://quotes.toscrape.com/"
QUOTES_LOGIN_URL = QUOTES_BASE_URL + "login"
QUOTES_TITLE = "Quotes to Scrape"

DEFAULT_TIMEOUT_MS = 15_000
NAVIGATION_TIMEOUT_MS = 30_000
RANDOM_BOOK_COUNT = 5
MAX_PAGES = 5
# Time the test waits for you to type credentials and click Login.
MANUAL_LOGIN_TIMEOUT_MS = 120_000
