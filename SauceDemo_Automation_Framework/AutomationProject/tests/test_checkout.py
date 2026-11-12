"""Checkout required fields, postal boundary, and completion."""
import csv
import pytest
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.config import PASSWORD, PROJECT_ROOT, USERNAME


def open_checkout(driver):
    LoginPage(driver).open().login(USERNAME, PASSWORD)
    ProductsPage(driver).add_product("Sauce Labs Backpack")
    ProductsPage(driver).open_cart()
    CartPage(driver).checkout()
    return CheckoutPage(driver)


def postal_rows():
    with (PROJECT_ROOT / "testdata/checkout_data.csv").open(newline="", encoding="utf-8-sig") as stream:
        return list(csv.DictReader(stream))


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.negative
def test_fr12_blank_first_name_error(driver):
    page = open_checkout(driver)
    page.fill_information("", "Tester", "12345")
    page.continue_checkout()
    assert page.error_message()


@pytest.mark.regression
@pytest.mark.negative
def test_fr13_blank_last_name_error(driver):
    page = open_checkout(driver)
    page.fill_information("Lab", "", "12345")
    page.continue_checkout()
    assert page.error_message()


@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.parametrize("case", postal_rows(), ids=lambda r: r["case_id"])
def test_fr14_postal_boundaries(driver, case):
    page = open_checkout(driver)
    page.fill_information(case["first_name"], case["last_name"], case["postal_code"])
    page.continue_checkout()
    if case["expected"] == "invalid":
        assert page.exists(page.ERROR), f"{case['case_id']} accepted by AUT, expected rejection"
        assert "checkout-step-one" in driver.current_url
    else:
        assert "checkout-step-two" in driver.current_url
        assert page.visible(page.FINISH)


@pytest.mark.regression
def test_fr15_valid_checkout_info_opens_overview(driver):
    page = open_checkout(driver)
    page.fill_information("Lab", "Tester", "12345")
    page.continue_checkout()
    assert "checkout-step-two" in driver.current_url
    assert page.visible(page.FINISH).is_displayed()


@pytest.mark.smoke
@pytest.mark.regression
def test_fr16_finish_order_shows_success(driver):
    page = open_checkout(driver)
    page.fill_information("Lab", "Tester", "12345")
    page.continue_checkout()
    page.finish()
    assert page.success_message() == "Thank you for your order!"
