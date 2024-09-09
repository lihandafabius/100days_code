# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time
#
# # Configure Chrome options
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_experimental_option("detach", True)
#
# # Initialize the Chrome WebDriver
# driver = webdriver.Chrome(options=chrome_options)
#
# # Navigate to the NutritionValue homepage
# driver.get("https://www.nutritionvalue.org/")
#
# # Login process
# login_button = driver.find_element(By.XPATH, '//*[@id="main"]/tbody/tr[1]/td/div[1]/a[9]')
# login_button.click()
# time.sleep(3)
#
# email = driver.find_element(By.XPATH, '//*[@id="email"]')
# email.send_keys("")
#
# password = driver.find_element(By.XPATH, '//*[@id="password"]')
# password.send_keys("")
#
# account_login = driver.find_element(By.XPATH, '//*[@id="create-account"]')
# account_login.click()
# time.sleep(3)
#
# # Scroll to the "A" button to ensure it's clickable
# a_letter_button = driver.find_element(By.XPATH, '//*[@id="main"]/tbody/tr[27]/td/div/div/a[1]')
# driver.execute_script("arguments[0].scrollIntoView();", a_letter_button)  # Scroll to the element
# time.sleep(2)  # Give the page time to scroll
#
# # Click the "A" letter button
# a_letter_button.click()
#
# # Continue with scraping the food items...
#
# # Initialize an empty list to store food names
# foods_list = []
#
# # Scrape the food names under the 'A' section
# food_elements = driver.find_elements(By.XPATH, '//div[@class="list-group"]/a')
#
# for food in food_elements:
#     food_name = food.text.strip()
#     food_url = food.get_attribute("href")
#     foods_list.append([food_name, food_url])
#
# # Save the data to a CSV file
# csv_file = 'foods_A.csv'
# with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)
#     writer.writerow(["Food Name", "URL"])  # Write the header
#     writer.writerows(foods_list)  # Write the food names and URLs
#
# print(f"Scraped {len(foods_list)} foods starting with 'A' and saved to {csv_file}")
#
# # Quit the WebDriver
# driver.quit()


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import csv

# Path to your ChromeDriver
# Configure Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(options=chrome_options)


# Navigate to Audible Best Sellers
driver.get("https://www.audible.com/search?keywords=bestsellers")

# Wait for page load
time.sleep(3)

# Scrape book details
book_elements = driver.find_elements(By.CSS_SELECTOR, 'li.bc-list-item')

# Open CSV file to write results
with open('audible_books_selenium.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Title', 'Subtitle', 'Author', 'Length', 'Release Date', 'Language'])

    for book in book_elements:
        try:
            title = book.find_element(By.CSS_SELECTOR, 'a.bc-link.bc-color-link').text
            subtitle = book.find_element(By.CSS_SELECTOR, 'li.subtitle').text if book.find_elements(By.CSS_SELECTOR,
                                                                                                    'li.subtitle') else 'N/A'
            author = book.find_element(By.CSS_SELECTOR, 'li.authorLabel').text.replace('By:',
                                                                                       '').strip() if book.find_elements(
                By.CSS_SELECTOR, 'li.authorLabel') else 'N/A'
            length = book.find_element(By.CSS_SELECTOR, 'li.runtimeLabel').text.replace('Length:',
                                                                                        '').strip() if book.find_elements(
                By.CSS_SELECTOR, 'li.runtimeLabel') else 'N/A'
            release_date = book.find_element(By.CSS_SELECTOR, 'li.releaseDateLabel').text.replace('Release date:',
                                                                                                  '').strip() if book.find_elements(
                By.CSS_SELECTOR, 'li.releaseDateLabel') else 'N/A'
            language = book.find_element(By.CSS_SELECTOR, 'li.languageLabel').text.replace('Language:',
                                                                                           '').strip() if book.find_elements(
                By.CSS_SELECTOR, 'li.languageLabel') else 'N/A'

            csvwriter.writerow([title, subtitle, author, length, release_date, language])
        except Exception as e:
            print(f"Error scraping data: {e}")

print("Scraping completed!")

