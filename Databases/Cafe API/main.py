# Importing relevant modules and libraries
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random
from datetime import datetime as dt

# Creating a Flask application, and a corresponding database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Configuring the parameters/columns of entries in the database, and their allowable types/formats
class Cafe(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    # Helper method that creates a dictionary mapping column names (parameters) with their current data (attributes)
    def convert_to_dict(self):

        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


# Initializes the database
db.create_all()


# Homepage
@app.route("/")
def home():

    curr_year = dt.now().year

    return render_template("index.html", year=curr_year)
    

# Returns a random cafe from the database
@app.route("/random", methods=["GET"])
def random_cafe():

    cafes = db.session.query(Cafe).all()
    rand_cafe = random.choice(cafes)

    return jsonify(cafe=rand_cafe.convert_to_dict())


# Returns all cafes in the database
@app.route('/all', methods=["GET"])
def all_cafes():

    cafes = db.session.query(Cafe).all()
    info = [cafe.convert_to_dict() for cafe in cafes]

    return jsonify(cafes=info)


# Returns the cafe(s) matching the queried location
@app.route('/search', methods=["GET"])
def cafe_search():

    cafe_location = request.args.get("loc")
    matching_cafes = db.session.query(Cafe).filter_by(location=cafe_location)
    info = [cafe.convert_to_dict() for cafe in matching_cafes]
    search_error = {
        "Not Found": "Sorry, we don't have a cafe at that location."
    }

    if len(info) == 0:

        return jsonify(error=search_error), 404

    else:

        return jsonify(cafes=info), 200


# Adds a new cafe into the database
@app.route('/add', methods=["POST"])
def add_cafe():

    new_cafe = Cafe(
        name=request.form["name"],
        map_url=request.form["map_url"],
        location=request.form["location"],
        coffee_price=request.form["coffee_price"],
        img_url=request.form["img_url"],
        id=request.form["id"],
        seats=request.form["seats"],
        can_take_calls=bool(int(request.form["can_take_calls"])),
        has_sockets=bool(int(request.form["has_sockets"])),
        has_toilet=bool(int(request.form["has_toilet"])),
        has_wifi=bool(int(request.form["has_wifi"]))
    )

    db.session.add(new_cafe)
    db.session.commit()

    add_response = {
        "success": "Successfully added the new Cafe!"
    }

    return jsonify(response=add_response), 200


# Updates the coffee price attribute of a current cafe in the database
@app.route('/update-price/<cafe_id>', methods=["PATCH"])
def update_price(cafe_id):

    selected_cafe = Cafe.query.get(cafe_id)
    new_price = request.args.get("new_price")

    success_response = {
        "success": "Successfully updated the price!"
    }
    error_response = {
        "Not Found": "Unable to find a cafe in the database associated with the given id."
    }

    if selected_cafe:

        selected_cafe.coffee_price = new_price
        db.session.commit()

        return success_response, 200

    else:

        return jsonify(error=error_response), 404


# Removes an existing cafe from the database (authentication required)
@app.route('/report-closed/<cafe_id>', methods=["DELETE"])
def report_closed(cafe_id):

    required_key = "TopSecretKey"
    request_key = request.args.get("api_key")

    success = {
        "success": "Successfully removed the cafe from the database."
    }
    invalid_key = {
        "Forbidden": "Request not processed - invalid api key"
    }
    not_found = {
        "Not Found": "Unable to find a cafe in the database associated with the given id."
    }

    if request_key != required_key:

        return jsonify(error=invalid_key), 403

    else:

        selected_cafe = Cafe.query.get(cafe_id)

        if selected_cafe:

            db.session.delete(selected_cafe)
            db.session.commit()

            return jsonify(response=success), 200

        else:

            return jsonify(error=not_found), 404


# A RESTful API that allows a client to add, edit, delete, or view cafes stored in a database.
# The database (created via SQAlchemy) contains detailed information regarding each cafe.
if __name__ == '__main__':

    app.run(debug=True, port=2300)
