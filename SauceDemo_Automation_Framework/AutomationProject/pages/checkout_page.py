"""Checkout information, overview and completion page object."""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE = (By.ID, "continue")
    ERROR = (By.CSS_SELECTOR, "[data-test='error']")
    FINISH = (By.ID, "finish")
    COMPLETE_HEADER = (By.CSS_SELECTOR, ".complete-header")

    def fill_information(self, first, last, postal):
        self.enter(self.FIRST_NAME, first)
        self.enter(self.LAST_NAME, last)
        self.enter(self.POSTAL_CODE, postal)

    def continue_checkout(self):
        self.click(self.CONTINUE)

    def error_message(self):
        return self.text(self.ERROR)

    def finish(self):
        self.click(self.FINISH)

    def success_message(self):
        return self.text(self.COMPLETE_HEADER)
