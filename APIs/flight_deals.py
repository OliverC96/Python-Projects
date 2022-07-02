# Importing relevant modules/libraries
import requests
import datetime as dt
import smtplib
import time
import os
from twilio.rest import Client

# Declaring constants (keys, tokens, and endpoints for API usage)
TEQUILA_KEY = os.environ["TEQUILA_KEY"]
TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
ORIGIN_CODE = "YYC"
TEQUILA_HEADERS = {
    "apikey": TEQUILA_KEY,
    "Content-Type": "application/json",
}

SHEETY_ENDPOINT = "https://api.sheety.co/081b8783110aa213c9d733711b278567/flightDeals"
SHEETY_TOKEN = os.environ["SHEETY_TOKEN"]
SHEETY_HEADER = {
    "Authorization": "Bearer {}".format(SHEETY_TOKEN)
}

TWILIO_SID = os.environ["TWILIO_SID"]
TWILIO_TOKEN = os.environ["TWILIO_TOKEN"]
TWILIO_NUMBER = os.environ["TWILIO_NUMBER"]

MY_NUMBER = os.environ["MY_NUMBER"]
MY_EMAIL = os.environ["MY_EMAIL"]
MY_PASSWORD = os.environ["EMAIL_PASS"]
SUBJECT = "NEW LOW PRICE FLIGHT!"

BITLY_ENDPOINT = "https://api-ssl.bitly.com/v4/shorten"
BITLY_TOKEN = os.environ["BITLY_TOKEN"]
BITLY_HEADERS = {
    "Authorization": "Bearer {}".format(BITLY_TOKEN),
    "content-type": "application/json"
}

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

current_date = dt.datetime.now()
tomorrow = current_date + dt.timedelta(1)
six_months = current_date + dt.timedelta(180)


# Returns the IATA code associated with the specified city (using the Tequila API)
def flight_search(city_name: str) -> str:

    query_config = {
        "term": city_name,
        "locale": "en-US",
        "location_types": "city"
    }

    tequila_response = requests.get(url=TEQUILA_ENDPOINT + "/locations/query", params=query_config, headers=TEQUILA_HEADERS)
    tequila_response.raise_for_status()
    city_data = tequila_response.json()
    city_code = city_data["locations"][0]["code"]

    return city_code


# Populates the /prices spreadsheet with the appropriate IATA codes (using the Sheety API)
def update_codes() -> dict:

    response = requests.get(url=SHEETY_ENDPOINT + "/prices", headers=SHEETY_HEADER)
    response.raise_for_status()
    data = response.json()["prices"]

    for destination in data:

        destination["iataCode"] = flight_search(destination["city"])

        row_config = {
            "price": {
                "iataCode": destination["iataCode"],
            }
        }

        row_endpoint = SHEETY_ENDPOINT + "\prices" + "/{}".format(destination["id"])
        requests.put(url=row_endpoint, headers=SHEETY_HEADER, json=row_config)

    return data


# Returns the cheapest flight that meets the specified requirements (using the Tequila API)
def get_cheapest_flight(destination_code: str, num_stopovers: int = 0) -> dict:

    flight_config = {
        "fly_from": ORIGIN_CODE,
        "fly_to": destination_code,
        "date_from": tomorrow.strftime("%d/%m/%Y"),
        "date_to": six_months.strftime("%d/%m/%Y"),
        "nights_in_dst_from": 7,
        "nights_in_dst_to": 28,
        "flight_type": "round",
        "max_stopovers": num_stopovers,
        "curr": "CAD",
        "limit": 5000,
        "sort": "price"
    }

    cheapest_flight = requests.get(url=TEQUILA_ENDPOINT + "/v2/search", params=flight_config, headers=TEQUILA_HEADERS)
    cheapest_flight.raise_for_status()

    return cheapest_flight


# Shortens the specified url link to improve clarity of the alert message (using the Bitly API)
def shorten_link(link: str) -> str:

    bitly_config = {
        "domain": "bit.ly",
        "long_url": link
    }

    response = requests.post(url=BITLY_ENDPOINT, headers=BITLY_HEADERS, json=bitly_config)

    return response.json()["link"]


