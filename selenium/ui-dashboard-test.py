from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup WebDriver
CHROMEDRIVER_PATH = '/opt/homebrew/bin/chromedriver'
service = Service(executable_path=CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(5)

try:
    # Step 1: Open Flight Management page
    print("🔗 Opening Flight Management page...")
    driver.get("http://localhost:5173/flight-management")
    time.sleep(1)

    # Step 2: Click 'Search Flights' button
    print("🔍 Clicking 'Search Flights' button...")
    search_button = driver.find_element(By.XPATH, "//button[text()='Search Flights']")
    search_button.click()
    time.sleep(1)

    # Step 3: Verify 'All Flights' heading
    print("✅ Verifying 'All Flights' heading...")
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.XPATH, "//h2[text()='All Flights']")
        )
    )
    print("🆗 'All Flights' found.")

    # Step 4: Click 'Add Airline' button
    print("➕ Clicking 'Add Airline' button...")
    add_airline_button = driver.find_element(By.XPATH, "//button[text()='Add Airline']")
    add_airline_button.click()
    time.sleep(1)

    # Step 5: Verify 'Add Airline' submit button
    print("✅ Verifying 'Add Airline' form submit button...")
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.XPATH, "//button[@type='submit' and contains(text(),'Add Airline')]")
        )
    )
    print("🆗 'Add Airline' submit button found.")

    # Step 6: Click 'Add Flight' button
    print("✈️ Clicking 'Add Flight' button...")
    add_flight_button = driver.find_element(By.XPATH, "//button[text()='Add Flight']")
    add_flight_button.click()
    time.sleep(1)

    # Step 7: Verify 'Add Flight' submit button
    print("✅ Verifying 'Add Flight' form submit button...")
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.XPATH, "//button[@type='submit' and contains(text(),'Add Flight')]")
        )
    )
    print("🆗 'Add Flight' submit button found.")

    print("\n🎉 All UI tests passed successfully!")

except Exception as e:
    print(f"\n🚨 Test failed: {e}")
finally:
    print("🔚 Closing browser...")
    driver.quit()
