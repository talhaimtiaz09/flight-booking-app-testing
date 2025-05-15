# tests/test_login.py
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

LOGIN_URL = 'http://localhost:5173/login'
TOAST_CLASS = "Toastify__toast"

test_cases = [
    pytest.param({"email": "test@test.com", "password": "Test@123"}, True, id="valid_login"),
    pytest.param({"email": "", "password": ""}, False, id="empty_email_password"),
    pytest.param({"email": "invalidemail", "password": "password123"}, False, id="invalid_email_format"),
    pytest.param({"email": "testuser@example.com", "password": ""}, False, id="empty_password"),
    pytest.param({"email": "testuser@example.com", "password": "wrongpassword"}, False, id="wrong_password"),
]

def get_toast_message(driver):
    try:
        toast = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, TOAST_CLASS))
        )
        return toast.text
    except Exception:
        return None

def perform_login(driver, credentials):
    driver.get(LOGIN_URL)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))

    email_input = driver.find_element(By.ID, "email")
    password_input = driver.find_element(By.ID, "password")
    email_input.clear()
    password_input.clear()

    email_input.send_keys(credentials["email"])
    password_input.send_keys(credentials["password"])
    password_input.send_keys(Keys.RETURN)

    time.sleep(2)
    return get_toast_message(driver)

@pytest.mark.parametrize("credentials, expected_success", test_cases)
def test_login_cases(driver, credentials, expected_success):
    toast = perform_login(driver, credentials)
    actual_success = toast and "user logged in successfully" in toast.lower()

    if expected_success:
        assert actual_success, f"Expected login to succeed for: {credentials}, but it failed. Toast: {toast}"
    else:
        assert not actual_success, f"Expected login to fail for: {credentials}, but it succeeded. Toast: {toast}"
