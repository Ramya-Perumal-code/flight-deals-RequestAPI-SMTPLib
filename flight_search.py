from datetime import datetime
import requests
import os
from dotenv import load_dotenv
import json

TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"
CITY_SEARCH_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
FLIGHT_OFFER_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"


class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self._api_key = os.getenv("amadeus_Api_key")
        self._api_secret = os.getenv("amadeus_Api_secret")
        self._token = self._get_new_token()

    def _get_new_token(self):

        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            'grant_type': 'client_credentials',
            'client_id': self._api_key,
            'client_secret': self._api_secret,
        }
        response = requests.post(url=TOKEN_ENDPOINT, headers=header, data=body)
        return response.json()['access_token']

    def get_city_code(self, city_name):
        print(self._token)
        header = {
            "Authorization": f"Bearer {self._token}"
        }
        param = {
            "keyword": city_name,
            "max": "2",
            "include": "AIRPORTS"
        }
        response = requests.get(url=CITY_SEARCH_ENDPOINT, params=param, headers=header)
        print(f"Status code : {response.status_code}")


        try:
            code = response.json()["data"][0]["iataCode"]
        except IndexError:
            print(f"Index Error: No airport code found for {city_name}")
            return "N/A"
        except KeyError:
            print(f"Key Error: No airport code found for {city_name} ")
            return "Not found"

        return code

    def check_flights(self, origin_city_code, destn_city_code, from_date, return_date, is_direct):
        header = {
            "Authorization": f"Bearer {self._token}"
        }
        param = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destn_city_code,
            "departureDate": from_date.strftime("%Y-%m-%d"),
            "returnDate": return_date.strftime("%Y-%m-%d"),
            "adults": 1,
            "currencyCode": "GBP",
            "max": "10",
            "nonStop": is_direct

        }
        response = requests.get(url=FLIGHT_OFFER_ENDPOINT, headers=header, params=param)
        if response.status_code != 200:
            print(f"check_flight response code: {response.status_code}")
            print("Response body", response.text)
            return None
        # print(json.dumps(response.json()))
        return response.json()
