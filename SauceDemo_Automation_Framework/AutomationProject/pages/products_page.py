"""Product catalogue page object."""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProductsPage(BasePage):
    TITLE = (By.CSS_SELECTOR, ".title")
    ITEMS = (By.CSS_SELECTOR, ".inventory_item")
    CART_BADGE = (By.CSS_SELECTOR, ".shopping_cart_badge")
    CART_LINK = (By.CSS_SELECTOR, ".shopping_cart_link")
    MENU = (By.ID, "react-burger-menu-btn")
    LOGOUT = (By.ID, "logout_sidebar_link")

    def is_loaded(self):
        return self.text(self.TITLE) == "Products"

    def product(self, name):
        for card in self.driver.find_elements(*self.ITEMS):
            if card.find_element(By.CSS_SELECTOR, ".inventory_item_name").text == name:
                return card
        raise AssertionError(f"Product not found: {name}")

    def product_count(self):
        self.visible(self.TITLE)
        return len(self.driver.find_elements(*self.ITEMS))

    def product_price(self, name):
        return self.product(name).find_element(By.CSS_SELECTOR, ".inventory_item_price").text

    def add_product(self, name):
        self.product(name).find_element(By.CSS_SELECTOR, "button").click()

    def product_button_text(self, name):
        return self.product(name).find_element(By.CSS_SELECTOR, "button").text

    def badge_count(self):
        return int(self.driver.find_element(*self.CART_BADGE).text) if self.driver.find_elements(*self.CART_BADGE) else 0

    def open_cart(self):
        self.click(self.CART_LINK)

    def logout(self):
        self.click(self.MENU)
        self.click(self.LOGOUT)
