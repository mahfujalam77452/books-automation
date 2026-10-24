"""Base page object definitions."""


class BasePage:
    """Common functionality for page objects."""

    def __init__(self, driver):
        self.driver = driver
