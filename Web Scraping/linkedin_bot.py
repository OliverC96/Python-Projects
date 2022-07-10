# Importing relevant modules/libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os

# Declaring constants
LINKEDIN_MAIN = "https://ca.linkedin.com/"
MY_EMAIL = os.environ["ALT_EMAIL"]
MY_PASS = os.environ["LNKDN_PASS"]
MY_PHONE = os.environ["MY_NUMBER"]
DESIRED_JOB = "python developer"
DESIRED_LOCATION = "Calgary"
FILTERS = ["Past Month", "Internship", "Entry level", "Remote", "Software Engineer", "Python Developer", "Java Software Engineer", "$40,000+"]

# Initializing a chrome web driver object
chrome_driver_path = "chromedriver"
driver = webdriver.Chrome(executable_path=chrome_driver_path)
driver.get(LINKEDIN_MAIN)


# Logging in to the LinkedIn account associated with the given username(email) and password
def login(user_name: str, user_pass: str):

    username_entry = driver.find_element(By.ID, "session_key")
    username_entry.send_keys(user_name)
    password_entry = driver.find_element(By.ID, "session_password")
    password_entry.send_keys(user_pass)
    password_entry.send_keys(Keys.ENTER)

    # Dismissing the messages tab to enable visibility of nearby html elements
    time.sleep(10)
    dismiss_messages = driver.find_element(By.CSS_SELECTOR, ".application-outlet > aside > div:nth-of-type(1) > header > div:nth-of-type(3) > button:nth-of-type(2)")
    dismiss_messages.click()


# A quick/basic search for jobs with the given title/role and location
def search_jobs(job_title: str, job_location: str):

    time.sleep(2)
    jobs_tab = driver.find_element(By.CSS_SELECTOR, ".global-nav__nav > ul > li:nth-of-type(3)")
    jobs_tab.click()

    time.sleep(2)
    search_fields = driver.find_elements(By.CSS_SELECTOR, ".relative > input")
    keyword_search = search_fields[0]
    keyword_search.send_keys(job_title)

    time.sleep(2)
    location_search = search_fields[3]
    location_search.send_keys(job_location)

    time.sleep(2)
    keyword_search.send_keys(Keys.ENTER)

    time.sleep(2)
    job_filters = driver.find_element(By.CSS_SELECTOR, ".job-search-ext > section > div > div > div > div > div > button")
    job_filters.click()


# A more specific/comprehensive search via the given list of filters/preferences (returns a list of the matching job results)
def filter_jobs(desired_filters: list) -> list:

    time.sleep(2)
    filter_root = driver.find_element(By.CSS_SELECTOR, "#artdeco-modal-outlet > div > div > div:nth-of-type(2) > ul")
    filter_containers = filter_root.find_elements(By.XPATH, ".//li/fieldset/div/ul/li/label")
    easy_apply_filter = filter_root.find_element(By.XPATH, ".//li[7]/fieldset/div")
    filter_options = [container.find_element(By.XPATH, ".//p/span[1]") for container in filter_containers]
    filter_texts = [option.get_attribute("innerHTML").strip() for option in filter_options]

    for i in range(len(filter_containers)):

        curr_option = filter_containers[i]
        curr_text = filter_texts[i]

        if curr_text in desired_filters:

            curr_option.click()

    easy_apply_filter.click()

    time.sleep(2)
    submit_filters = driver.find_element(By.CSS_SELECTOR, "#artdeco-modal-outlet > div > div > div:nth-of-type(3) > div > button:nth-of-type(2)")
    submit_filters.click()

    # Selecting the last job result container to enable visibility of the jobs positioned lower on the page (for future reference)
    time.sleep(2)
    results_root = driver.find_element(By.CSS_SELECTOR, ".jobs-search-two-pane__wrapper > div > section:nth-of-type(1) > div > div > ul")
    bottom_item = results_root.find_element(By.XPATH, "(.//li)[last()]")
    bottom_item.click()

    time.sleep(1)
    results = results_root.find_elements(By.XPATH, ".//li/div/div[1]/div[1]/div[2]/div[1]/a")

    return results


# Dismissing the update window that arises after saving or following a new job (to enable visibility of nearby html elements)
def dismiss_update():

    time.sleep(2)
    curr_update = driver.find_element(By.CSS_SELECTOR, "#artdeco-toasts__wormhole > section > div > div > button")
    curr_update.click()


# Following a company if they have not already been followed
def follow_company(root_container):

    # Selecting the right panel, and scrolling to the bottom of the page to enable visibility of the "Follow" button
    time.sleep(2)
    right_panel = root_container.find_element(By.XPATH, ".//div[4]")
    right_panel.click()
    html_tag = driver.find_element(By.TAG_NAME, "html")
    html_tag.send_keys(Keys.END)
    time.sleep(1)

    follow_button = root_container.find_element(By.XPATH, ".//div[last()]/section/section/div[1]/div[1]/button")
    follow_status = follow_button.find_element(By.XPATH, ".//span").get_attribute("innerHTML").strip()

    if follow_status != "Following":

        follow_button.click()
        dismiss_update()


# Saving a job if it has not already been saved
def save_jobs(job_results: list):

    right_root = driver.find_element(By.CSS_SELECTOR, ".jobs-search-two-pane__wrapper > div > section:nth-of-type(2) > div > div > div:nth-of-type(1) > div")

    for job in job_results:

        job.click()
        time.sleep(1)

        save_button = right_root.find_element(By.XPATH, ".//div[1]/div/div[1]/div[1]/div[3]/div/button")
        save_status = save_button.find_element(By.XPATH, ".//span[1]").get_attribute("innerHTML").strip()

        if save_status != "Saved":

            save_button.click()
            dismiss_update()

        follow_company(right_root)


# Applying for "Easy Apply" jobs using only the given phone number
def easy_apply(job_results: list, phone_number: str):

    # Selecting the first job result container to redirect the user to the top of the page before applying for jobs
    top_item = job_results[0]
    top_item.click()
    time.sleep(2)

    apply_root = driver.find_element(By.CSS_SELECTOR, ".jobs-search-two-pane__wrapper > div > section:nth-of-type(2) > div > div > div:nth-of-type(1) > div")

    for job in job_results:

        job.click()
        time.sleep(2)

        apply_button = apply_root.find_element(By.XPATH, ".//div[1]/div/div[1]/div[1]/div[3]/div/div/div/button")
        apply_button.click()

        time.sleep(2)
        phone_entry = driver.find_element(By.CSS_SELECTOR, ".jobs-easy-apply-content > div:nth-of-type(2) > form > div > div > div:nth-of-type(3) > div:nth-of-type(2) > div > div > input")
        phone_entry.send_keys(phone_number)
        phone_entry.send_keys(Keys.ENTER)


# Utilizes the Selenium (Browser Automation) framework to automatically search for desirable jobs, and save/follow/apply for them (depending on the user's preferences)
if __name__ == "__main__":

    login(MY_EMAIL, MY_PASS)
    search_jobs(DESIRED_JOB, DESIRED_LOCATION)
    matching_jobs = filter_jobs(FILTERS)
    save_jobs(matching_jobs)
    easy_apply(matching_jobs, MY_PHONE)

    # Terminates the Selenium web driver client, and closes the remaining browser window
    driver.stop_client()
    driver.close()
