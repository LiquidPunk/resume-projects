import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Data scrapped from "https://philkotse.com/used-cars-for-sale"

def click_load_more_button(driver):
    try:
        # Wait for the "Load More" button to be clickable
        see_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'btnloadmore'))
        )
        see_more_button.click()
    except Exception as e:
        print(f"Error finding 'Load More' button: {e}")

def extract_car_info(soup):
    car_name_element = soup.find('h3', class_='title')
    car_name = car_name_element.find('a').text.strip() if car_name_element else "N/A"

    ul_tag = soup.find('ul', class_='tag')
    year = transmission = mileage = "N/A"
    if ul_tag:
        year_element = ul_tag.find('li', string=lambda text: text and text.isdigit())
        year = year_element.text.strip() if year_element else "N/A"

        transmission_element = ul_tag.find('li', {'data-tag': 'transmission'})
        transmission = transmission_element['title'] if transmission_element else "N/A"

        mileage_element = ul_tag.find('li', {'data-tag': 'numOfKm'})
        mileage = mileage_element['title'] if mileage_element else "N/A"

    price_element = soup.find('div', class_='price')
    price = price_element.text.strip() if price_element else "N/A"

    return [car_name, year, transmission, mileage, price]

# Setting up the webdriver
driver = webdriver.Chrome()

# Providing url to scrape
driver.get("https://philkotse.com/used-cars-for-sale")

# Wait for the initial content to load
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'col-4')))

# Opening a csv to write the data in
with open('car_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)

    # Write header row
    csv_writer.writerow(['Car Name', 'Year', 'Transmission', 'Mileage', 'Price'])

    while True:
        # Parse the current page content
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extract and process data you need from the current page
        car_elements = soup.find_all('div', class_='col-4')

        for car in car_elements:
            car_data = extract_car_info(car)
            csv_writer.writerow(car_data)

        # Check if the "Load More" button is present
        load_more_button_present = driver.find_elements(By.ID, 'btnloadmore')

        if not load_more_button_present:
            print("load more button not present.")
            break

        click_load_more_button(driver)

        # Wait for the next set of results to load
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'col-4')))

# After scraping, close the webdriver
driver.quit()
