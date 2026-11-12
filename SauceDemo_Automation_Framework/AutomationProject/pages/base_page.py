"""Shared Selenium actions using explicit waits."""
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utils.config import TIMEOUT_SECONDS
from utils.logger import get_logger


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, TIMEOUT_SECONDS)
        self.logger = get_logger(type(self).__name__)

    def visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        self.logger.info("Click %s", locator)
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def enter(self, locator, value):
        field = self.visible(locator)
        field.clear()
        field.send_keys(value)

    def text(self, locator):
        return self.visible(locator).text

    def exists(self, locator):
        return bool(self.driver.find_elements(*locator))
