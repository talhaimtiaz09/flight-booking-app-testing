# tests/test_flight_search.py
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

flight_search_cases = [
    pytest.param(
        {"from": "Dubai", "to": "London", "departDate": "15-06-2025"},
        True,
        id="valid_search_dubai_to_london"
    ),
    pytest.param(
        {"from": "", "to": "London", "departDate": "15-06-2025"},
        False,
        id="missing_from_city"
    ),
    pytest.param(
        {"from": "Dubai", "to": "", "departDate": "15-06-2025"},
        False,
        id="missing_to_city"
    ),
    pytest.param(
        {"from": "New York", "to": "Tokyo", "departDate": "01-01-2000"},
        False,
        id="past_date"
    ),
    pytest.param(
        {"from": "Dubai", "to": "London", "departDate": "invalid-date"},
        False,
        id="invalid_date_format"
    ),
]

def get_toast_message(driver):
    try:
        toast = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "Toastify__toast"))
        )
        return toast.text.strip().lower()
    except:
        return None

def perform_flight_search(driver, data):
    driver.get("http://localhost:5173/search")
    time.sleep(1)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "from")))

    from_input = driver.find_element(By.NAME, "from")
    to_input = driver.find_element(By.NAME, "to")
    date_input = driver.find_element(By.NAME, "departDate")

    from_input.clear()
    from_input.send_keys(data["from"])
    to_input.clear()
    to_input.send_keys(data["to"])
    date_input.clear()
    date_input.send_keys(data["departDate"])

    driver.find_element(By.ID, "search-button").click()
    time.sleep(2)

    return get_toast_message(driver)

# ✅ Parametrized test
@pytest.mark.parametrize("case, expected_success", flight_search_cases)
def test_flight_search(driver, case, expected_success):
    toast = perform_flight_search(driver, case)
    actual_success = toast and "fetched successfull" in toast

    assert actual_success == expected_success, f"❌ Case failed: {case} | Toast: {toast}"
