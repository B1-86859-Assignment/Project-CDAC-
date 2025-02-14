import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import numpy as np
from selenium.common.exceptions import NoSuchElementException


driver = webdriver.Firefox()
url = "https://www.99acres.com/search/property/buy/mumbai?city=12&keyword=mumbai&preference=S&area_unit=1&res_com=R"

driver.get(url)
time.sleep(5)

data = []

outer_div = driver.find_element(By.CLASS_NAME , "pageComponent")
sections = outer_div.find_elements(By.TAG_NAME ,"section")


def click_next_page():
    try:
        next_button = driver.find_element(By.LINK_TEXT, 'Next Page >')
        next_button.click()
        return True
    except NoSuchElementException:
        return False


for v in range(1,3):
    with open('mumbai.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write the header
        writer.writerow(['project_name', 'subheading', 'builder', 'apartment_type', 'price_range', 'bathroom_info','carpet_area'])
        
        print(f"Page number :{v}")
        i = 1

        for section in sections:
            
            
            try:
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
                        apartment_type=np.nan
                        price_range = np.nan

                # Extract bathroom information - adjust the class name if needed
                try:
                    bathroom_info = card.find_element(By.CLASS_NAME, 'configs__bathroom').text
                except:
                    bathroom_info= np.nan
                
                
                    
                    
                writer.writerow([project_name, subheading, builder, apartment_type, price_range, bathroom_info,carpet_area])
            
                print(f"Extracted data for property {i} : {project_name}")
                i+=1
        
            except Exception as e:
                print(f"Error while extracting property data: {e}")
            
            try:
                click_next_page()
                time.sleep(3)
            except:
                print("No more pages to load ")
            

time.sleep(2)
driver.quit()