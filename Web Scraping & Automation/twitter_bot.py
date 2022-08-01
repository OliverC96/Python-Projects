# Importing relevant modules/libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Declaring constants and global variables
TWITTER_MAIN = "https://twitter.com"
MY_USER = "OliverClennan"
MY_PASS = "601155002"
DESIRED_DOWN = 75
DESIRED_UP = 75
OOKLA_ENDPOINT = "https://www.speedtest.net"
ISP_NAME = "telus"
chrome_driver_path = "chromedriver"


# Logging in to the Twitter account associated with the given credentials
def twitter_login(username: str, password: str):

    driver = webdriver.Chrome(executable_path=chrome_driver_path)
    driver.get(url=TWITTER_MAIN)
    time.sleep(6)

    login_button = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[5]/a')
    login_button.click()
    time.sleep(2)

    username_field = driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')
    username_field.send_keys(username)
    username_field.send_keys(Keys.ENTER)
    time.sleep(2)

    password_field = driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
    password_field.send_keys(password)
    password_field.send_keys(Keys.ENTER)
    time.sleep(4)

    # Returns the current web driver object to be used for subsequent tasks on twitter (tweeting, sending direct messages)
    return driver


# Logging out of the Twitter account, terminating the Selenium web driver object
def twitter_logout(driver):

    profile_button = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/header/div/div/div/div[2]/div/div')
    profile_button.click()
    time.sleep(2)

    logout_button = driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div[2]/div/div[2]/div/div/div/div/div/a[2]')
    logout_button.click()
    time.sleep(2)

    confirm_button = driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div[2]/div[1]')
    confirm_button.click()
    time.sleep(3)

    driver.stop_client()
    driver.close()


# Sending a complaint to the Internet Service Provider (ISP) via a private/direct message
def send_direct_complaint(driver, isp_name: str, download: int, upload: int):

    search_field = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/label/div[2]/div/input')
    search_field.send_keys(isp_name + " support")
    time.sleep(1)
    search_field.send_keys(Keys.ENTER)
    time.sleep(2)

    # Locating the ISPs Twitter support account
    user = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/section/div/div/div[3]/div/div/div/div/div[2]/div/div/div/div[1]/a')
    user.click()
    time.sleep(3)

    # Opening up a private conversation
    message_button = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/div[2]/div[2]/div')
    message_button.click()
    time.sleep(2)

    complaint = "Hey, I have been having some issues recently with my internet speeds. My current speeds are {} Mbps down / {} Mbps up, and with my TELUS plan, I have been promised speeds of {} Mbps down / {} Mbps up. Is there any way to resolve this difference?"\
        .format(download, upload, DESIRED_DOWN, DESIRED_UP)

    # Compiling and sending the complaint message
    message_field = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/section[2]/div/div/div[2]/div/div/aside/div[2]/div[2]/div/div/div/div/label/div[1]/div/div/div/div/div[2]/div/div/div/div')
    message_field.click()
    message_field.send_keys(complaint)
    message_field.send_keys(Keys.ENTER)
    time.sleep(3)

    twitter_logout(driver)


# Sending a complaint to the ISP via a public tweet
def send_complaint_tweet(driver, download: int, upload: int, location: str):

    message = "Hello @TELUS, I have recently been having some issues with my internet speeds. My contract promises {} Mbps down / {} Mbps up, however I am only getting {} Mbps down / {} Mbps up currently (in {}). Can you fix this?"\
        .format(DESIRED_DOWN, DESIRED_UP, download, upload, location)

    # Compiling and sending the tweet
    tweet_field = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div[2]/div/div/div/div')
    tweet_field.send_keys(message)
    time.sleep(3)

    submit_button = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]')
    submit_button.click()
    time.sleep(3)


# Retrieving the current upload and download internet speeds (and the user's location)
def get_internet_speeds() -> tuple:

    ookla_driver = webdriver.Chrome(executable_path=chrome_driver_path)
    ookla_driver.get(url=OOKLA_ENDPOINT)
    time.sleep(2)

    curr_server = ookla_driver.find_element(By.CSS_SELECTOR, ".server-current > div:nth-of-type(2) > a").text.strip()
    location = ookla_driver.find_element(By.CSS_SELECTOR, ".server-current > div:nth-of-type(3) > span").get_attribute("innerHTML")

    # Ensuring the server is set to TELUS before the test begins (for more pertinent results)
    if curr_server != "TELUS":

        change_server = ookla_driver.find_element(By.CSS_SELECTOR, ".server-current > div:nth-of-type(4) > a")
        change_server.click()
        time.sleep(2)

        servers = ookla_driver.find_elements(By.CSS_SELECTOR, ".server-hosts > div > ul > li")
        server_names = [server.find_element(By.XPATH, ".//a/span[2]").get_attribute("innerHTML").strip() for server in servers]

        for i in range(len(servers)):

            if server_names[i] == "TELUS":

                servers[i].click()

            i += 1

    # Initiating the speed test
    time.sleep(2)
    start_button = ookla_driver.find_element(By.CSS_SELECTOR, ".start-button > a")
    start_button.click()
    time.sleep(45)

    # Obtaining the relevant results
    results = ookla_driver.find_elements(By.CSS_SELECTOR, ".result-container-data > div > div > div:nth-of-type(2) > span")
    download_speed, upload_speed = results[0].get_attribute("innerHTML").strip(), results[1].get_attribute("innerHTML").strip()

    ookla_driver.stop_client()
    ookla_driver.close()

    return round(float(download_speed)), round(float(upload_speed)), location


# Utilizes the Selenium (Browser Automation) framework to send complaints to an ISP via Twitter if internet speeds are not desirable/sufficient
if __name__ == "__main__":

    # Evaluating internet speeds on a daily basis
    while True:

        time.sleep(86400)

        curr_down, curr_up, my_location = get_internet_speeds()

        # Sends two complaints (one private, one public) to the ISP regarding the poor and insufficient internet speeds
        if curr_down < DESIRED_DOWN - 15 or curr_up < DESIRED_UP - 15:

            twitter_driver = twitter_login(MY_USER, MY_PASS)
            send_complaint_tweet(twitter_driver, curr_down, curr_up, my_location)
            send_direct_complaint(twitter_driver, ISP_NAME, curr_down, curr_up)
