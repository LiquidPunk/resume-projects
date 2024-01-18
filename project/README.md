# Used Car Price Prediction Through Machine Learning

#### Video Demo:  <https://youtu.be/leDrIC6BO-c>

## Prerequisites

Make sure you have Python installed on your system.

## Overview

This comprehensive machine learning project covers the entire process, excluding model deployment. The primary objective is to gather data on used cars in the Philippines, perform an in-depth analysis, and predict used car prices though machine learning models. Python scripts and ipynb files were used throughout this project to scrape data, clean and preprocessing, with additional fine-tuning through Microsoft Excel, And the exploratory data analysis (EDA) and Price prediction using machine learning models.
NOTE: Data scraping was run on PyCharm and the Cleaning, Preprocessing, EDA, and Price predictions were run on Google Colab —a hosted Jupyter Notebook service. It is important to note that the file EDA|XGBRegressor|used_cars_ph.ipynb is the only file specifically tested and adapted to run on Visual Studio Code with its corresponding csv, while the other files were simply imported from different IDEs. For optimal functionality, other files may need to be executed in their respective native environments. All Prices are in PHP Philippine Peso.
## Key Features
- **Data Scraping**: Automated data extraction from two major car sales websites in the Philippines.
- **Data Cleaning & Preprocessing**: Utilization of Python and Microsoft Excel for thorough and fine-tuned data preparation.
- **Data Analysis**: Exploration of the dataset through various statistical methods and visualizations.
- **Machine Learning**: Employing the XGBRegressor model for price prediction, chosen for its performance and accuracy compared to other tested models.

## Files Description

### Data_Scraping
1. `scrape_autodeal.py`
   - **Description**: This Python script is web scraping using the Beautiful Soup library. It extracts specific data from autodeal.com related to used cars. The scraped information includes 'car_title', 'car_price', 'car_mileage', 'car_transmission', 'car_fuel_type', 'seller_name', and 'seller_location.'
   - **Info**: Though most of these features will be omitted in the final dataset. This is also one of two scripts that were used to scape autodial.com, It was done this way due to varying elements in the HTML and it saves time during the Data cleaning and preprocessing part of the project.

   - **Usage**: Run on PyCharm or any other similar Python IDE
   - **Dependencies**: BeautifulSoup4

2. `scape_autodeal_2.py`
   - **Description**: An extension of `scrape_autodeal.py`, adapted to scrape a different/older layout from the same website.
   - **Usage**: Run on PyCharm or any other similar Python IDE
- **Dependencies**: BeautifulSoup4

3. `scape_philkotse.py`
   - **Description**: This is a more complex web scraping python script, though still similar to the previously mentioned scripts. Data collected from the script contains the features 'Car Name', 'Year', 'Transmission', 'Mileage', 'Price'. And uses packages Beautiful Soup, as well as Selenium and ChromeDriver.
- **Info**: I believed the amount of data from the previous scraping was lacking, so I needed to scrape a different website which was more troublesome due to the webpage utilizing a “load more” button instead of numbered pages.
NOTE: This script worked in collecting data required, BUT is inefficient in how it scrapes the data, as well as the implementation of an auto scroller to find the ‘Next Page’ button not working. Still need a lot of improvements.
   - **Usage**: Run on PyCharm or any other similar Python IDE
   - **Dependencies**: Selenium, BeautifulSoup4, ChromeDriver

### Data_Preprocessing
4. `DataCleaning_Preprocessing_autodeal.ipynb`
   - **Description**: A Jupyter notebook for cleaning and preprocessing of data scraped from autodeal.com. Includes handling of missing values, dropping duplicates, data normalization, feature engineering, and merging of the two autodeal datasets.
   - **Usage**: Run via Jupyter Notebook specifically created and ran in Google Colab.

5. `DataCleaning_Preprocessing_philkotse.ipynb`
   - **Description**: A Jupyter notebook for cleaning and preprocessing of data scraped from philkotse.com. Similar goal and includes the same ideas and functionalities as the autodeal notebook, though more complex/tedious due to scraping only one format of the site as well as the flaws of script used to scrape the data.
- **Info**: Uses functions to compare formats of the cleaned data.
   - **Usage**: Run via Jupyter Notebook specifically created and ran in Google Colab.

### Exploratory Data Analysis and Machine Learning
6. `EDA_XGBRegressor_used_cars_ph.ipynb`
   - **Description**: The highlight of this project. This jupyter notebook encompassing both exploratory data analysis (EDA) and the implementation of a machine learning model (XGBoost Regressor) in predicting used car prices. All Prices are in PHP Philippine Peso.
   - **Info**: In refining the data, I made a strategic decision to eliminate outliers in the 'Mileage' and 'Price' features based on graphical observations. Notably, I set upper bounds for outliers in each feature, rather than employing the Interquartile Range, as I noticed a concentration of outliers and less frequent cars in the higher price range. For 'Mileage,' I capped it at 150,000 after observing the graph, considering that cars with higher mileage might not be in optimal working condition. During model selection, I tested different models and found that both Random Forest and XGBRegressor performed well, with the latter being slightly more accuracy. To prepare features/columns for the machine learning model, I used label encoding for 'Car_Name' and used pandas' get_dummies for 'Car_Brand.' The choice of encoding methods were due simply to the model performing better when doing so.
NOTE: This model is tailored to more “affordable cars” and common car models. It may not perform well with luxury vehicles, uncommon car models, and or heavily modified cars etc..
   - **Usage**: Run via Jupyter Notebook specifically created and ran in Google Colab.

### Dataset
7. `used_car_data_ph.csv`
   - **Description**: The final, merged and cleaned dataset used in the exploratory data analysis and machine learning model part of the project. Contains the features “Car_Name”, “Car_Brand”, “Year”, “Transmission”, “Mileage”, and “Price”. Though the feature/column “Transmission” cannot be used reliably due to most sellers labeling cars as automatic transmission (AT) instead of continuously variable transmission (CVT). Data within this csv were collected from autodial.ph and philkotse.com with the scripts found in the DataScraping folder. All Prices are in PHP Philippine Peso.
   - **Usage**: Used in `EDA_XGBRegressor_used_cars_ph.ipynb`.

## Installing Dependencies

To run the provided code, you'll need to install the following Python packages.:

```bash
pip install requests
pip install beautifulsoup4
pip install selenium
pip install pandas
pip install matplotlib
pip install seaborn
pip install scikit-learn
pip install xgboost
