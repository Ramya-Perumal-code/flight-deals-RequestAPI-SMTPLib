class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self, price, origin_airport, departure_airport, out_date, return_date, stops):
        self.price = price
        self.departure_airport = departure_airport
        self.origin_airport = origin_airport
        self.out_date = out_date
        self.return_date = return_date
        self.stops = stops


def find_cheapest_flight(data):
    if data is None or not data['data']:
        print("No flight data")
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A", "N/A")

    first_flight = data["data"][0]

    lowest_price = float(first_flight['price']['grandTotal'])
    stops = len(first_flight["itineraries"][0]["segments"]) - 1
    origin_airport = first_flight["itineraries"][0]["segments"][0]['departure']["iataCode"]
    departure_airport = first_flight["itineraries"][0]["segments"][stops]['arrival']["iataCode"]
    out_date = first_flight["itineraries"][0]["segments"][0]['departure']["at"].split("T")[0]
    return_date = first_flight["itineraries"][0]["segments"][0]['arrival']["at"].split("T")[0]

    cheapest_flight = FlightData(lowest_price, origin_airport, departure_airport, out_date, return_date,stops)

    for flight in data["data"]:
        price = float(flight['price']['grandTotal'])
        if price < lowest_price:
            lowest_price = price
            stops = len(flight["itineraries"][0]["segments"]) - 1
            origin_airport = flight["itineraries"][0]["segments"][0]['departure']["iataCode"]
            departure_airport = flight["itineraries"][0]["segments"][stops]['arrival']["iataCode"]
            out_date = flight["itineraries"][0]["segments"][0]['departure']["at"].split("T")[0]
            return_date = flight["itineraries"][0]["segments"][0]['arrival']["at"].split("T")[0]
            cheapest_flight = FlightData(lowest_price, origin_airport, departure_airport, out_date, return_date, stops)
            print(f"lowest price to {departure_airport} is £{lowest_price}")


    # print(data)
    return cheapest_flight

