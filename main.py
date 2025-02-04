#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

import time
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager
from datetime import datetime, timedelta
import smtplib
from dotenv import load_dotenv

# load_dotenv("c:/personalData/Ramya/top_secret/.env")
datamanager = DataManager()
flightsearch = FlightSearch()
notificationmanager = NotificationManager()

ORIGIN_CITY_CODE = 'LON'

sheet_data = datamanager.get_flights()

for data in sheet_data:
    if data['iataCode'] == '':
        data['iataCode'] = flightsearch.get_city_code(data['city'])
        print(f"iatacode: {data['iataCode']}")
        time.sleep(2)

travel_date = datetime.now() + timedelta(days=1)
return_date = travel_date + timedelta(days=6 * 30)

user_data = datamanager.get_customer_emails()
user_mail_ids = [user['whatIsYourEmailAddress?'] for user in user_data]

for destn in sheet_data:
    print(f"Getting the flight details for {destn['city']}")
    flights = flightsearch.check_flights(ORIGIN_CITY_CODE, destn['iataCode'], travel_date, return_date, "true")
    cheapest_flight = find_cheapest_flight(flights)
    time.sleep(2)

    if cheapest_flight.stops == 'N/A':
        print(f"No direct flight to {destn['city']}. Looking for indirect flights...")
        flights = flightsearch.check_flights(ORIGIN_CITY_CODE, destn['iataCode'], travel_date, return_date, "false")
        cheapest_flight = find_cheapest_flight(flights)

    print(f"{destn['city']}: £ {cheapest_flight.price}")

    if not cheapest_flight.price == 'N/A':
        if float(destn['lowestPrice']) > cheapest_flight.price:
            if cheapest_flight.stops == 0:
                message = (f"Only £ {cheapest_flight.price} to fly  direct from {cheapest_flight.origin_airport} "
                           f" to {cheapest_flight.departure_airport}, on {cheapest_flight.out_date} "
                           f"with {cheapest_flight.stops} stop(s) "
                           f"until {cheapest_flight.return_date}.")
            else:
                message = (f"Only £ {cheapest_flight.price} to fly   from {cheapest_flight.origin_airport} "
                           f" to {cheapest_flight.departure_airport}, on {cheapest_flight.out_date} "
                           f"with {cheapest_flight.stops} stop(s) "
                           f"departing on  {cheapest_flight.out_date} and returning on {cheapest_flight.return_date}.")

            print(f"Check your email. Lower price flight found to {destn['city']}!")
            for user in user_mail_ids:
                notificationmanager.send_mail(message, user)

    time.sleep(2)
