from selenium import webdriver
from selenium.webdriver.common.by import By
import time

options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=options)

driver.get('https://orteil.dashnet.org/experiments/cookie/')

cookie = driver.find_element(By.ID, 'cookie')
timeout = time.time() + 5
stop = time.time() + 5 * 60

while time.time() < stop:
    cookie.click()
    if time.time() > timeout:
        prizes_list = driver.find_elements(By.CSS_SELECTOR, '#store div:not(.grayed)>b')
        #  get element which are not grayed i.e. which can be availed
        prize_to_click = prizes_list[-1]  # last element has highest value
        prize_to_click.click()
        timeout = time.time() + 5

cps_el = driver.find_element(By.ID, 'cps')
print(cps_el.text)
driver.quit()



