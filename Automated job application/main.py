from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

Password = ""
Email = ""

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# Initialize the driver
driver = webdriver.Chrome(options=chrome_options)

url= ("https://www.linkedin.com/jobs/search/?currentJobId=3828092607&f_AL=true&f_WT=3%2C2%2C1&geoId=100339781&keywords="
       "python%20developer&location=Nairobi%2C%20Nairobi%20County%2C%20Kenya&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh="
       "true&spellCorrectionEnabled=true")
driver.get(url)


time.sleep(2)
sign_in = driver.find_element(By.XPATH, value="/html/body/div[1]/header/nav/div/a[2]")
sign_in.click()

# time.sleep(5)
# email_phone = driver.find_element(By.CSS_SELECTOR, value=".text-input flex input")
# email_phone.send_keys(Email, Keys.ENTER)

time.sleep(2)
sign_in_button = driver.find_element(by=By.LINK_TEXT, value="Sign in")
sign_in_button.click()

time.sleep(5)
email_field = driver.find_element(by=By.ID, value="username")
email_field.send_keys(Email, Keys.ENTER)
password_field = driver.find_element(by=By.ID, value="password")
password_field.send_keys(Password, Keys.ENTER)
login = driver.find_element(By.CSS_SELECTOR, value=".login__form_action_container button")
login.click()

# password = driver.find_element(By.ID, value="session_password")
# password.send_keys(Password, Keys.ENTER)
# log_in = driver.find_element(By.CLASS_NAME, value="btn-md btn-primary flex-shrink-0 cursor-pointer sign-in-form__submit-btn--full-width")
# log_in.click()
driver.quit()




