# Importing relevant modules/libraries
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, SelectField
from wtforms.validators import DataRequired, URL
import csv

# Creating a Flask application and configuring a secret key for the flask_wtf form
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

# Declaring constants
COFFEE = '☕'
POWER = '🔌'
WIFI = '💪'
NA = '✘'

all_choices = [[NA], [NA], [NA]]

for i in range(1, 6):

    all_choices[0].append(COFFEE * i)
    all_choices[1].append(WIFI * i)
    all_choices[2].append(POWER * i)


class CafeForm(FlaskForm):

    name = StringField(label='Cafe Name: ', validators=[DataRequired()])
    location = URLField(label="Cafe Location on Google Maps (URL): ", validators=[DataRequired(), URL()])
    opening_time = StringField(label="Cafe Opening Time (e.g. 8:00AM): ", validators=[DataRequired()])
    closing_time = StringField(label="Cafe Closing Time (e.g. 5:30PM): ", validators=[DataRequired()])
    coffee_rating = SelectField(label="Coffee Rating: ", validators=[DataRequired()], choices=all_choices[0])
    wifi_strength = SelectField(label="Wifi Strength: ", validators=[DataRequired()], choices=all_choices[1])
    power_availability = SelectField(label="Power Socket Availability: ", validators=[DataRequired()], choices=all_choices[2])
    submit = SubmitField(label='Submit')


# Homepage
@app.route("/")
def home():

    return render_template("index.html")


# Displays a form where one can add a new cafe to the database
@app.route('/add', methods=["GET", "POST"])
def add_cafe():

    form = CafeForm()

    if form.validate_on_submit():

        cafe_data = [form.name.data, form.location.data, form.opening_time.data, form.closing_time.data, form.coffee_rating.data, form.wifi_strength.data, form.power_availability.data]

        with open('cafe-data.csv', 'a', newline='') as csv_file:

            writer = csv.writer(csv_file)
            writer.writerow(cafe_data)

        return redirect(url_for('cafes'))

    return render_template('add.html', form=form)


# Displays an up-to-date table containing the cafes and their respective ratings
@app.route('/cafes')
def cafes():

    with open('cafe-data.csv', 'r', newline='') as csv_file:

        csv_data = csv.reader(csv_file, delimiter=',')
        all_cafes = [row for row in csv_data]

    return render_template('cafes.html', cafes=all_cafes)


# Removes an existing cafe from the database
@app.route('/cafes/delete/<cafe_name>')
def delete_cafe(cafe_name):

    with open('cafe-data.csv', 'r', newline='') as curr_csv:

        csv_data = csv.reader(curr_csv, delimiter=',')
        curr_cafes = [row for row in csv_data]

        with open('cafe-data.csv', 'w', newline='') as new_csv:

            writer = csv.writer(new_csv)

            for cafe in curr_cafes:

                if cafe[0] != cafe_name:

                    writer.writerow(cafe)

    return redirect(url_for('cafes'))


# Runs an application that allows one to view nearby cafes and important information pertaining to them, such as their
# daily hours, location, and availability of wifi and power outlets. Built using Flask, Flask-Bootstrap, and Flask-WTF.
if __name__ == '__main__':

    app.run(debug=True, port=2000)
