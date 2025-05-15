from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup WebDriver
CHROMEDRIVER_PATH = '/opt/homebrew/bin/chromedriver'
LOGIN_URL = 'http://localhost:5173/login'
TOAST_CLASS = "Toastify__toast"

service = Service(executable_path=CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(5)  # Implicit wait

# Test Data
valid_credentials = {"email": "test@test.com", "password": "Test@123"}

invalid_credentials = [
    # {"email": "test@test.com", "password": "Test@123"},
    {"email": "", "password": ""},
    {"email": "invalidemail", "password": "password123"},
    {"email": "testuser@example.com", "password": ""},
    {"email": "testuser@example.com", "password": "wrongpassword"}
]

# Helper: Generate toast message
def get_toast_message():
    try:
        toast = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, TOAST_CLASS))
        )
        return toast.text
    except Exception:
        return None

# Core: Perform login and check result
def perform_login(credentials):
    try:
        driver.get(LOGIN_URL)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )

        # Fill form
        email_input = driver.find_element(By.ID, "email")
        password_input = driver.find_element(By.ID, "password")
        email_input.clear()
        password_input.clear()
        email_input.send_keys(credentials["email"])
        password_input.send_keys(credentials["password"])
        password_input.send_keys(Keys.RETURN)

        # Allow time for toast
        time.sleep(2)
        toast_msg = get_toast_message()

        if toast_msg:
            print(f"🧾 Toast message: {toast_msg}")
            return "User logged in successfully" in toast_msg
        else:
            print("⚠️ No toast message appeared.")
            return False
    except Exception as e:
        print(f"❌ Exception during login: {e}")
        return False

# Test: Valid login
def test_valid_login():
    print("\n🔐 Testing VALID login")
    result = perform_login(valid_credentials)
    if result:
        print("✅ Valid login passed!")
    else:
        print("❌ Valid login failed!")
    assert result, "Valid login should succeed."

# Test: Invalid logins
def test_invalid_logins():
    for creds in invalid_credentials:
        print(f"\n🔐 Testing INVALID login with Email: '{creds['email']}' | Password: '{creds['password']}'")
        result = perform_login(creds)
        if not result:
            print("✅ Invalid login correctly rejected.")
        else:
            print("❌ Invalid login was incorrectly accepted!")
        assert not result, f"Invalid login should fail for: {creds['email']}"

# Main test execution
try:
    test_valid_login()
    test_invalid_logins()
    print("\n🎉 All tests completed successfully!")
except AssertionError as err:
    print(f"\n🛑 Test failed: {err}")
finally:
    print("\n🔚 Closing browser...")
    driver.quit()
