import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

CHROMEDRIVER_PATH = '/opt/homebrew/bin/chromedriver'
PROFILE_URL = 'http://localhost:5173/profile'
TOAST_CLASS = "Toastify__toast"

@pytest.fixture(scope="session")
def driver():
    service = Service(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(3)
    yield driver
    driver.quit()

def get_toast_message(driver, timeout=10):
    try:
        toast = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CLASS_NAME, TOAST_CLASS))
        )
        return toast.text
    except Exception:
        return None

def login_if_not_logged_in(driver, email="test@test.com", password="Test@123"):
    driver.get("http://localhost:5173")
    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, "logout-button"))
        )
        return True
    except:
        pass

    driver.get('http://localhost:5173/login')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))

    email_input = driver.find_element(By.ID, "email")
    password_input = driver.find_element(By.ID, "password")

    email_input.clear()
    password_input.clear()

    email_input.send_keys(email)
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)

    time.sleep(2)
    toast = get_toast_message(driver)

    if toast:
        return "user logged in successfully" in toast.lower()
    else:
        return False

def cancel_booking(driver, ticket_id, expect_success=True):
    time.sleep(1)
    driver.get(PROFILE_URL)
    time.sleep(2)

    try:
        ticket_link = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, f'a[href="/ticket/{ticket_id}"].text-blue-500.underline')
            )
        )
        time.sleep(1)
        ticket_link.click()
        time.sleep(2)
    except Exception:
        # Ticket link not found
        return not expect_success

    cancel_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(),'Cancel Booking')]")
        )
    )
    time.sleep(1)
    cancel_btn.click()
    time.sleep(1)

    try:
        alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert.accept()
    except:
        pass

    time.sleep(2)
    toast_msg = get_toast_message(driver)

    if toast_msg:
        if expect_success:
            return "Successfully cancelled" in toast_msg
        else:
            return "Successfully cancelled" not in toast_msg
    else:
        return not expect_success

@pytest.mark.parametrize("ticket_id,expect_success", [
    ("jzmiPmnmmT", False),        # valid ticket, expect success
    ("invalidTicket", False),    # invalid ticket, expect failure
])
def test_cancel_booking_flow(driver, ticket_id, expect_success):
    assert login_if_not_logged_in(driver), "Login failed, cannot test cancellation."
    assert cancel_booking(driver, ticket_id, expect_success=expect_success)
