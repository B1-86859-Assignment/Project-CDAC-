from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time
import csv


# Initialize the driver
driver = webdriver.Firefox()

# URL of MagicBricks property page
url = "https://www.magicbricks.com/property-for-sale/residential-real-estate?bedroom=1,2,3,4,5,%3E5&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&cityName=Kolkata"

# Open the website
driver.get(url)
time.sleep(5)  # Wait for the initial page to load

# Scroll down the page multiple times to load all content
scroll_pause_time = 10
last_height = driver.execute_script("return document.body.scrollHeight")

print("Starting to scroll and load all properties...")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)
    new_height = driver.execute_script("return document.body.scrollHeight")
    print(f"Scrolled to new height: {new_height}")
    if new_height == last_height:
        print("No more content loaded. Ending scroll.")
        break
    last_height = new_height

# After scrolling, extract all property listings
properties = driver.find_elements(By.CLASS_NAME, 'mb-srp__card')

# Open a CSV file for writing
with open('kolkata.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Write the header
    writer.writerow(['Title', 'Carpet Area', 'Status', 'Floor', 'Price', 'Bathrooms', 'Transaction', 'Furnishing'])

    print("Extracting property data without WebDriverWait...")

    # Loop through each property and extract the necessary details
    for prop in properties:
        try:
            # Extract the title (property name)
            title = prop.find_element(By.CLASS_NAME, 'mb-srp__card--title').text

            # Extract the carpet area if available
            try:
                carpet_area = prop.find_element(By.XPATH, ".//div[@data-summary='carpet-area']//div[@class='mb-srp__card__summary--value']").text
            except:
                carpet_area = 'N/A'

            # Extract the status
            try:
                status = prop.find_element(By.XPATH, ".//div[@data-summary='status']//div[@class='mb-srp__card__summary--value']").text
            except:
                status = 'N/A'

            # Extract the floor information
            try:
                floor = prop.find_element(By.XPATH, ".//div[@data-summary='floor']//div[@class='mb-srp__card__summary--value']").text
            except:
                floor = 'N/A'

            # Extract the price
            try:
                price = prop.find_element(By.CLASS_NAME, 'mb-srp__card__price--amount').text
            except:
                price = 'N/A'
            
            # Extract the number of bathrooms
            try:
                bathrooms = prop.find_element(By.XPATH, ".//div[@data-summary='bathroom']//div[@class='mb-srp__card__summary--value']").text
            except:
                bathrooms = 'N/A'

            # Extract the transaction type (e.g., resale)
            try:
                transaction = prop.find_element(By.XPATH, ".//div[@data-summary='transaction']//div[@class='mb-srp__card__summary--value']").text
            except:
                transaction = 'N/A'
                
            # Extract furnishing status
            try:
                furnishing = prop.find_element(By.XPATH, ".//div[@data-summary='furnishing']//div[@class='mb-srp__card__summary--value']").text
            except:
                furnishing = 'N/A'
            
            # Write the data to the CSV file
            writer.writerow([title, carpet_area, status, floor, price, bathrooms, transaction, furnishing])
            print(f"Extracted data for property: {title}")
    
        except Exception as e:
            print(f"Error while extracting property data: {e}")

# Close the browser after scraping
driver.quit()

print("Data saved to kolkata.csv")
