from selenium import webdriver
import os
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By


def scrape_logo(url):
    # Initialize Selenium webdriver (replace 'chromedriver' with the name of your web driver)
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)

    driver = webdriver.Chrome(options=options)

    driver.get(url)

    # Find the logo element
    logo_element = driver.find_element(By.CSS_SELECTOR, value=".sp-sticky-logo hidden-xs src")

    # # Extract the URL of the logo image
    # logo_url = logo_element.get_attribute('src')

    # Download the logo image
    download_logo(logo_element)

    # Close the webdriver
    driver.quit()


def download_logo(logo_url):
    # Create a directory to save the logo image
    os.makedirs('logos', exist_ok=True)
    # Get the filename from the URL
    filename = 'logo.png'
    # Download the logo image
    response = requests.get(logo_url)
    with open(os.path.join('logos', filename), 'wb') as f:
        f.write(response.content)
    print("Logo downloaded successfully.")


# Example usage
url = 'https://www.egerton.ac.ke/'
scrape_logo(url)
