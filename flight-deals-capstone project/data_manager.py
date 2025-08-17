import requests
from pprint import pprint


USERNAME = "lihanda"
PASSWORD = "vugrieujgh9er898ur0er0hrefgh9eru9re80re"
sheet_api_key = "https://api.sheety.co/a9f4312606efe4cba2476d54444fb203/flightDealsProject/prices"
auth_params = {
    "Authorization": "Basic bGloYW5kYTp2dWdyaWV1amdoOWVyODk4dXIwZXIwaHJlZmdoOWVydTlyZTgwcmU ="
}


class DataManager:
    def __init__(self):
        self.data = {}
        self.customer_data = {}

    def get_data(self):
        response = requests.get(url=sheet_api_key, auth=(USERNAME, PASSWORD), headers=auth_params)
        data = response.json()
        self.data = data["prices"]
        # pprint(data["prices"])
        return self.data

    def update_destination_codes(self):
        for city in self.data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{sheet_api_key}/{city['id']}",
                json=new_data,
                auth=(USERNAME,PASSWORD),
                headers=auth_params,
            )
            print(response.text)

    def get_customer_emails(self):
        customers_endpoint = "https://api.sheety.co/a9f4312606efe4cba2476d54444fb203/flightDealsProject/users"
        response = requests.get(customers_endpoint, auth=(PASSWORD, USERNAME), headers=auth_params)
        data = response.json()["users"]
        print(data)
        self.customer_data = data
        return self.customer_data

