import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth

USERNAME = "lihanda"
PASSWORD = "vwuogywegypwuihwipeufgiwugiweugfiweu"
WEIGHT_KG = 62
HEIGHT_CM = 150
AGE = 21
APP_ID = "c2b8259f"
API_KEY = "af575c174730566e08d2e33b56b35d14"
workout_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
exercise = input("Tell me which exercise you did: ")
sheet_endpoint = "https://api.sheety.co/a9f4312606efe4cba2476d54444fb203/myWorkouts/workouts"
Date = datetime.now().strftime("%d/%m/%y")
workout_time = datetime.now().strftime("%X")

header_params = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

workout_params = {
    "query": exercise,
    "age": AGE,
    "height_cm": HEIGHT_CM,
    "weight_kg": WEIGHT_KG,

}
auth_params = {
    "Authorization": "Basic bGloYW5kYTp2d3VvZ3l3ZWd5cHd1aWh3aXBldWZnaXd1Z2l3ZXVnZml3ZXU=",
}


response = requests.post(url=workout_endpoint, json=workout_params, auth=(USERNAME,PASSWORD),headers=auth_params)
result = response.json()

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": Date,
            "time": workout_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(sheet_endpoint, json=sheet_inputs, auth=(USERNAME,PASSWORD), headers=auth_params)

    print(sheet_response.text)