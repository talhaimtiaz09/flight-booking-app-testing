from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import random
import time
import datetime


# Setup Chrome WebDriver
service = Service(executable_path='/opt/homebrew/bin/chromedriver')
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(5)


# -------------------------
# Helper Functions
# -------------------------

def get_toast_message():
    try:
        toast = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "Toastify__toast"))
        )
        return toast.text.strip().lower()
    except Exception:
        return None


def click_button_with_text(text):
    buttons = driver.find_elements(By.TAG_NAME, "button")
    for btn in buttons:
        if btn.text.strip().lower() == text.lower():
            btn.click()
            return
    raise Exception(f"Button with text '{text}' not found")


def login_if_not_logged_in(email="test@test.com", password="Test@123"):
    print("\n" + "=" * 50)
    print("Checking login state...")

    driver.get("http://localhost:5173")

    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, "logout-button"))
        )
        print("✅ Already logged in. No need to log in again.")
        return True
    except:
        print("🔐 Not logged in. Performing login...")

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
    toast = get_toast_message()

    if toast and "user logged in successfully" in toast:
        print("✅ Login successful.")
        return True
    else:
        print(f"❌ Login failed. Toast: {toast}")
        return False


# -------------------------
# Flight Search & Booking Test
# -------------------------
def perform_flight_search(data):
    try:
        # if not login_if_not_logged_in():
        #     print("❌ Login failed, skipping this test.")
        #     return False

        print("\n" + "=" * 60)
        print(f"Testing Flight Search: FROM='{data['from']}', TO='{data['to']}', DATE='{data['departDate']}'")

        driver.get("http://localhost:5173/search")
        time.sleep(1)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "from")))

        # Fill form fields with delay
        from_input = driver.find_element(By.NAME, "from")
        from_input.clear()
        from_input.send_keys(data["from"])
        time.sleep(0.5)

        to_input = driver.find_element(By.NAME, "to")
        to_input.clear()
        to_input.send_keys(data["to"])
        time.sleep(0.5)

        date_input = driver.find_element(By.NAME, "departDate")
        date_input.clear()
        date_input.send_keys(data["departDate"])
        time.sleep(0.5)

        driver.find_element(By.ID, "search-button").click()

        time.sleep(2)
        toast_message = get_toast_message()
        print(f"🧾 Toast message: {toast_message}")

        # Check if test passed
        expected = data["expected_success"]
        actual_success = toast_message and "fetched successfull" in toast_message

        if actual_success == expected:
            print("✅ Flight Search Test PASSED.\n")
            return True
        else:
            print("❌ Flight Search Test FAILED.\n")
            return False
    except Exception as e:
        print(f"🚨 Error during flight search: {e}")
        return False


# -------------------------
# Test Cases (valid + invalid)
# -------------------------

flight_search_cases = [
    {
        "from": "Dubai",
        "to": "London",
        "departDate": "15-06-2025",
        "expected_success": True
    },
    {
        "from": "",
        "to": "London",
        "departDate": "15-06-2025",
        "expected_success": False  # Invalid: missing departure city
    },
    {
        "from": "Dubai",
        "to": "",
        "departDate": "15-06-2025",
        "expected_success": False  # Invalid: missing destination
    },
    {
        "from": "New York",
        "to": "Tokyo",
        "departDate": "01-01-2000",  # Past date
        "expected_success": False
    },
    {
        "from": "Dubai",
        "to": "London",
        "departDate": "invalid-date",
        "expected_success": False
    }
]

# -------------------------
# Main Execution
# -------------------------

try:
    for idx, case in enumerate(flight_search_cases, 1):
        print(f"\n🔎 Running Test Case {idx} ----------------------------")
        result = perform_flight_search(case)
        if result:
            print("✅ Search test passed ✅")
        else:
            print("❌ Search test failed ❌")

        time.sleep(2)
finally:
    print("\n🔚 Closing browser...")
    driver.quit()
