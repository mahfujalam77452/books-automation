"""Test Case 4: Broken link validation."""
import allure
import pytest


@allure.feature("Links")
@pytest.mark.regression
class TestBrokenLinks:

    @allure.title("TC04 - All homepage links return HTTP 200")
    def test_no_broken_links(self, home_page):
        home_page.open_home()
        home_page.wait_for_books()

        with allure.step("Collect unique links"):
            urls = home_page.get_unique_link_urls()
            assert urls, "No links found on the homepage"
            allure.attach("\n".join(urls), name=f"{len(urls)} links checked",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step(f"Check status of {len(urls)} links"):
            broken = []
            for url in urls:
                status = home_page.get_status(url)
                if status != 200:
                    broken.append(f"{url} -> {status}")
            assert not broken, f"{len(broken)} broken link(s):\n" + "\n".join(broken)