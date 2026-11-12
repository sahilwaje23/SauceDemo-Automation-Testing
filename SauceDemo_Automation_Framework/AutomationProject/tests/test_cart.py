"""Cart-to-checkout navigation."""
import pytest
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.config import PASSWORD, USERNAME


@pytest.mark.smoke
@pytest.mark.regression
def test_fr11_checkout_opens_your_information_page(driver):
    LoginPage(driver).open().login(USERNAME, PASSWORD)
    ProductsPage(driver).add_product("Sauce Labs Backpack")
    ProductsPage(driver).open_cart()
    CartPage(driver).checkout()
    assert "checkout-step-one" in driver.current_url
    assert CheckoutPage(driver).visible(CheckoutPage.FIRST_NAME).is_displayed()
