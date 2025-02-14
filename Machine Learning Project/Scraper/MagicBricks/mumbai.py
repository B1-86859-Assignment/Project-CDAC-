from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv


# Initialize the driver
driver = webdriver.Firefox()

# URL of MagicBricks property page
url = "https://www.magicbricks.com/property-for-sale/residential-real-estate?bedroom=1,2,3,4,5,%3E5&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&cityName=Mumbai"

# Open the website
driver.get(url)
time.sleep(5)  # Wait for the initial page to load

# Scroll down the page multiple times to load more content
scroll_pause_time = 10  # Adjust this time to let the content load
last_height = driver.execute_script("return document.body.scrollHeight")

print("Starting to scroll and load more properties...")

while True:
    # Scroll down to the bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # Wait to load the page
    time.sleep(scroll_pause_time)
    
    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    print(f"Scrolled down to new height: {new_height}")
    if new_height == last_height:
        print("No more new content loaded. Ending scroll.")
        break  # Break the loop if no more content is loaded
    last_height = new_height

# After scrolling, extract property listings
properties = driver.find_elements(By.CLASS_NAME, 'mb-srp__card')

# Open a CSV file for writing
with open('mumbai 1.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Write the header
    writer.writerow(['Title', 'Carpet Area', 'Status', 'Floor', 'Price', 'Bathrooms', 'Transaction', 'Furnishing'])

    print("Extracting property data...")

    # Loop through each property and extract the necessary details
    for prop in properties:
        try:
            # Extract the title (property name)
            title = prop.find_element(By.CLASS_NAME, 'mb-srp__card--title').text
            
            # Use WebDriverWait to check for each element
            
            
            
            wait = WebDriverWait(driver, 0.2)
            
            
            
            

            # Extract the carpet area if available
            try:
                carpet_area = wait.until(EC.presence_of_element_located(
                    (By.XPATH, ".//div[@data-summary='carpet-area']//div[@class='mb-srp__card__summary--value']")
                )).text
            except:
                carpet_area = 'N/A'

            # Extract the status
            try:
                status = wait.until(EC.presence_of_element_located(
                    (By.XPATH, ".//div[@data-summary='status']//div[@class='mb-srp__card__summary--value']")
                )).text
            except:
                status = 'N/A'

            # Extract the floor information
            try:
                floor = wait.until(EC.presence_of_element_located(
                    (By.XPATH, ".//div[@data-summary='floor']//div[@class='mb-srp__card__summary--value']")
                )).text
            except:
                floor = 'N/A'

            # Extract the price
            price = prop.find_element(By.CLASS_NAME, 'mb-srp__card__price--amount').text
            
            # Extract the number of bathrooms
            try:
                bathrooms = wait.until(EC.presence_of_element_located(
                    (By.XPATH, ".//div[@data-summary='bathroom']//div[@class='mb-srp__card__summary--value']")
                )).text
            except:
                bathrooms = 'N/A'

            # Extract the transaction type (e.g., resale)
            try:
                transaction = wait.until(EC.presence_of_element_located(
                    (By.XPATH, ".//div[@data-summary='transaction']//div[@class='mb-srp__card__summary--value']")
                )).text
            except:
                transaction = 'N/A'
                
            # Extract furnishing status
            try:
                furnishing = wait.until(EC.presence_of_element_located(
                    (By.XPATH, ".//div[@data-summary='furnishing']//div[@class='mb-srp__card__summary--value']")
                )).text
            except:
                furnishing = 'N/A'
            
            # Write the data to the CSV file
            writer.writerow([title, carpet_area, status, floor, price, bathrooms, transaction, furnishing])
            print(f"Extracted data for property: {title}")
    
        except Exception as e:
            print(f"Error while extracting property data: {e}")

# Close the browser after scraping
driver.quit()

print("Data saved to properties.csv")
