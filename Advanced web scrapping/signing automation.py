from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# Initialize the driver
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://secure-retreat-92358.herokuapp.com/")

first_name = driver.find_element(By.NAME, value="fName")
first_name.send_keys("fname", Keys.ENTER)
last_name = driver.find_element(By.NAME, value="lName")
last_name.send_keys("lname", Keys.ENTER)
email = driver.find_element(By.NAME, value="email")
email.send_keys("enter_email_value", Keys.ENTER)

# signup_button = driver.find_element(By.CLASS_NAME, value="btn btn-lg btn-primary btn-block")
# signup_button.send_keys(Keys.ENTER)

signup_button = driver.find_element(By.CSS_SELECTOR, value="form button")
signup_button.click()

