import requests
from twilio.rest import Client

api_key = "7cf07f74cf354fbc91940d6c51f0885d"
MY_LAT = -0.281490
MY_LONG = 36.078419
account_sid = "AC0c9d8165cc10ca5a15bef271e14044ab"
auth_token = "366495226daff75811b232dda56199d7"
OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"
parameters = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "appid": api_key,
    "cnt": 4,
}
response = requests.get(OWM_ENDPOINT, params=parameters)
response.raise_for_status()
data = response.json()
# print(data["list"][0]["weather"][0]["id"])

will_rain = False
for hour_data in data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True
if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body="It's gonna rain today. Remember to carry an umbrella☔.",
        from_='+19062144306',
        to='+254715371294'
    )

    print(message.status)

