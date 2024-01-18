import requests
from bs4 import BeautifulSoup
import csv

# This code scrapes the newer format of the site

def scrape_page(url, writer):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Check if the element is found
    car_elements = soup.select('div.col.span_7.positionrelative.padtop')

    for car in car_elements:
        car_title = car.select_one('a.darklink h3').text.strip()

        # Check for the presence of hot-deal-price class
        hot_deal_price_element = car.select_one('span.hot-deal-price')
        car_price = hot_deal_price_element.text.strip() if hot_deal_price_element else 'N/A'

        # If hot-deal-price is not present, check for the regular price format
        if car_price == 'N/A':
            regular_price_element = car.select_one('h4.nomargin.padbottom.padtop')
            car_price = regular_price_element.text.strip() if regular_price_element else 'N/A'

        car_mileage_element = car.select_one('span.padright30.small.reducedopacity')
        car_mileage = car_mileage_element.text.strip() if car_mileage_element else 'N/A'

        car_transmission_elements = car.select('div.padbottom20 span.small.reducedopacity')
        car_transmission = car_transmission_elements[1].text.strip() if len(car_transmission_elements) > 1 else 'N/A'

        car_fuel_type_elements = car.select('div.padbottom20 span.small.reducedopacity')
        car_fuel_type = car_fuel_type_elements[2].text.strip() if len(car_fuel_type_elements) > 2 else 'N/A'

        seller_name_element = car.select_one('div.vcard span.fn.bold.small.dealerbadge')
        seller_name = seller_name_element.text.strip() if seller_name_element else 'N/A'

        seller_location_element = car.select_one('div.vcard div.adr span.locality small')
        seller_location = seller_location_element.text.strip() if seller_location_element else 'N/A'

        # Write the data to a CSV file
        writer.writerow({'Car Title': car_title,
                         'Car Price': car_price,
                         'Car Mileage': car_mileage,
                         'Car Transmission': car_transmission,
                         'Car Fuel Type': car_fuel_type,
                         'Seller Name': seller_name,
                         'Seller Location': seller_location})


# Opening a csv to write the data in
with open('scraped_data2.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Car Title', 'Car Price', 'Car Mileage', 'Car Transmission', 'Car Fuel Type', 'Seller Name', 'Seller Location']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Writes header for the csv file
    writer.writeheader()

    # Loop through multiple pages (adjust the range accordingly)
    for page_number in range(1, 56):  # Assuming there are 5 pages
        current_url = f"https://www.autodeal.com.ph/used-cars/search/certified-pre-owned+repossessed+used-car-status/page-{page_number}?sort-by=relevance"

        # Call the function to scrape data from the current page
        scrape_page(current_url, writer)