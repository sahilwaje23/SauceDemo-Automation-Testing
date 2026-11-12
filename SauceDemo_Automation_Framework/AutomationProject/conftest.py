"""Browser fixtures, setup/teardown, logs, and failure screenshots."""
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService

os.environ.setdefault("WDM_LOCAL", "1")
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from utils.config import BROWSER, HEADLESS, PROJECT_ROOT, REPORTS
from utils.logger import get_logger

logger = get_logger(__name__)
_chrome_path = None
_edge_path = None
_chrome_wdm_failed = False
_edge_wdm_failed = False


@pytest.fixture
def driver(request):
    global _chrome_path, _edge_path, _chrome_wdm_failed, _edge_wdm_failed
    if BROWSER == "edge":
        options = EdgeOptions()
        if HEADLESS:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1440,1000")
        try:
            if _edge_wdm_failed:
                raise RuntimeError("Using Selenium Manager after WebDriver Manager failure")
            _edge_path = _edge_path or EdgeChromiumDriverManager().install()
            browser = webdriver.Edge(service=EdgeService(_edge_path), options=options)
        except Exception:
            _edge_wdm_failed = True
            logger.exception("Edge WebDriver Manager failed; using Selenium Manager")
            browser = webdriver.Edge(options=options)
    else:
        options = ChromeOptions()
        if HEADLESS:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1440,1000")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        try:
            if _chrome_wdm_failed:
                raise RuntimeError("Using Selenium Manager after WebDriver Manager failure")
            _chrome_path = _chrome_path or ChromeDriverManager().install()
            browser = webdriver.Chrome(service=ChromeService(_chrome_path), options=options)
        except Exception:
            _chrome_wdm_failed = True
            logger.exception("Chrome WebDriver Manager failed; using Selenium Manager")
            browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(0)
    request.node._driver = browser
    logger.info("START %s", request.node.nodeid)
    yield browser
    browser.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call":
        return
    status = "PASS" if report.passed else "FAIL" if report.failed else "SKIP"
    logger.info("%s %s", status, item.nodeid)
    if report.failed and hasattr(item, "_driver"):
        image_dir = REPORTS / "screenshots"
        image_dir.mkdir(parents=True, exist_ok=True)
        image_path = image_dir / f"{item.name}.png"
        try:
            item._driver.save_screenshot(str(image_path))
            from pytest_html import extras
            report.extras = getattr(report, "extras", [])
            report.extras.append(extras.image(str(image_path), name="Failure screenshot"))
            logger.error("Failure screenshot saved: %s", image_path)
        except Exception:
            logger.exception("Could not save failure screenshot")
