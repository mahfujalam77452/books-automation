"""Test Case 5: Product image validation with pagination."""
import allure
import pytest
from playwright.sync_api import expect

from config import settings


@allure.feature("Product Images")
@pytest.mark.regression
class TestProductImages:

    @allure.title("TC05 - Product images are valid on up to 5 pages")
    def test_product_images_with_pagination(self, home_page):
        home_page.open_home()
        home_page.wait_for_books()

        for page_number in range(1, settings.MAX_PAGES + 1):
            with allure.step(f"Validate images on page {page_number}"):
                expect(home_page.current_page_label).to_contain_text(f"Page {page_number} of")
                assert home_page.product_images.count() > 0, "No product images found"
                errors = home_page.get_image_errors()
                assert not errors, f"Page {page_number}:\n" + "\n".join(errors)

            if page_number == settings.MAX_PAGES or not home_page.has_next_page():
                break

            with allure.step("Click Next"):
                home_page.click_next()