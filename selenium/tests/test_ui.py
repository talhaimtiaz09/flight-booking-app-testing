import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

CHROMEDRIVER_PATH = '/opt/homebrew/bin/chromedriver'

@pytest.fixture(scope="module")
def driver():
    service = Service(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


def test_flight_management_ui(driver):
    try:
        print("🔗 Opening Flight Management page...")
        driver.get("http://localhost:5173/flight-management")
        time.sleep(1)

        print("🔍 Clicking 'Search Flights' button...")
        search_button = driver.find_element(By.XPATH, "//button[text()='Search Flights']")
        search_button.click()
        time.sleep(1)

        print("✅ Verifying 'All Flights' heading...")
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//h2[text()='All Flights']")
            )
        )
        print("🆗 'All Flights' found.")

        print("➕ Clicking 'Add Airline' button...")
        add_airline_button = driver.find_element(By.XPATH, "//button[text()='Add Airline']")
        add_airline_button.click()
        time.sleep(1)

        print("✅ Verifying 'Add Airline' form submit button...")
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[@type='submit' and contains(text(),'Add Airline')]")
            )
        )
        print("🆗 'Add Airline' submit button found.")

        print("✈️ Clicking 'Add Flight' button...")
        add_flight_button = driver.find_element(By.XPATH, "//button[text()='Add Flight']")
        add_flight_button.click()
        time.sleep(1)

        print("✅ Verifying 'Add Flight' form submit button...")
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[@type='submit' and contains(text(),'Add Flight')]")
            )
        )
        print("🆗 'Add Flight' submit button found.")
    except Exception as e:
        pytest.fail(f"Flight Management UI test failed: {e}")


def test_homepage_navigation_ui(driver):
    try:
        print("🔗 Opening homepage...")
        driver.get("http://localhost:5173/")
        time.sleep(1)

        print("🔎 Navigating to Search Flights page...")
        search_link = driver.find_element(By.CSS_SELECTOR, 'a[href="/search"].hover\\:text-gray-500')
        search_link.click()
        time.sleep(1)

        print("✅ Verifying Search Flights button...")
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "search-button"))
        )
        print("🆗 Search button found.")

        print("📊 Navigating to Dashboard...")
        dashboard_link = driver.find_element(By.CSS_SELECTOR, 'a[href="/flight-management"].hover\\:text-gray-500')
        dashboard_link.click()
        time.sleep(1)

        print("✅ Verifying dashboard heading...")
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//h1[contains(text(),'Flight Management Dashboard')]")
            )
        )
        print("🆗 Dashboard header found.")

        print("📨 Navigating to Contact Us...")
        contact_link = driver.find_element(By.CSS_SELECTOR, 'a[href="/contact"].hover\\:text-gray-500')
        contact_link.click()
        time.sleep(1)

        print("✅ Verifying 'Follow Us' section...")
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//h3[contains(text(),'Follow Us')]")
            )
        )
        print("🆗 'Follow Us' section found.")
    except Exception as e:
        pytest.fail(f"Homepage Navigation UI test failed: {e}")
