import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time

from selenium.webdriver.support.wait import WebDriverWait

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
        self.driver.get("https://www.speedtest.net/")
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, ".start-text").click()
        WebDriverWait(self.driver, 120).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div[data-result-id*='true']"))
        )
        self.down = float(self.driver.find_element(By.CSS_SELECTOR, ".download-speed").text)
        self.up = float(self.driver.find_element(By.CSS_SELECTOR, ".upload-speed").text)
        print(f"up {self.up} down {self.down}")

    # def tweet_at_provider(self):
    #     self.driver.get("https://twitter.com/login")
    #
    #     time.sleep(2)
    #     email = self.driver.find_element_by_xpath(
    #         '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/form/div/div[1]/label/div/div[2]/div/input')
    #     password = self.driver.find_element_by_xpath(
    #         '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/form/div/div[2]/label/div/div[2]/div/input')
    #
    #     email.send_keys(TWITTER_EMAIL)
    #     password.send_keys(TWITTER_PASSWORD)
    #     time.sleep(2)
    #     password.send_keys(Keys.ENTER)
    #
    #     time.sleep(5)
    #     tweet_compose = self.driver.find_element_by_xpath(
    #         '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div')
    #
    #     tweet = f"Hey Internet Provider, why is my internet speed {self.down}down/{self.up}up when I pay for {PROMISED_DOWN}down/{PROMISED_UP}up?"
    #     tweet_compose.send_keys(tweet)
    #     time.sleep(3)
    #
    #     tweet_button = self.driver.find_element_by_xpath(
    #         '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[4]/div/div/div[2]/div[3]')
    #     tweet_button.click()
    #
    #     time.sleep(2)
    #     self.driver.quit()


bot = InternetSpeedTwitterBot()
# bot.tweet_at_provider()
bot.get_internet_speed()




