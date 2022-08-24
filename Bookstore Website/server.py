# Importing relevant modules
from flask import Flask, render_template
from datetime import datetime as dt


# Creating a Flask application
app = Flask(__name__)


# Rendering the HTML (and CSS) code on the Flask development server
@app.route('/')
def home():

    year = dt.now().year

    return render_template("index.html", curr_year=year)


if __name__ == "__main__":

    # Running in debug mode to allow for continuous page refreshing, and detection of any errors that may arise
    app.run(debug=True)
