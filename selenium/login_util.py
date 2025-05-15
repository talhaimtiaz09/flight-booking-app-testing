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


def get_toast_message():
    try:
        toast = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "Toastify__toast"))
        )
        return toast.text.strip().lower()
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

    if toast and "user logged in successfully" in toast:
        print("✅ Login successful.")
        return True
    else:
        print(f"❌ Login failed. Toast: {toast}")
        return False
