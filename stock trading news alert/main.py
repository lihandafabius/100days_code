import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = "PWYNRTQ6L2IUPKVT"
NEWS_API_KEY = "2df5847fa54e4881a90caad4385de4c5"
account_sid = "AC0c9d8165cc10ca5a15bef271e14044ab"
auth_token = "366495226daff75811b232dda56199d7"
# STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").


parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "interval": "Daily",
    "apikey": "STOCK_API_KEY",
}
response = requests.get(STOCK_ENDPOINT, params=parameters)
response.raise_for_status()
data = response.json()
yesterday = float(data["Time Series (Daily)"]["2024-02-16"]["4. close"])
print(yesterday)

day_before_yesterday = float(data["Time Series (Daily)"]["2024-02-15"]["4. close"])
print(day_before_yesterday)

difference = abs(yesterday - day_before_yesterday)
print(difference)

percentage_diff = (difference / yesterday) * 100
print(percentage_diff)
# TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").
if percentage_diff > 0.1:
    news_params = {
        "q": COMPANY_NAME,
        "apiKey": NEWS_API_KEY,
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"]
    print(news_data)

    three_articles = news_data[:3]
    formatted_articles = [f"{article['title']}. \nBrief: {article['description']}" for article in three_articles]
    print(formatted_articles)

    client = Client(account_sid, auth_token)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_='+19062144306',
            to='+254715371294'
        )



