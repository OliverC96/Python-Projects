# Importing relevant modules and libraries
from flask import Flask, render_template, request
from datetime import datetime as dt
import requests
import json
import smtplib
from twilio.rest import Client
import os

# Declaring constants (API endpoints, authorization tokens, etc.)
DATA_ENDPOINT = "https://api.npoint.io/718381b611359a39567f"

MY_EMAIL = os.environ["MY_EMAIL"]
EMAIL_PASS = os.environ["EMAIL_PASS"]
SERVER_DOMAIN = "smtp.gmail.com"
SERVER_PORT = 587

TWILIO_SID = os.environ["TWILIO_SID"]
TWILIO_AUTH = os.environ["TWILIO_TOKEN"]
TWILIO_NUMBER = os.environ["TWILIO_NUMBER"]
MY_NUMBER = os.environ["MY_NUMBER"]

# Creating a Flask application
app = Flask(__name__)

# Retrieving the blog data contained in the json located at the given endpoint
response = requests.get(url=DATA_ENDPOINT)
response.raise_for_status()
blog_data = json.loads(response.text)

curr_year = dt.now().year


# Homepage
@app.route('/')
def home():

    return render_template("index.html", data=blog_data, year=curr_year)


# About section
@app.route('/about')
def about():

    return render_template("about.html", year=curr_year)


# Sends an email to the site owner containing the message from the contact form (via the SMTP library)
def send_email(from_email: str, msg_body: str):

    with smtplib.SMTP(SERVER_DOMAIN, SERVER_PORT) as connection:

        connection.ehlo()
        connection.starttls()
        connection.login(user=from_email, password=EMAIL_PASS)
        connection.sendmail(
            to_addrs=MY_EMAIL,
            from_addr=from_email,
            msg=msg_body
        )


# Sends an SMS message to the site owner containing the message from the contact form (via the Twilio API)
def send_sms(msg_body: str):

    twilio_client = Client(TWILIO_SID, TWILIO_AUTH)
    twilio_client.messages \
        .create(
            to=MY_NUMBER,
            from_=TWILIO_NUMBER,
            body=msg_body
        )


# Contact section (containing the functional contact form)
@app.route('/contact', methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        email = request.form["email"]
        body = request.form["message"]

        send_email(email, body)
        send_sms(body)

    return render_template("contact.html", year=curr_year, method=request.method)


# Retrieves the image reference corresponding to the specified post
def get_post_image(post_id: int) -> str:

    if post_id == 1:

        return 'assets/img/cacti2.jpg'

    elif post_id == 2:

        return 'assets/img/boredom2.jpg'

    else:

        return 'assets/img/fasting2.jpg'


# Post section
@app.route('/post/<int:article_num>')
def post(article_num):

    for blog_post in blog_data:

        if blog_post["id"] == article_num:

            return render_template("post.html", year=curr_year, post=blog_post, img_ref=get_post_image(article_num))


# Renders a sample blog website, including a functional contact form that notifies the site owner via email and SMS
if __name__ == "__main__":

    app.run(debug=True, port=3000)
