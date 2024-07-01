import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Function to scroll down the page
def scroll_down(driver, last_height):
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(2)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    return new_height != last_height, new_height

# Function to scrape tweets
def scrape_tweets(query, start_date, end_date):
    # Initialize Chrome driver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to Twitter advanced search page
    url = f"https://twitter.com/search?q={query}%20since%3A{start_date}%20until%3A{end_date}&src=typed_query"
    driver.get(url)
    time.sleep(3)

    # Infinite scroll to load more tweets
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        scrolled, new_height = scroll_down(driver, last_height)
        if not scrolled:
            break
        last_height = new_height

    # Extract tweets
    tweets = driver.find_elements(By.XPATH, "//div[@data-testid='tweet']")
    tweet_data = []
    for tweet in tweets:
        username = tweet.find_element(By.XPATH, ".//span[contains(@class, 'css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0')]").text
        tweet_text = tweet.find_element(By.XPATH, ".//div[@lang='en']").text
        tweet_data.append((username, tweet_text))

    driver.quit()
    return tweet_data

# Example usage
if __name__ == "__main__":
    query = "#BlackLivesMatter"
    start_date = "2021-06-28"
    end_date = "2024-06-28"
    tweets = scrape_tweets(query, start_date, end_date)
    for tweet in tweets:
        print(tweet)
