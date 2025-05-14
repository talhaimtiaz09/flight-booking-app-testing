from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Using Service to specify the path to chromedriver
service = Service(executable_path='/opt/homebrew/bin/chromedriver')  # or ChromeDriverManager().install() for auto-management

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(service=service)

# Set implicit wait (this will make Selenium wait for elements to load)
driver.implicitly_wait(5)  # Waits up to 5 seconds for elements to appear

# Define valid and invalid test cases
valid_credentials = {
    "email": "test@test.com",
    "password": "Test@123"
}

invalid_credentials = [
    {"email": "", "password": ""},  # Empty fields
    # {"email": "invalidemail", "password": "password123"},  # Invalid email
    # {"email": "testuser@example.com", "password": ""},  # Missing password
    # {"email": "testuser@example.com", "password": "wrongpassword"}  # Invalid password
]

# Define a function to check for toast messages
def get_toast_message():
    try:
        # Wait for the toast element to appear (adjust the selector as needed)
        toast_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "Toastify__toast"))
        )
        # Return the text of the toast message
        return toast_element.text
    except Exception as e:
        print("No toast message found:", e)
        return None

def perform_login(credentials):
    try:
        # Open login page
        # print("\n" + "#" * 50)  # Divider
        # print("Navigating to the login page...")
        driver.get('http://localhost:5173/login')

        # Wait for the login form elements to be visible
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )

        # Fill the form
        print(f"\n{'=' * 50}")
        print(f"Filling form\n email: {credentials['email']}\npassword: {credentials['password']}")
        email_input = driver.find_element(By.ID, "email")
        password_input = driver.find_element(By.ID, "password")

        email_input.clear()
        password_input.clear()

        email_input.send_keys(credentials["email"])
        password_input.send_keys(credentials["password"])

        # Submit the form by pressing Enter (can also click the login button)
        password_input.send_keys(Keys.RETURN)

        # Wait for the toast message to appear
        time.sleep(2)  # Adjust the sleep time to give the toast enough time to appear

        # Check if the toast message appears
        toast_message = get_toast_message()
        if toast_message:
            # print(f"{'-' * 50}")
            print(f"Ui message: {toast_message}")
            # Check for successful login message
            if "User logged in successfully" in toast_message:
                print("Login was successful!")
                return True  # Success
            else:
                print("Login failed or unexpected message.")
                return False  # Failure
        else:
            print("No toast message found.")
            return False  # Failure

    except Exception as e:
        print(f"An error occurred during login: {e}")
        return False  # Failure

def test_valid_login():
    print("\n" + "=" * 50)
    print("Testing valid login...")
    success = perform_login(valid_credentials)
    assert success, "Valid login test failed"

def test_invalid_logins():
    for credentials in invalid_credentials:
        print("\n" + "=" * 50)
        print(f"Testing invalid login with email: {credentials['email']} and password: {credentials['password']}")
        success = perform_login(credentials)
        assert not success, f"Invalid login test failed for {credentials['email']}"

try:
    # Run tests
    test_valid_login()
    test_invalid_logins()

    # print("\n" + "#" * 50)
    print("All tests commpeleted!")
except AssertionError as e:
    print(f"\nTest failed: {e}")
finally:
    # Close the browser after the test
    time.sleep(1)
    print("\n" + "-" * 50)
    print("Closing the browser...")
    driver.quit()
