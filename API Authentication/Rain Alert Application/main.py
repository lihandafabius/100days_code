import requests
from twilio.rest import Client

api_key = ""
MY_LAT = -0.281490
MY_LONG = 36.078419
account_sid = ""
auth_token = ""
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

