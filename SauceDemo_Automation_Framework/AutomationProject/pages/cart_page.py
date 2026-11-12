"""Shopping cart page object."""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    ITEMS = (By.CSS_SELECTOR, ".cart_item")
    CHECKOUT = (By.ID, "checkout")

    def item_names(self):
        return [item.find_element(By.CSS_SELECTOR, ".inventory_item_name").text for item in self.driver.find_elements(*self.ITEMS)]

    def item_prices(self):
        return [item.find_element(By.CSS_SELECTOR, ".inventory_item_price").text for item in self.driver.find_elements(*self.ITEMS)]

    def remove(self, name):
        for item in self.driver.find_elements(*self.ITEMS):
            if item.find_element(By.CSS_SELECTOR, ".inventory_item_name").text == name:
                item.find_element(By.CSS_SELECTOR, "button").click()
                return
        raise AssertionError(f"Cart item not found: {name}")

    def checkout(self):
        self.click(self.CHECKOUT)
