"""File and console logging shared by tests and pages."""
import logging
from logging.handlers import RotatingFileHandler
from utils.config import REPORTS


def get_logger(name):
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    log_dir = REPORTS / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    file_handler = RotatingFileHandler(log_dir / "automation.log", maxBytes=2_000_000, backupCount=3, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)
    logger.propagate = False
    return logger
