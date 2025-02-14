from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

# Initialize the driver
driver = webdriver.Firefox()

# URL of MagicBricks property page
url = "https://www.magicbricks.com/property-for-sale/residential-real-estate?bedroom=1,2,3,4,5,%3E5&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&cityName=Pune"

# Open the website
driver.get(url)
time.sleep(5)  # Wait for the initial page to load

# Scroll down the page multiple times to load more content
scroll_pause_time = 8  # Shorten this time for faster scrolling
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
with open('pune_properties.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Write the header
    writer.writerow(['Title', 'Carpet Area', 'Status', 'Floor', 'Price', 'Bathrooms', 'Transaction', 'Furnishing'])

    print("Extracting property data...")

    # Loop through each property and extract the necessary details
    for prop in properties:
        try:
            # Extract the title (property name)
            title = prop.find_element(By.CLASS_NAME, 'mb-srp__card--title').text

            # Find carpet area, status, floor, etc., using find_elements for faster extraction
            carpet_area = prop.find_elements(By.XPATH,
                                             ".//div[@data-summary='carpet-area']//div[@class='mb-srp__card__summary--value']")
            carpet_area = carpet_area[0].text if carpet_area else 'N/A'

            status = prop.find_elements(By.XPATH,
                                        ".//div[@data-summary='status']//div[@class='mb-srp__card__summary--value']")
            status = status[0].text if status else 'N/A'

            floor = prop.find_elements(By.XPATH,
                                       ".//div[@data-summary='floor']//div[@class='mb-srp__card__summary--value']")
            floor = floor[0].text if floor else 'N/A'

            price = prop.find_element(By.CLASS_NAME, 'mb-srp__card__price--amount').text

            bathrooms = prop.find_elements(By.XPATH,
                                           ".//div[@data-summary='bathroom']//div[@class='mb-srp__card__summary--value']")
            bathrooms = bathrooms[0].text if bathrooms else 'N/A'

            transaction = prop.find_elements(By.XPATH,
                                             ".//div[@data-summary='transaction']//div[@class='mb-srp__card__summary--value']")
            transaction = transaction[0].text if transaction else 'N/A'

            furnishing = prop.find_elements(By.XPATH,
                                            ".//div[@data-summary='furnishing']//div[@class='mb-srp__card__summary--value']")
            furnishing = furnishing[0].text if furnishing else 'N/A'

            # Write the data to the CSV file
            writer.writerow([title, carpet_area, status, floor, price, bathrooms, transaction, furnishing])
            print(f"Extracted data for property: {title}")

        except Exception as e:
            print(f"Error while extracting property data: {e}")

# Close the browser after scraping
driver.quit()

print("Data saved to pune_properties.csv")
