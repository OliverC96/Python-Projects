# Importing relevant modules/libraries
import requests
from bs4 import BeautifulSoup
import smtplib
import time

# Declaring constants
PRODUCT_URL = "https://www.amazon.ca/Crate-61-essential-patchouli-activated/dp/B07CMJ4XGF/ref=sxts_rp_s_1_0?content-id=amzn1.sym.c7f6ac45-4e13-4a92-93ea-0aa88f4cc599%3Aamzn1.sym.c7f6ac45-4e13-4a92-93ea-0aa88f4cc599&crid=8LMPK7R07UON&cv_ct_cx=soap&keywords=soap&pd_rd_i=B07CMJ4XGF&pd_rd_r=61166338-3077-446b-bed5-5a9f440906f8&pd_rd_w=JqioT&pd_rd_wg=tgSSW&pf_rd_p=c7f6ac45-4e13-4a92-93ea-0aa88f4cc599&pf_rd_r=C6HEVFX4PMM87F2SJEE7&psc=1&qid=1656986150&sprefix=soap%2Caps%2C157&sr=1-1-f0029781-b79b-4b60-9cb0-eeda4dea34d6"
TITLE = "Amazon Price Alert!"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = "587"
MY_EMAIL = "clennanoliver@gmail.com"
MY_PASS = "cphxyuahejhnrhnc"
RECIPIENT = "oliverclennan@gmail.com"

QUERY_HEADER = {
    "accept-language": "en-CA,en-US;q=0.9,en;q=0.8",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15"
}

BITLY_ENDPOINT = "https://api-ssl.bitly.com/v4/shorten"
BITLY_TOKEN = "1115da2722bf2f8c01ae6709c4a3aa6645437d11"
BITLY_HEADERS = {
    "Authorization": "Bearer {}".format(BITLY_TOKEN),
    "content-type": "application/json"
}


# Shortens the specified url link to improve clarity of the alert message (using the Bitly API)
def shorten_link(link: str) -> str:

    bitly_config = {
        "domain": "bit.ly",
        "long_url": link
    }

    response = requests.post(url=BITLY_ENDPOINT, headers=BITLY_HEADERS, json=bitly_config)

    return response.json()["link"]


# Returns a tuple containing the name and price of the product specified in the Amazon url (using the BeautifulSoup library)
def get_product_info(product_url: str) -> tuple:

    response = requests.get(product_url, headers=QUERY_HEADER)
    product_page = response.text
    soup = BeautifulSoup(product_page, "lxml")

    item_price = soup.select("span .a-offscreen")[0].text[1:]
    item_name = soup.select("title")[0].text.split(' : ')[0]

    return item_name, item_price


# Sends an email price alert containing the name and current price of the product, and a link to it's Amazon page (using the smtplib module)
def send_email_alert(price: float, name: str, link: str):

    body = "** NOW FOR ONLY ${} **\n{}\n{}".format(price, name, shorten_link(link))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as connection:

        connection.starttls()
        connection.login(MY_EMAIL, MY_PASS)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=RECIPIENT,
            msg="Subject: {}\n\n{}".format(TITLE, body)
        )

if __name__ == "__main__":

    # Displaying the welcome message, and prompting user to enter the price of the product, and it's Amazon url
    print("Welcome to the Amazon Price Tracker!")
    amazon_url = input("Please enter a valid Amazon Product URL: ")
    price_threshold = input("Please enter an integer price threshold to trigger the alerts: $")

    # Continually prompting the user until a valid (integer) price threshold is entered
    while not price_threshold.isdigit():

        price_threshold = input("Invalid entry - please enter an integer price threshold: $")

    # Continuously retrieving the price of the product every 60 sec. / 1 min.
    while True:

        time.sleep(60)

        product_name, current_price = get_product_info(amazon_url)

        # Sending an email alert message if the current price is below the user-specified threshold value
        if round(float(current_price)) <= int(price_threshold):

            send_email_alert(current_price, product_name, amazon_url)
