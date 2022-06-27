# Importing relevant modules/libraries
import requests
import datetime as dt
import random
import os
from twilio.rest import Client

# Declaring constants
STOCK_API_KEY = os.environ["STOCK_KEY"]
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_API_KEY = os.environ["NEWS_KEY"]
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

TICKER = "TSLA"
NAME = "Tesla"
DOWN_ARROW = "🔻"
UP_ARROW = "🔺"

ACCOUNT_SID = os.environ["TWILIO_SID"]
AUTH_TOKEN = os.environ["TWILIO_TOKEN"]
TWILIO_NUMBER = os.environ["TWILIO_NUMBER"]
MY_NUMBER = os.environ["MY_NUMBER"]


# Returns a two-tuple containing the current date and the most recent weekday, in ISO 8601 format
def get_date() -> tuple:

    current = dt.datetime.now()
    yesterday = current - dt.timedelta(days=1)

    # If the current day is a monday, yesterday is set to the most recent weekday (i.e. the previous Friday)
    if current.weekday() == 0:

        yesterday = yesterday - dt.timedelta(days=2)

    c_date = current.strftime("%Y") + "-" + current.strftime("%m") + "-" + current.strftime("%d")
    y_date = yesterday.strftime("%Y") + "-" + yesterday.strftime("%m") + "-" + yesterday.strftime("%d")

    return c_date, y_date


# Computes the daily percentage variation of the specified stock ticker (using the AlphaVantage API)
def get_daily_change(date: str, prev_date: str, symbol: str) -> str:

    stock_parameters = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": "compact",
        "datatype": "json",
        "apikey": STOCK_API_KEY
    }

    stock_response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
    stock_response.raise_for_status()
    stock_data = stock_response.json()["Time Series (Daily)"]

    daily_data = stock_data[date]
    prev_data = stock_data[prev_date]

    close_price = float(daily_data["4. close"])
    prev_close_price = float(prev_data["4. close"])
    daily_variation = (((close_price - prev_close_price) / prev_close_price) * 100)
    daily_variation = round(daily_variation, 2)
    arrow = ""

    if daily_variation < 0:

        arrow += DOWN_ARROW

    else:

        arrow += UP_ARROW

    return arrow + str(abs(daily_variation)) + "%"


# Retrieves a popular, recent news article pertaining to the specified company name (using the News API)
def get_recent_news(company_name: str) -> tuple:

    news_parameters = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": company_name,
        "language": "en",
        "sortBy": "popularity",
        "pageSize": 3
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    news_response.raise_for_status()
    article_num = random.randint(0,2)
    news_article = news_response.json()["articles"][article_num]
    title = news_article["title"]
    description = news_article["description"]

    return title, description


# Sending an SMS alert to the given phone number (using the Twilio API)
if __name__ == "__main__":

    # Only sends alerts on weekdays (as the stock market is closed on weekends)
    if dt.datetime.now().weekday() <= 4:

        date = get_date()
        daily_percent = get_daily_change(date[0], date[1], TICKER)
        recent_news = get_recent_news(NAME)

        # Only sends an alert if the stock's daily price variation meets, or exceeds, 5%
        if int(daily_percent[1]) >= 5:

            # Message contains the stock's daily price action, and a relevant, recent news article
            alert_message = TICKER + daily_percent + "\n\n" + recent_news[0] + "\n\n" + recent_news[1]

            twilio_client = Client(ACCOUNT_SID, AUTH_TOKEN)

            sms_message = twilio_client.messages \
                .create(
                    body=alert_message,
                    from_=TWILIO_NUMBER,
                    to=MY_NUMBER
                )
