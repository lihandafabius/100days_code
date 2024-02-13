# import smtplib
#
# my_email = "fabiuslihandaachevi@gmail.com"
# password = "etmm guyf pbzh yeck"
#
# with smtplib.SMTP("smtp.gmail.com") as connection:
#     connection.starttls()
#
#     connection.login(user=my_email, password=password)
#     connection.sendmail(from_addr=my_email, to_addrs="fabiuslihanda8@gmail.com", msg="Subject:Niaje mzee\n\nthis is "
#                                                                                      "the body of my mail")

# import datetime as dt
# now = dt.datetime.now()
# print(now)

import smtplib
import datetime as dt
import random

my_email = "fabiuslihandaachevi@gmail.com"
MY_PASSWORD = "etmm guyf pbzh yeck"
now = dt.datetime.now()
weekday = now.weekday()
if weekday == 1:
    with open("quotes.txt") as quote_file:
        all_quotes = quote_file.readlines()
        quote = random.choice(all_quotes)
    print(quote)
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(my_email, MY_PASSWORD)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=my_email,
            msg=f"Subject:Monday Motivation\n\n{quote}"
        )
