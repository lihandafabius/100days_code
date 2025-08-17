from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# Initialize the driver
driver = webdriver.Chrome(options=chrome_options)

# try:
    # Navigate to the webpage
    # driver.get("https://www.amazon.com/dp/B075CYMYK6?ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6&th=1")

#     # Wait up to 10 seconds for the elements to be visible
#     wait = WebDriverWait(driver, 10)
#
#     # Use XPath as an alternative, looking for an element that contains the class name
#     price_dollar_xpath = '//span[contains(@class, "a-price-whole")]'
#     price_fraction_xpath = '//span[contains(@class, "a-price-fraction")]'
#
#     price_dollar = wait.until(EC.visibility_of_element_located((By.XPATH, price_dollar_xpath)))
#     price_fraction = wait.until(EC.visibility_of_element_located((By.XPATH, price_fraction_xpath)))
#
#     print(f"The price is {price_dollar.text}.{price_fraction.text}")
#
# except NoSuchElementException:
#     print("One of the elements could not be found.")
# except TimeoutException:
#     print("Timed out waiting for page to load.")
# finally:
#     # Close the driver
#     driver.quit()
driver.get("https://www.python.org/")
# search_bar = driver.find_element(By.NAME, value="q")
# print(search_bar.tag_name)
# print(search_bar.get_attribute("placeholder"))
# button = driver.find_element(By.ID, value="submit")
# print(button.size)
#
# doc_link = driver.find_element(By.CSS_SELECTOR, value=".documentation-widget a")
# print(doc_link.text)
# bug_link = driver.find_element(By.XPATH, value='//*[@id="site-map"]/div[2]/div/ul/li[3]/a')
# print(bug_link.text)

