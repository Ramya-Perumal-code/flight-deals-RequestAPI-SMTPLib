import requests
import os
from dotenv import load_dotenv

load_dotenv("c:/personalData/Ramya/top_secret/.env")


class DataManager:
    def __init__(self):
        self.username = os.getenv("flight_username")
        self.password = os.getenv("flight_password")
        self.auth_token = os.getenv("token1")
        self.flight_endpoint = os.getenv("flight_Endpoint")
        self.users_endpoint = os.getenv("users_Endpoint")
        self.destination_data = {}
        self.customer_data = {}

    def get_flights(self):
        auth_header = {
            "Authorization": self.auth_token,
        }
        response = requests.get(url=self.flight_endpoint, auth=(self.username, self.password), headers=auth_header)
        print(response.status_code)
        self.destination_data = response.json()["prices"]
        return self.destination_data

    def put_iatacode(self, sheet_id, iatacode):
        auth_header = {
            "Authorization": self.auth_token,
        }
        param = {
            "price":
                {
                    "iataCode": iatacode

                }
        }

        response = requests.put(url=f"{self.flight_endpoint}/{sheet_id}", json=param, headers=auth_header)
        print(response.status_code)
        print(response.json())

    def get_customer_emails(self):
        auth_header = {
            "Authorization": self.auth_token,
        }
        response = requests.get(url=self.users_endpoint, auth=(self.username, self.password), headers=auth_header)
        print(response.status_code)
        self.customer_data = (response.json()["users"])
        return self.customer_data
