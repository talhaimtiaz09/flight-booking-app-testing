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
    # Step 1: Open homepage
    print("🔗 Opening homepage...")
    driver.get("http://localhost:5173/")
    time.sleep(1)

    # Step 2: Click 'Search Flights' link
    print("🔎 Navigating to Search Flights page...")
    search_link = driver.find_element(By.CSS_SELECTOR, 'a[href="/search"].hover\\:text-gray-500')
    search_link.click()
    time.sleep(1)

    # Step 3: Verify 'Search Flights' button exists
    print("✅ Verifying Search Flights button...")
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "search-button"))
    )
    print("🆗 Search button found.")

    # Step 4: Navigate to Flight Management Dashboard
    print("📊 Navigating to Dashboard...")
    dashboard_link = driver.find_element(By.CSS_SELECTOR, 'a[href="/flight-management"].hover\\:text-gray-500')
    dashboard_link.click()
    time.sleep(1)

    # Step 5: Verify dashboard heading
    print("✅ Verifying dashboard heading...")
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.XPATH, "//h1[contains(text(),'Flight Management Dashboard')]")
        )
    )
    print("🆗 Dashboard header found.")

    # Step 6: Navigate to Contact Us
    print("📨 Navigating to Contact Us...")
    contact_link = driver.find_element(By.CSS_SELECTOR, 'a[href="/contact"].hover\\:text-gray-500')
    contact_link.click()
    time.sleep(1)

    # Step 7: Verify 'Follow Us' heading
    print("✅ Verifying 'Follow Us' section...")
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.XPATH, "//h3[contains(text(),'Follow Us')]")
        )
    )
    print("🆗 'Follow Us' section found.")

    print("\n🎉 All UI steps executed successfully!")

except Exception as e:
    print(f"\n🚨 Test failed: {e}")
finally:
    print("🔚 Closing browser...")
    driver.quit()
