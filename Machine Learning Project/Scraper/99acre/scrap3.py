import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import numpy as np
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Firefox()

url = "https://www.99acres.com/search/property/buy/mumbai?city=12&keyword=mumbai&preference=S&area_unit=1&res_com=R"
driver.delete_all_cookies()
driver.get(url)
time.sleep(5)

data = []

def click_next_page():
    try:
        # Use XPath to locate the Next Page button more robustly
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Next Page')]"))
        )
        next_button.click()
        time.sleep(3)  # Allow time for the next page to load
        return True
    except Exception as e:
        print(f"Error clicking next page: {e}")
        return False
# Add this after your current click_next_page function
def wait_for_page_to_load():
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "r_srp__rightSection"))  # Ensure the main container is loaded
    )


with open('mumbai.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Write the header
    writer.writerow(['project_name', 'subheading', 'builder', 'apartment_type', 'price_range', 'bathroom_info','carpet_area'])

    # Loop through the pages
    for v in range(1, 3):  # Change this range for more pages
        print(f"Page number: {v}")
        time.sleep(3)  # Allow some time for the page to load fully

        # Get the updated list of sections for the current page
        try:
            outer_div = driver.find_element(By.CLASS_NAME, "pageComponent")
            sections = outer_div.find_elements(By.TAG_NAME, "section")
        except Exception as e:
            print(f"Error finding sections: {e}")
            break

        for i, section in enumerate(sections, start=1):
            try:
                # Extract project name
                try:
                    project_name = section.find_element(By.CLASS_NAME, 'PseudoTupleRevamp__heading').text
                except:
                    project_name = np.nan

                # Extract subheading
                try:
                    subheading = section.find_element(By.TAG_NAME, 'h2').text.strip()
                except:
                    subheading = np.nan

                # Extract builder name
                try:
                    builder = section.find_element(By.CLASS_NAME, 'PseudoTupleRevamp__contactSubheading').text
                except:
                    builder = np.nan

                # Extract carpet area
                try:
                    carpet_area = section.find_element(By.CLASS_NAME, 'CarpetArea__data').text
                except:
                    carpet_area = np.nan

                # Extract apartment types and prices
                config_cards = section.find_elements(By.CLASS_NAME, 'configs__configCard')
                for card in config_cards:
                    try:
                        apartment_type = card.find_element(By.CLASS_NAME, 'configs__ccl1').text
                        price_range = card.find_element(By.CLASS_NAME, 'configs__ccl2').text
                    except:
                        apartment_type = np.nan
                        price_range = np.nan

                # Extract bathroom information
                try:
                    bathroom_info = card.find_element(By.CLASS_NAME, 'configs__bathroom').text
                except:
                    bathroom_info = np.nan

                    # Write row to the CSV file
                writer.writerow([project_name, subheading, builder, apartment_type, price_range, bathroom_info,carpet_area])

                print(f"Extracted data for property {i}: {project_name}")

            except Exception as e:
                print(f"Error while extracting property data: {e}")

        # Try to go to the next page
        if not click_next_page():
            print("No more pages to load or error in pagination.")
            break
        wait_for_page_to_load()
        
        
# Close the browser
driver.quit()
