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

# Dummy passenger data
dummy_passenger = {
    "firstName": "John",
    "lastName": "Doe",
    "dob": "01-01-1990",
    "passportNumber": "A1234567",
    "country": "UAE",
    "stat": "Single",
    "phNumber": "1234567890",
    "email": "john.doe@example.com"
}


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
        login_if_not_logged_in()

        print("\n" + "=" * 60)
        print(f"Testing Flight Search: FROM='{data['from']}', TO='{data['to']}', DATE='{data['departDate']}'")

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
        toast_message = get_toast_message()
        print(f"Toast message: {toast_message}")

        if data["expected_message"] in (toast_message or ""):
            print("✅ Flight Search Test passed.")
            return toast_message and "fetched successfull" in toast_message
        else:
            print("❌ Flight Search Test failed.")
            return False
    except Exception as e:
        print(f"🚨 Error during flight search: {e}")
        return False


def proceed_to_booking():
    try:
        print("\nStarting booking flow...")

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

        click_button_with_text("Next")

        fill_passenger_details()

        click_button_with_text("Next")

        for checkbox_id in ["agreement", "terms"]:
            checkbox = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, checkbox_id))
            )
            if not checkbox.is_selected():
                checkbox.click()
            time.sleep(0.5)

        click_button_with_text("Next")

        print("✅ Booking flow steps completed, ready for payment.")
        return True
    except TimeoutException:
        print("❌ Booking flow failed: Timeout waiting for element.")
        return False
    except Exception as e:
        print(f"❌ Booking flow error: {e}")
        return False


def fill_passenger_details():
    driver.find_element(By.ID, "firstName-1").send_keys(dummy_passenger["firstName"])
    driver.find_element(By.ID, "lastName-1").send_keys(dummy_passenger["lastName"])
    # Uncomment if needed
    # driver.find_element(By.ID, "dob-1").send_keys(dummy_passenger["dob"])
    # driver.find_element(By.ID, "passportNumber-1").send_keys(dummy_passenger["passportNumber"])
    # driver.find_element(By.ID, "country-1").send_keys(dummy_passenger["country"])
    # driver.find_element(By.ID, "stat-1").send_keys(dummy_passenger["stat"])
    driver.find_element(By.ID, "phNumber-1").send_keys(dummy_passenger["phNumber"])
    driver.find_element(By.ID, "email-1").send_keys(dummy_passenger["email"])
    time.sleep(1)


# -------------------------
# Payment Test
# -------------------------

def fill_payment_details():
    time.sleep(1)
    card_number = driver.find_element(By.NAME, "cardNumber")
    card_number.clear()
    card_number.send_keys("4242424242424242")

    expiry = driver.find_element(By.NAME, "cardExpiry")
    expiry.clear()
    future_month = random.randint(1, 12)
    future_year = datetime.datetime.now().year + random.randint(1, 5)
    expiry_value = f"{future_month:02d}/{str(future_year)[2:]}"  # MM/YY
    expiry.send_keys(expiry_value)

    cvc = driver.find_element(By.NAME, "cardCvc")
    cvc.clear()
    cvc.send_keys("564")

    billing_name = driver.find_element(By.NAME, "billingName")
    billing_name.clear()
    billing_name.send_keys("John Doe")

    time.sleep(1)


def perform_payment():
    try:
        time.sleep(1)
        print("\nStarting payment flow...")

        fill_payment_details()

        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "SubmitButton--complete"))
        )
        submit_button.click()

        confirmation = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h3[contains(text(),'Payment Done!')]"))
        )
        if confirmation:
            print("✅ Payment successful - Payment Done message found.")
            return True
        else:
            print("❌ Payment confirmation message not found.")
            return False
    except TimeoutException:
        print("❌ Payment flow failed: Timeout waiting for element.")
        return False
    except Exception as e:
        print(f"❌ Payment flow error: {e}")
        return False


# -------------------------
# Test Cases
# -------------------------

flight_search_cases = [
    {
        "from": "Dubai",
        "to": "London",
        "departDate": "15-06-2025",
        "expected_message": "flights fetched successfull"
    },
    # Additional test cases can be added here...
]

# -------------------------
# Main Execution
# -------------------------

try:
    for case in flight_search_cases:
        search_success = perform_flight_search(case)

        if search_success:
            booking_success = proceed_to_booking()
            if booking_success:
                payment_success = perform_payment()
                if payment_success:
                    print("🎉 Full booking and payment flow succeeded.")
                else:
                    print("⚠️ Payment failed.")
            else:
                print("⚠️ Booking failed.")
        else:
            print("⚠️ Flight search failed, skipping booking/payment.")

        time.sleep(2)
finally:
    print("\nClosing browser...")
    driver.quit()
