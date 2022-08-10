# Importing relevant modules/libraries
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
import requests
import time
import json
import os

# Declaring constants (API endpoints, headers and tokens)
FORM_LINK = os.environ["FORM_LINK"]
ZILLOW_LINK = "https://www.zillow.com"

QUERY_HEADER = {
    "accept-language": "en-CA,en-US;q=0.9,en;q=0.8",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15"
}

BITLY_ENDPOINT = "https://api-ssl.bitly.com/v4/shorten"
BITLY_TOKEN = os.environ["BITLY_TOKEN"]
BITLY_HEADERS = {
    "Authorization": "Bearer {}".format(BITLY_TOKEN),
    "content-type": "application/json"
}


# Shortens the specified url link to improve clarity (using the Bitly API)
def shorten_link(link: str) -> str:

    bitly_config = {
        "domain": "bit.ly",
        "long_url": link
    }

    response = requests.post(url=BITLY_ENDPOINT, headers=BITLY_HEADERS, json=bitly_config)

    return response.json()["link"]


# NOTE - this method may not always work due to complex anti-bot measures embedded within the Zillow site (eg. CAPTCHA software) - human intervention may be required
# Executes a Zillow search with the given parameters, and returns the url containing the search results (url reconstruction not feasible)
def zillow_search(city: str, min_price: int = 0, max_price: int = 3000, num_beds: int = 1, num_baths: int = 0) -> str:

    # Initializing an 'undetected' web driver object; opening Zillow's home page
    options = webdriver.ChromeOptions()
    options.headless = False
    driver = uc.Chrome(options=options)
    driver.get(ZILLOW_LINK)
    time.sleep(15)

    rent_tab = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/header/nav/div[2]/ul[1]/li[2]/a')
    rent_tab.click()
    time.sleep(4)

    # Applies the specified filters to the search
    location_field = driver.find_element(By.XPATH, '/html/body/div[1]/div[5]/div/section/div[1]/div/form/div/div/input')
    location_field.send_keys(city, Keys.ENTER)
    time.sleep(2)

    price_tab = driver.find_element(By.XPATH, '/html/body/div[1]/div[5]/div/section/div[2]/div/div[2]/button')
    price_tab.click()
    time.sleep(2)

    min_field = driver.find_element(By.XPATH, '//*[@id="price-exposed-min"]')
    min_field.click()
    time.sleep(0.5)
    min_field.send_keys(min_price)
    time.sleep(1)

    max_field = driver.find_element(By.XPATH, '//*[@id="price-exposed-max"]')
    max_field.click()
    time.sleep(0.5)
    max_field.send_keys(max_price, Keys.ENTER)
    time.sleep(1)

    bb_tab = driver.find_element(By.XPATH, '//*[@id="beds"]')
    bb_tab.click()
    time.sleep(1)

    # Necessary for attaining the correct xpath of the button corresponding to the desired number of bathrooms
    bath_xpath = {
        0: 1,
        1: 2,
        1.5: 3,
        2: 4,
        3: 5,
        4: 6,
    }

    beds_button = driver.find_element(By.XPATH, '//*[@id="beds-form"]/fieldset[1]/div[1]/button[{}]'.format(num_beds + 1))
    beds_button.click()
    baths_button = driver.find_element(By.XPATH, '//*[@id="beds-form"]/fieldset[2]/div/button[{}]'.format(bath_xpath[num_baths]))
    baths_button.click()
    driver.find_element(By.XPATH, '//*[@id="exposed-filters-exact-beds"]').click()
    time.sleep(1)

    driver.find_element(By.XPATH, '/html/body/div[1]/div[5]/div/section/div[2]/div/div[3]/div/div/div/button').click()
    time.sleep(2)

    return driver.current_url



# Correctly formats the price and url link of the property listing
def adjust_attributes(price, link: str) -> tuple:

    # A valid link must start with https://zillow.com
    if "https" not in link:

        formatted_link = shorten_link("https://zillow.com" + link)

    else:

        formatted_link = shorten_link(link)

    # If the price is in integer form, add a dollar sign and comma at the appropriate indices
    if isinstance(price, int):

        price = str(price)
        formatted_price = "$" + price[0] + "," + price[1:]

    # Otherwise, remove the unnecessary plus sign at the end of the price string
    else:

        if "C" in price:

            price = price.replace("C", "")

        formatted_price = price.replace("+", "")

    return formatted_price, formatted_link


# Returns a nested dictionary (json), containing the information (rent price, listing link and address) of each property found by the Zillow search
def retrieve_properties(search_url: str) -> dict:

    properties = {}
    i = 0

    # Obtaining the content of the Zillow page (using the Requests module)
    response = requests.get(url=search_url, headers=QUERY_HEADER)
    response.raise_for_status()

    # Parsing through the data to isolate the property search results (using the BeautifulSoup library)
    soup = BeautifulSoup(response.text, "lxml")
    javascript_data = soup.find('script', {'data-zrr-shared-data-key': 'mobileSearchPageStore'}).text
    json_data = json.loads(javascript_data.split('--')[1])
    all_listings = json_data["cat1"]["searchResults"]["listResults"]

    # Iterating through all of the listings
    for listing in all_listings:

        listing_address = listing["address"]
        raw_link = listing["detailUrl"]

        # Handling units with multiple prices (1/2/3+ bedroom variants)
        try:

            raw_price = listing["unformattedPrice"]

        except KeyError:

            raw_price = listing["units"][0]["price"]

        listing_price, listing_link = adjust_attributes(raw_price, raw_link)

        # Constructing the nested dictionary
        properties[i] = {
            "price": listing_price,
            "address": listing_address,
            "link": listing_link
        }

        i += 1

    return properties


# Automatically fills out the Google form with the given parameters (using the Selenium library)
def populate_form(address: str, rent: str, link: str):

    # Initializing a web driver object; opening the form in a Chrome window
    driver = webdriver.Chrome(executable_path="chromedriver")
    driver.get(url=FORM_LINK)
    time.sleep(1)

    address_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_field.send_keys(address)
    time.sleep(0.5)

    rent_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    rent_field.send_keys(rent)
    time.sleep(0.5)

    link_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_field.send_keys(link)
    time.sleep(0.5)

    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
    submit_button.click()


# Searches for desirable rental properties on Zillow and populates a google form with information pertaining to these properties
if __name__ == "__main__":

    zillow_url = zillow_search("Calgary", 1000, 3500, 1, 1)
    properties = retrieve_properties(zillow_url)

    for property in properties.values():

        populate_form(property["address"], property["price"], property["link"])
