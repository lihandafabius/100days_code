import requests

USERNAME = "lihanda"
PASSWORD = "vugrieujgh9er898ur0er0hrefgh9eru9re80re"
sheet_api_key = "https://api.sheety.co/a9f4312606efe4cba2476d54444fb203/flightDealsProject/users"



def post_new_row(first_name, last_name, email):

    headers = {
        "Authorization": "Basic bGloYW5kYTp2dWdyaWV1amdoOWVyODk4dXIwZXIwaHJlZmdoOWVydTlyZTgwcmU =",
        "Content-Type": "application/json",
    }

    body = {
        "user": {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
        }
    }

    response = requests.post(url=sheet_api_key, headers=headers, json=body, auth=(USERNAME, PASSWORD))
    response.raise_for_status()
    print(response.text)