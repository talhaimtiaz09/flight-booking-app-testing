from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # <-- Import Keys here
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup WebDriver
CHROMEDRIVER_PATH = '/opt/homebrew/bin/chromedriver'
PROFILE_URL = 'http://localhost:5173/profile'
TOAST_CLASS = "Toastify__toast"

service = Service(executable_path=CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(3)  # Implicit wait

# Helper: Get toast message
def get_toast_message(timeout=10):
    try:
        toast = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CLASS_NAME, TOAST_CLASS))
        )
        return toast.text
    except Exception:
        return None


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

    # Adjust this check to match your actual toast text, ignoring case
    if toast and "user logged in successfully" in toast.lower():
        print("✅ Login successful.")
        return True
    else:
        print(f"❌ Login failed. Toast: {toast}")
        return False

# Core: Cancel booking by ticket id and check toast
def cancel_booking(ticket_id, expect_success=True):
    try:
        time.sleep(1)
     

        driver.get(PROFILE_URL)
        time.sleep(2)

        # Try to find and click ticket link
        try:
            ticket_link = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, f'a[href="/ticket/{ticket_id}"].text-blue-500.underline')
                )
            )
            time.sleep(1)
            ticket_link.click()
            time.sleep(2)
        except Exception as e:
            if expect_success:
                print(f"❌ Ticket link not found for expected ticket: {ticket_id}")
                return False
            else:
                print(f"✅ Ticket link not found for  ticket '{ticket_id}' – Test passed.")
                return True

        # Click Cancel Booking
        cancel_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(),'Cancel Booking')]")
            )
        )
        time.sleep(1)
        cancel_btn.click()
        time.sleep(1)

        # Handle alert
        try:
            alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
            print(f"⚠️ Alert text: {alert.text}")
            alert.accept()
            print("🆗 Alert accepted.")
        except:
            print("⚠️ No alert appeared.")

        time.sleep(2)
        toast_msg = get_toast_message()

        if toast_msg:
            print(f"🧾 Toast message for ticket {ticket_id}: {toast_msg}")
            return "Successfully cancelled" in toast_msg if expect_success else "Successfully cancelled" not in toast_msg
        else:
            print(f"⚠️ No toast message appeared for ticket {ticket_id}.")
            return not expect_success

    except Exception as e:
        print(f"❌ Exception while cancelling ticket {ticket_id}: {e}")
        return False


# Test cases with different ticket IDs
def run_cancellation_tests():
    if not login_if_not_logged_in():
        print("❌ Cannot proceed with cancellation without login.")
        return False
    test_cases = [
        ("jzmiPmnmmT", False),        # valid ticket, should succeed
        ("invalidTicket", False),    # invalid, should fail, expect_failure = True
        # ("anotherinvlaidTicketId", False),  # invalid again
    ]

    for tid, expect_success in test_cases:
        print(f"\n🔄 Testing cancellation for ticket ID: {tid}")
        result = cancel_booking(tid, expect_success=expect_success)
        if result:
            print(f"✅ Cancellation test PASSED for ticket {tid}")
        else:
            print(f"❌ Cancellation test FAILED for ticket {tid}")

# Main execution
try:
    run_cancellation_tests()
    print("\n🎉 All cancellation tests completed!")
finally:
    print("\n🔚 Closing browser...")
    driver.quit()
