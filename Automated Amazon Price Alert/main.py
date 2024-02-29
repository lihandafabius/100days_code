import requests
from bs4 import BeautifulSoup
import lxml
import smtplib
import os


my_email = os.environ.get("email")
password = os.environ.get("smtplib_password")

url = "https://www.amazon.com/s?k=macbook+air&crid=K13Y3REJYYHI&sprefix=ma%2Caps%2C896&ref=nb_sb_ss_ts-doa-p_3_2"
headers = {
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,"
              "image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "sec-fetch-dest": "document",
    "Accept-Encoding": "gzip, deflate, br, zstd",

}

response = requests.get(url,headers=headers)
data = response.text
print(data)
soup = BeautifulSoup(data, "lxml")
price = soup.find(name="span", class_="a-price-whole").getText()
price = float(price.split("$")[1])
title = soup.find(id="productTitle").get_text().strip()
print(title)

BUY_PRICE = 200

if price < BUY_PRICE:
    message = f"{title} is now {price}"

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        result = connection.login(my_email, password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=my_email,
            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{url}".encode("utf-8")
        )



