# tests/conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

CHROMEDRIVER_PATH = '/opt/homebrew/bin/chromedriver'

@pytest.fixture(scope="function")
def driver():
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()
