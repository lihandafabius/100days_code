from selenium import webdriver
from selenium.webdriver.common.by import By

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# Initialize the driver
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.python.org/")
event_times = driver.find_elements(By.CSS_SELECTOR, value=".event-widget time")
# for time in event_times:
#     print(time.text)
events_names = driver.find_elements(By.CSS_SELECTOR, value=".event-widget li a")
# for event in events_names:
#     print(event.text)

events = {}
for n in range(len(event_times)):
    events[n] = {
        "time": event_times[n].text,
        "name": events_names[n].text,
    }
print(events)
driver.quit()