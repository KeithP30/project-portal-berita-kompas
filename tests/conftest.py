import csv
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="function")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_experimental_option(
        "prefs", {"profile.default_content_setting_values.notifications": 2}
    )
    options.page_load_strategy = "eager"

    if os.getenv("CI"):
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

    d = webdriver.Chrome(options=options)  
    d.set_page_load_timeout(60)
    yield d
    try:
        d.quit()
    except Exception:
        pass


def load_csv(filename):
    filepath = os.path.join(os.path.dirname(__file__), "..", "data", filename)
    with open(filepath, newline="", encoding="utf-8") as f:
        return [row for row in csv.DictReader(f)]