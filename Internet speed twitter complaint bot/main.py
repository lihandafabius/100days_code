import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

password = os.getenv("PASSWORD")
username = os.getenv("email")
promised_up = 10
promised_down = 100


class InternetSpeedTwitterBot:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.down = 0
        self.up = 0

    def get_internet_speed(self):
        self.driver.get("https://speedtest.net/")
        time.sleep(4)
        go_button = self.driver.find_element(By.CSS_SELECTOR, value=".engine-wrapper a")
        go_button.click()


    def tweet_at_provider(self):
        pass


bot = InternetSpeedTwitterBot()
bot.tweet_at_provider()
bot.get_internet_speed()