# Constructing the body of an alert message, containing all of the necessary information extracted from the tequila json response
def create_message(flight: dict) -> str:

    cost = flight["price"]
    from_name = flight["cityFrom"]
    from_code = flight["flyFrom"]
    to_name = flight["cityTo"]
    to_code = flight["flyTo"]
    from_date = flight["local_arrival"].split("T")[0]
    to_date = flight["local_departure"].split("T")[0]
    booking_link = shorten_link(flight["deep_link"])
    num_stopovers = 0
    stopover_city = flight["route"][0]["cityTo"]

    if len(flight["route"]) > 2:

        num_stopovers += 1

    alert_message = "Low Price Alert!\nOnly ${} to fly from {}-{} to {}-{}, from {} to {}. ".format(cost, from_name, from_code, to_name, to_code, from_date, to_date)

    if num_stopovers != 0:

        alert_message += "\nFlight has {} stop over, via {}".format(num_stopovers, stopover_city)

    alert_message += "\nBooking link: {}".format(booking_link)

    return alert_message


# Sends an SMS message alerting the recipient of a low price flight that is within their budget (using the Twilio API)
def send_sms(flight: dict):

    twilio_client = Client(TWILIO_SID, TWILIO_TOKEN)

    twilio_client.messages \
        .create(
            body=create_message(flight),
            from_=TWILIO_NUMBER,
            to=MY_NUMBER
        )


# Adds a user to the 'Flight Club'; appends their account data to the /users spreadsheet
def add_user():

    print("Welcome to Oliver's Flight Club!")
    print("I find the best flight deals on the market and email them directly to you.")

    first_name = input("What is your first name? ")
    last_name = input("What is your last name? ")
    email = input("What is your email address? ")
    confirmation = input("Please enter your email address again to confirm: ")

    while email != confirmation:

        confirmation = input("Emails don't match - please enter your email address again to confirm: ")

    user_data = {
        "user": {
            "firstName": first_name,
            "lastName": last_name,
            "email": email
        }
    }

    requests.post(url=SHEETY_ENDPOINT + "/users", headers=SHEETY_HEADER, json=user_data)

    print("Congratulations - you're now a member of the flight club!")


# Sends an email alert regarding a low price flight to every user on the mailing list (using the smtplib module)
def send_emails(flight: dict):

    response = requests.get(url=SHEETY_ENDPOINT + "/users", headers=SHEETY_HEADER)
    response.raise_for_status()
    users = response.json()["users"]

    for user in users:

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as connection:

            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=user["email"],
                msg="Subject: {}\n\n{}".format(SUBJECT, create_message(flight))
            )


if __name__ == "__main__":

    # Executes the program once per day
    while True:

        time.sleep(86400)

        # Retrieves data from the /prices spreadsheet
        flight_data = update_codes()
        threshold_prices = {}

        # A dictionary in the format of [city] : cheapest flight to [city]
        cheap_flights = {}

        for destination in flight_data:

            threshold_prices[destination["city"]] = destination["lowestPrice"]

            # Searches for direct flights
            try:

                cheapest_flight = get_cheapest_flight(destination["iataCode"]).json()["data"][0]

            # Searches for one-stopover (each way) flights if there doesn't exist any direct flight that meets the specifications
            except (IndexError, KeyError):

                try:

                    cheapest_flight = get_cheapest_flight(destination["iataCode"], 2).json()["data"][0]

                # Assigns an empty string as the flight if no valid one-stopover flight is found
                except (IndexError, KeyError):

                    cheapest_flight = ""

            else:

                # Searches for one-stopover (each way) flights if there exists direct flights, but none of which are below the price threshold
                if cheapest_flight["price"] > threshold_prices[destination["city"]]:

                    cheapest_flight = get_cheapest_flight(destination["iataCode"], 2).json()["data"][0]

            cheap_flights[destination["city"]] = cheapest_flight

        # Sends an SMS and email message containing a breakdown of any flight found that costs less than the threshold value
        for city, flight_info in cheap_flights.items():

            if flight_info != "":

                if flight_info["price"] <= threshold_prices[city]:

                    send_sms(flight_info)
                    send_emails(flight_info)
