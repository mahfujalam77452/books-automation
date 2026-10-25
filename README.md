# Books to Scrape - UI Automation Framework

## Project Overview

A UI automation framework built with **Playwright (Python)** and **Pytest**.
It validates the [Books to Scrape](https://books.toscrape.com/index.html) website
(homepage, book navigation, data consistency, links, images, pagination) and the
login flow of [Quotes to Scrape](https://quotes.toscrape.com/).

The project runs locally, inside Docker, and in GitHub Actions, and produces
an HTML report and an Allure report.

## Features

- Page Object Model with a shared `BasePage` (OOP, DRY)
- Auto-waiting locators and `expect` assertions, no hardcoded sleeps
- Random book selection (5 unique books per test)
- Broken link check with duplicate removal
- Image attribute validation across up to 5 pages
- Manual-credential login test (the person types in the browser)
- Mobile device emulation (bonus)
- Screenshots, videos and traces kept on failure
- HTML report (pytest-html) and Allure report
- Dockerfile and GitHub Actions pipeline

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.9+ (3.11 recommended) | Language |
| Playwright | Browser automation |
| Pytest + pytest-playwright | Test runner and Playwright fixtures |
| pytest-html | HTML report |
| allure-pytest | Allure results |
| Docker | Containerized execution |
| GitHub Actions | CI/CD |

## Installation Guide

```bash
git clone https://github.com/mahfujalam77452/books-automation
cd books-automation

python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux

pip install -r requirements.txt
playwright install chromium
```

## Environment Setup

- No credentials or secrets are needed. The login test asks the person to type
  the username and password in the browser.
- `config/settings.py` holds all URLs, timeouts and counts. Change values there.
- To view Allure reports locally install **Java** and the Allure CLI:
  `npm install -g allure-commandline`

## Running Tests

| Goal | Command |
|---|---|
| All automatic tests (headless) | `pytest -m "not manual"` |
| Everything incl. manual login (visible browser) | `pytest --headed` |
| One file | `pytest tests/test_homepage.py` |
| Mobile bonus only | `pytest -m mobile` |
| Manual login test only | `pytest tests/test_quotes_login.py --headed` |

**Manual login test:** the browser opens the login page and waits up to 2 minutes.
Type any username and password, then click **Login**. The test continues automatically.

**Docker:**

```bash
docker build -t books-automation .
docker run --rm \
  -v "$(pwd)/reports:/app/reports" \
  -v "$(pwd)/allure-results:/app/allure-results" \
  -v "$(pwd)/test-results:/app/test-results" \
  books-automation
```

## Project Structure

```
books-automation/
├── .github/workflows/playwright.yml   # CI pipeline
├── config/settings.py                 # URLs, timeouts, constants
├── pages/
│   ├── base_page.py                   # Shared browser actions
│   ├── home_page.py                   # Books homepage page object
│   ├── book_details_page.py           # Book details page object
│   └── quotes_login_page.py           # Quotes login page object
├── tests/
│   ├── test_homepage.py               # TC01
│   ├── test_book_navigation.py        # TC02
│   ├── test_book_data_consistency.py  # TC03
│   ├── test_broken_links.py           # TC04
│   ├── test_product_images.py         # TC05
│   ├── test_quotes_login.py           # TC06 (manual credentials)
│   └── test_mobile.py                 # Bonus
├── conftest.py                        # Fixtures
├── pytest.ini                         # Pytest and Playwright options
├── requirements.txt
├── Dockerfile
└── README.md
```

## Test Case Coverage

| ID | Test | What it checks |
|---|---|---|
| TC01 | Homepage validation | URL, title, visible headings have text, books section, at least one book |
| TC02 | Random book navigation | 5 unique random books: details page loads, H1 equals selected title, info table visible, back to homepage |
| TC03 | Data consistency | 5 unique random books: homepage title and price equal details page title and price |
| TC04 | Broken links | All unique links on the homepage return HTTP 200 |
| TC05 | Product images | Visible, `src`, `alt`, class `thumbnail`, rendered; up to 5 pages via Next |
| TC06 | Login / Logout link | Login link, login page, manual credentials, POST succeeds, Logout visible and enabled |
| Bonus | Mobile emulation | Homepage and book navigation on an emulated iPhone 12 |

## Report Generation Guide

Every `pytest` run generates both reports automatically (configured in `pytest.ini`):

| Output | Location |
|---|---|
| HTML report | `reports/report.html` |
| Test log | `reports/pytest.log` |
| Allure results | `allure-results/` |
| Screenshots, videos, traces (failures) | `test-results/` |

## HTML Report Guide

1. Run `pytest -m "not manual"`.
2. Open `reports/report.html` in any browser. It is self-contained, so it can be
   emailed or opened from the CI artifact without extra files.
3. It shows the summary, pass/fail status, duration and error details per test.

## Allure Report Guide

1. Run `pytest -m "not manual"` (creates `allure-results/`).
2. Open an interactive report: `allure serve allure-results`
3. Or generate a static report: `allure generate allure-results --clean -o allure-report`
   then `allure open allure-report`
4. Do not open `allure-report/index.html` by double click (browsers block it on `file://`).
   Always use `allure open`.

Each test shows its steps. Random tests show the selected book in the step names.

Open a failure trace with: `playwright show-trace test-results/<test-folder>/trace.zip`

## GitHub Actions Setup

The workflow is `.github/workflows/playwright.yml`. It runs on every **push** and
**pull request** to `main` or `master`.

Steps: checkout, set up Python, install dependencies, install Playwright browsers,
run tests (`-m "not manual"`), generate Allure report, upload artifacts.

Artifacts (Actions run page, bottom section):

| Artifact | Contents |
|---|---|
| `html-report` | `report.html` and `pytest.log` |
| `allure-results` | Raw Allure data |
| `allure-report` | Generated Allure report (use `allure open`) |
| `test-results` | Screenshots, videos and traces of failed tests |

Uploads use `if: always()`, so reports are available even when tests fail.
No secrets are required.

## Design Decisions

- **Page Object Model + BasePage:** locators and actions live in page classes, tests
  only describe the scenario. Shared actions are written once (DRY).
- **Full book title from the `title` attribute:** the visible title on the listing is
  shortened with `...`, so reading the text would give false mismatches.
- **`random.sample`:** guarantees 5 different books per test.
- **Next button instead of building URLs:** page 1 is `/index.html` but page 2 is
  `/catalogue/page-2.html`, so clicking Next is more reliable.
- **Link check with `page.request`:** no extra library; `a.href` returns absolute URLs
  and URL fragments are removed before de-duplication.
- **Image render check:** `naturalWidth > 0` proves the image really loaded, not just
  that `src` exists.
- **Synchronization:** only Playwright auto-wait, `wait_for` and `expect`. No `sleep`.
- **Manual login:** credentials are typed by the person, so nothing sensitive is stored
  in code, reports or CI. The test is marked `manual` and excluded from CI.

## Known Limitations

- **TC06 cannot run in CI or Docker** because a person must type the credentials.
  It is excluded with `-m "not manual"`.
- TC02 and TC03 pick books randomly without a fixed seed, so a failure on one book
  may not repeat on the next run. The failing book title is shown in the step name.
- TC02 and TC03 loop over 5 books inside one test, so the first failing book stops
  that test.
- TC04 checks links one by one, so it takes some seconds. It only covers links on
  the homepage.
- Books to Scrape and Quotes to Scrape are public demo sites; tests depend on their
  availability and current HTML structure.
- Only Chromium is configured by default. Use `--browser=firefox` or `--browser=webkit`
  after `playwright install` to try others.
- The mobile test uses a manually created context, so automatic screenshots, videos and
  traces are not recorded for it.