"""Login tests using equivalence classes and username boundary values."""
import csv
import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.config import PASSWORD, PROJECT_ROOT, USERNAME


def login_rows():
    with (PROJECT_ROOT / "testdata/login_data.csv").open(newline="", encoding="utf-8-sig") as stream:
        return list(csv.DictReader(stream))


@pytest.mark.smoke
@pytest.mark.regression
def test_fr01_valid_login_redirects_to_products(driver):
    LoginPage(driver).open().login(USERNAME, PASSWORD)
    assert ProductsPage(driver).is_loaded()
    assert "/inventory.html" in driver.current_url


@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.parametrize("case", [r for r in login_rows() if r["case_id"] in {"FR02", "FR03", "FR04"}], ids=lambda r: r["case_id"])
def test_fr02_fr03_fr04_login_validation(driver, case):
    page = LoginPage(driver).open()
    page.login(case["username"], case["password"])
    assert page.error_message()
    assert "/inventory.html" not in driver.current_url


@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.parametrize("case", [r for r in login_rows() if r["case_id"].startswith("FR05")], ids=lambda r: r["case_id"])
def test_fr05_username_boundary_values(driver, case):
    page = LoginPage(driver).open()
    page.login(case["username"], case["password"])
    assert page.error_message()
    assert "/inventory.html" not in driver.current_url
