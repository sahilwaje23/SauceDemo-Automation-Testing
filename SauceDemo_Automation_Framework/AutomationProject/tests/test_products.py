"""Product, cart state, and logout protection."""
import pytest
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from utils.config import PASSWORD, USERNAME


@pytest.fixture
def products(driver):
    LoginPage(driver).open().login(USERNAME, PASSWORD)
    page = ProductsPage(driver)
    assert page.is_loaded()
    return page


@pytest.mark.smoke
@pytest.mark.regression
def test_fr06_six_products_show_names_prices_and_add_buttons(products):
    cards = products.driver.find_elements(*products.ITEMS)
    assert len(cards) >= 6
    for card in cards:
        assert card.find_element(By.CSS_SELECTOR, ".inventory_item_name").text
        assert card.find_element(By.CSS_SELECTOR, ".inventory_item_price").text.startswith("$")
        assert card.find_element(By.CSS_SELECTOR, "button").text == "Add to cart"


@pytest.mark.smoke
@pytest.mark.regression
def test_fr07_add_increments_badge_and_changes_button(products):
    name = "Sauce Labs Backpack"
    products.add_product(name)
    assert products.badge_count() == 1
    assert products.product_button_text(name) == "Remove"


@pytest.mark.regression
def test_fr08_remove_decrements_badge_and_restores_button(products):
    name = "Sauce Labs Backpack"
    products.add_product(name)
    products.add_product("Sauce Labs Bike Light")
    products.product(name).find_element(By.CSS_SELECTOR, "button").click()
    assert products.badge_count() == 1
    assert products.product_button_text(name) == "Add to cart"


@pytest.mark.regression
def test_fr09_cart_shows_product_name_and_price(products):
    name = "Sauce Labs Backpack"
    price = products.product_price(name)
    products.add_product(name)
    products.open_cart()
    cart = CartPage(products.driver)
    assert name in cart.item_names()
    assert price in cart.item_prices()


@pytest.mark.regression
def test_fr10_logout_blocks_inventory_access(driver):
    LoginPage(driver).open().login(USERNAME, PASSWORD)
    ProductsPage(driver).logout()
    assert "/inventory.html" not in driver.current_url
    driver.get("https://www.saucedemo.com/inventory.html")
    assert "/inventory.html" not in driver.current_url
    assert driver.find_element(By.ID, "login-button").is_displayed()
