"""Runtime configuration, overridable through environment variables."""
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BASE_URL = os.getenv("SAUCEDEMO_BASE_URL", "https://www.saucedemo.com/")
USERNAME = os.getenv("SAUCEDEMO_USERNAME", "standard_user")
PASSWORD = os.getenv("SAUCEDEMO_PASSWORD", "secret_sauce")
BROWSER = os.getenv("BROWSER", "chrome").lower()
HEADLESS = os.getenv("HEADLESS", "true").lower() in {"1", "true", "yes"}
TIMEOUT_SECONDS = int(os.getenv("WAIT_TIMEOUT", "10"))
REPORTS = PROJECT_ROOT / "reports"
