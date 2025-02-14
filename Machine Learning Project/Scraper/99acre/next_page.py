from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.action_chains import ActionChains

# Initialize the WebDriver
driver = webdriver.Firefox()  # Use the appropriate WebDriver
driver.delete_all_cookies()  # Clear any existing cookies
driver.get('https://www.99acres.com/search/property/buy/mumbai?city=12&keyword=mumbai&preference=S&area_unit=1&res_com=R')  # Navigate to the site

def scroll_to_bottom():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for new content to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def click_next_page():
    for attempt in range(3):  # Retry up to 3 times
        try:
            # Wait for the next page button to be visible
            next_button = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div/a[contains(text(), 'Next Page')]"))
            )

            print(f"Next button found: {next_button.is_displayed()}, {next_button.is_enabled()}")  # Debug log
            
            # Use ActionChains to move to the button and click it
            actions = ActionChains(driver)
            actions.move_to_element(next_button).click().perform()

            time.sleep(3)  # Allow time for the next page to load
            
            # Check if content is loaded by looking for a specific element
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "your_specific_content_selector"))  # Replace with a valid selector
            )
            print("Content loaded successfully on the next page.")
            return True  # Successful click
        except Exception as e:
            print(f"Attempt {attempt + 1}: Error clicking next page: {e}")
            time.sleep(2)  # Wait before retrying
            
    return False  # Failed to click after retries

# Scroll to the bottom of the page first
scroll_to_bottom()

# Example usage of the click_next_page function
while True:  # Loop to keep navigating until no more pages
    if not click_next_page():
        print("No more pages or unable to click the next page.")
        break  # Exit the loop if clicking fails
time.sleep(5)
# Clean up and close the browser
driver.quit()