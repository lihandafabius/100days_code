from pprint import pprint
import requests

USERNAME = "lihanda"
PASSWORD = "vugrieujgh9er898ur0er0hrefgh9eru9re80re"
sheet_api_key = "https://api.sheety.co/a9f4312606efe4cba2476d54444fb203/flightDealsProject/prices"
auth_params = {
    "Authorization": "Basic bGloYW5kYTp2dWdyaWV1amdoOWVyODk4dXIwZXIwaHJlZmdoOWVydTlyZTgwcmU ="
}



class DataManager:

    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=sheet_api_key, auth=(PASSWORD, USERNAME), headers=auth_params)
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{sheet_api_key}/{city['id']}",
                json=new_data
            )
            print(response.text)


