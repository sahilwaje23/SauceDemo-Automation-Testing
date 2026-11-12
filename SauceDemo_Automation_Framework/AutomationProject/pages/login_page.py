"""Login page object."""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.config import BASE_URL


class LoginPage(BasePage):
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN = (By.ID, "login-button")
    ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    def open(self):
        self.driver.get(BASE_URL)
        self.visible(self.USERNAME)
        return self

    def login(self, username, password):
        self.enter(self.USERNAME, username)
        self.enter(self.PASSWORD, password)
        self.click(self.LOGIN)

    def error_message(self):
        return self.text(self.ERROR)
