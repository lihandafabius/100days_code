import keyboard
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from PIL import Image, ImageGrab
import time
import math
import io

def get_pixel(image, x, y):
    # Load the image and get the color of the pixel at (x, y)
    px = image.load()
    return px[x, y]

def start():
    # Selenium setup for controlling Chrome
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)

    # Access the T-Rex game via a public URL
    driver.get("https://elgoog.im/t-rex/")

    # Give the user time to switch to the Chrome window
    time.sleep(3)

    # Start the game by pressing space
    body = driver.find_element(By.TAG_NAME, "body")
    body.send_keys(Keys.SPACE)

    # Initialize variables for game control
    x, y, width, height = 0, 102, 1920, 872
    jumping_time = 0
    last_jumping_time = 0
    current_jumping_time = 0
    last_interval_time = 0

    y_search1, y_search2, x_start, x_end = 557, 486, 400, 415
    y_search_for_bird = 460

    while True:
        # Re-fetch the body element in each loop iteration to avoid stale element reference
        body = driver.find_element(By.TAG_NAME, "body")

        # Press 'q' to quit the bot
        if keyboard.is_pressed('q'):
            break

        # Take a screenshot using Selenium and convert it to a BytesIO object
        screenshot = driver.get_screenshot_as_png()
        img = Image.open(io.BytesIO(screenshot))  # Convert byte data to an image

        # Get background color from the screenshot
        bg_color = get_pixel(img, 100, 100)

        # Check for obstacles
        for i in reversed(range(x_start, x_end)):
            # Check if the pixel at (i, y_search1) or (i, y_search2) is not the background color
            if get_pixel(img, i, y_search1) != bg_color or get_pixel(img, i, y_search2) != bg_color:
                body.send_keys(Keys.ARROW_UP)  # Press up to jump
                jumping_time = time.time()
                current_jumping_time = jumping_time
                break
            # Check for bird obstacle and duck
            if get_pixel(img, i, y_search_for_bird) != bg_color:
                body.send_keys(Keys.ARROW_DOWN)  # Press down to duck
                time.sleep(0.4)  # Hold down for a short time
                body.send_keys(Keys.NULL)  # Release down key
                break

        # Calculate interval time between jumps
        interval_time = current_jumping_time - last_jumping_time

        # Adjust the end of the search area if the game speeds up
        if last_interval_time != 0 and math.floor(interval_time) != math.floor(last_interval_time):
            x_end += 4
            if x_end >= width:
                x_end = width

        # Update jump time tracking
        last_jumping_time = jumping_time
        last_interval_time = interval_time

start()
