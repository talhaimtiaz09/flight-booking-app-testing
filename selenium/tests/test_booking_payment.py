import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import random
import datetime

@pytest.fixture(scope="session")
def driver():
    service = Service(executable_path='/opt/homebrew/bin/chromedriver')
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

@pytest.fixture(scope="session")
def dummy_passenger():
    return {
        "firstName": "John",
        "lastName": "Doe",
        "dob": "01-01-1990",
        "passportNumber": "A1234567",
        "country": "UAE",
        "stat": "Single",
        "phNumber": "1234567890",
        "email": "john.doe@example.com"
    }

@pytest.fixture(scope="session")
def test_context():
    # This dict will hold shared state between tests
    return {}

def login_if_not_logged_in(driver):
    driver.get("http://localhost:5173")
    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, "logout-button"))
        )
        return True
    except:
        driver.get('http://localhost:5173/login')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))

        email_input = driver.find_element(By.ID, "email")
        password_input = driver.find_element(By.ID, "password")

        email_input.clear()
        password_input.clear()

        email_input.send_keys("test@test.com")
        password_input.send_keys("Test@123")
        password_input.send_keys(Keys.RETURN)

        time.sleep(2)
        # Optionally check for success toast here
        return True

def perform_flight_search(driver, data):
    login_if_not_logged_in(driver)
    driver.get("http://localhost:5173/search")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "from")))

    driver.find_element(By.NAME, "from").clear()
    driver.find_element(By.NAME, "from").send_keys(data["from"])

    driver.find_element(By.NAME, "to").clear()
    driver.find_element(By.NAME, "to").send_keys(data["to"])

    driver.find_element(By.NAME, "departDate").clear()
    driver.find_element(By.NAME, "departDate").send_keys(data["departDate"])

    driver.find_element(By.ID, "search-button").click()
    time.sleep(2)

    # Check if flights found by presence of flight card element
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "searched-flight"))
        )
        return True
    except:
        return False

def proceed_to_booking(driver, dummy_passenger):
    try:
        flight_card = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "searched-flight"))
        )
        flight_card.click()
        time.sleep(1)

        seat = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "seatsHover"))
        )
        seat.click()
        time.sleep(1)

        driver.find_element(By.XPATH, "//button[contains(text(),'Next')]").click()

        driver.find_element(By.ID, "firstName-1").send_keys(dummy_passenger["firstName"])
        driver.find_element(By.ID, "lastName-1").send_keys(dummy_passenger["lastName"])
        driver.find_element(By.ID, "phNumber-1").send_keys(dummy_passenger["phNumber"])
        driver.find_element(By.ID, "email-1").send_keys(dummy_passenger["email"])
        time.sleep(1)

        driver.find_element(By.XPATH, "//button[contains(text(),'Next')]").click()

        for checkbox_id in ["agreement", "terms"]:
            checkbox = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, checkbox_id))
            )
            if not checkbox.is_selected():
                checkbox.click()
            time.sleep(0.5)

        driver.find_element(By.XPATH, "//button[contains(text(),'Next')]").click()
        return True
    except Exception:
        return False

def fill_payment_details(driver):
    driver.find_element(By.NAME, "cardNumber").clear()
    driver.find_element(By.NAME, "cardNumber").send_keys("4242424242424242")

    expiry = driver.find_element(By.NAME, "cardExpiry")
    expiry.clear()
    future_month = random.randint(1, 12)
    future_year = datetime.datetime.now().year + random.randint(1, 5)
    expiry_value = f"{future_month:02d}/{str(future_year)[2:]}"  # MM/YY
    expiry.send_keys(expiry_value)

    driver.find_element(By.NAME, "cardCvc").clear()
    driver.find_element(By.NAME, "cardCvc").send_keys("564")

    driver.find_element(By.NAME, "billingName").clear()
    driver.find_element(By.NAME, "billingName").send_keys("John Doe")

@pytest.mark.parametrize("flight_data", [
    {
        "from": "Dubai",
        "to": "London",
        "departDate": "15-06-2025"
    }
])
def test_flight_search(driver, flight_data, test_context):
    assert perform_flight_search(driver, flight_data)
    test_context["flight_search_done"] = True

@pytest.mark.dependency(depends=["test_flight_search"])
def test_booking_flow(driver, dummy_passenger, test_context):
    assert test_context.get("flight_search_done", False), "Flight search must succeed before booking"
    assert proceed_to_booking(driver, dummy_passenger)
    test_context["booking_done"] = True

@pytest.mark.dependency(depends=["test_booking_flow"])
def test_payment_flow(driver, test_context):
    assert test_context.get("booking_done", False), "Booking must succeed before payment"
    fill_payment_details(driver)

    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "SubmitButton--complete"))
    )
    submit_button.click()

    confirmation = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h3[contains(text(),'Payment Done!')]"))
    )
    assert confirmation is not None
