from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

page = 2087


# Set up Firefox options to run in headless mode
firefox_options = Options()
firefox_options.add_argument('--headless')  # Run in headless mode

# Set up the Firefox driver with headless options
driver = webdriver.Firefox(options=firefox_options)

# URL of the website
url = f"https://www.makaan.com/pune-residential-property/buy-property-in-pune-city?beds=1rk,1,2,3,3plus&propertyType=apartment,builder-floor,villa,residential-plot,independent-house&page={page}"

# Navigate to the website
driver.get(url)

# Wait for the page to load
WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'infoWrap')))

# Create a CSV file and write the header row
with open('makaan_data.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Property Name', 'Project Name', 'Location', 'City', 'Price', 'Area (sqft)', 'Construction Status',
                     'Possession Date','bathrooms', 'Developer'])


# Function to extract data from a single page
def extract_data(page_number):
    time.sleep(2)  # Wait for the page to load properly
    properties = driver.find_elements(By.CLASS_NAME, 'infoWrap')
    data = []

    print(f"Scraping page {page_number}: {len(properties)} properties found")

    for index, property in enumerate(properties):
        try:
            time.sleep(1)  # Adding a delay between each property extraction

            # Property Name (e.g., 2 BHK Apartment)
            property_name = property.find_element(By.TAG_NAME, 'strong').text.strip()

            # Project Name (e.g., Basil Vrundavan Wing E)
            project_name = property.find_element(By.XPATH, "//strong/a[@class='projName']").text.strip()

            # Location (e.g., Ambegaon Budruk)
            try:
                location = property.find_element(By.CLASS_NAME, 'locName').text.strip()
            except:
                location = "Not Available"

            # City (e.g., Pune)
            try:
                city = property.find_element(By.CLASS_NAME, 'cityName').text.strip()
            except:
                city = "Not Available"

            # Price (e.g., 82 L)
            price = property.find_element(By.CLASS_NAME, 'price').text.strip()

            # Area in sqft (e.g., 755 sqft)
            area = property.find_element(By.CLASS_NAME, 'size').text.strip()

            # Construction Status (e.g., Under Construction)
            try:
                construction_status = property.find_element(By.CLASS_NAME, 'val').text.strip()
            except:
                construction_status = "Not Available"

            # Possession Date (e.g., Possession by Apr 2028)
            try:
                possession_date = property.find_element(By.XPATH, '//ul/li[@title="old"]').text.strip()
            except:
                possession_date = "Not Available"

            try:
                bathrooms = property.find_element(By.XPATH, '//ul/li[@title="Bathrooms"]').text.strip()
            except:
                bathrooms = "Not Available"

            # Developer (e.g., Basil Avante)
            try:
                developer = property.find_element(By.CLASS_NAME, 'seo-hdng').text.strip()
            except:
                developer = "Not Available"

            # Append the data
            data.append([property_name, project_name, location, city, price, area, construction_status, possession_date,bathrooms,
                         developer])

            # Log the progress of each property scraped
            print(f"Property {index + 1}/{len(properties)} on page {page_number} scraped")

        except Exception as e:
            print(f"Error while scraping property data on page {page_number}: {e}")
            continue

    return data


# Function to check if next page exists
def has_next_page():
    try:
        next_page_element = driver.find_element(By.CLASS_NAME, 'icon-chevron-right')
        return next_page_element.is_enabled()
    except:
        return False


# Extract data from all pages and write to CSV file

for _ in range(2118):
    while True:
        url = f"https://www.makaan.com/pune-residential-property/buy-property-in-pune-city?beds=1rk,1,2,3,3plus&propertyType=apartment,builder-floor,villa,residential-plot,independent-house&page={page}"
        driver.get(url)

        # Adding a delay to ensure page elements have loaded fully
        time.sleep(3)

        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'infoWrap')))

        with open('makaan_data.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            data = extract_data(page)
            for row in data:
                writer.writerow(row)

        time.sleep(2)  # Wait before moving to the next page
        if not has_next_page():
            print(f"No more pages to scrape after page {page}.")
            break
        page += 1
        print(f"Moving to page {page}...")

# Close the browser
driver.quit()
