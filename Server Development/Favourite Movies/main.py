# Importing relevant modules and libraries
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired
import requests
import os


# Declaring constants (API keys, endpoints, and headers)
TMDB_KEY = os.environ["TMDB_KEY"]
TMDB_TOKEN = os.environ["TMDB_TOKEN"]
TMDB_ENDPOINT = "https://api.themoviedb.org/3"
IMG_ENDPOINT = "https://image.tmdb.org/t/p/w500"
TMDB_HEADERS = {
    "Authorization": "Bearer {}".format(TMDB_TOKEN),
    "Content-Type": "application/json"
}

# Creating a Flask application with a corresponding database (via SQAlchemy)
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ["MOVIE_SECRET"]
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)
db = SQLAlchemy(app)


# Configuring a form which allows a client to rate and review a movie on the list
class RateMovieForm(FlaskForm):

    new_rating = FloatField(label="Your Rating: ", validators=[DataRequired()])
    new_review = StringField(label="Your Review: ", validators=[DataRequired()])
    submit = SubmitField(label="Submit")


# Configuring a form which allows a client to add a new movie to the list
class AddMovieForm(FlaskForm):

    movie_title = StringField(label="Movie Title", validators=[DataRequired()])
    submit = SubmitField(label="Add Movie")


# Configuring the attributes of each entry in the database (and their allowable types/formats)
class Movie(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False, unique=True)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String, nullable=True)
    img_url = db.Column(db.String, nullable=False, unique=True)

# Initiating the database
db.create_all()


# Homepage, which displays the list of favourite movies
@app.route("/")
def home():

    # Orders the movies by their ratings (lowest to highest), and adjusts their rankings accordingly
    all_movies = db.session.query(Movie).order_by("rating")
    rankings = [i + 1 for i in range(all_movies.count())][::-1]

    for i in range(all_movies.count()):

        all_movies[i].ranking = rankings[i]
        db.session.commit()

    return render_template("index.html", movies=all_movies)


# Retrieves detailed information regarding the movie selected by the client
@app.route("/find")
def find_movie():

    movie_id = request.args.get("id")

    query_params = {
        "api_key": TMDB_KEY,
    }

    # Retrieves the details of the movie associated with the given id via a GET request to the TMDB API
    response = requests.get(url=TMDB_ENDPOINT + "/movie/{}".format(movie_id), params=query_params, headers=TMDB_HEADERS)
    response.raise_for_status()
    movie_data = response.json()

    # Instantiating a new Movie object with the information contained within the search data
    new_movie = Movie(
        title=movie_data["title"],
        img_url=IMG_ENDPOINT + movie_data["poster_path"],
        year=movie_data["release_date"][:4],
        description=movie_data["overview"],
    )

    # Adding the new movie to the database
    db.session.add(new_movie)
    db.session.commit()

    return redirect(url_for('home'))


# Allows a client to add a new movie to the list of favourites
@app.route('/add', methods=["GET", "POST"])
def add_movie():

    add_form = AddMovieForm()

    if add_form.validate_on_submit():

        movie_name = add_form.movie_title.data

        query_params = {
            "api_key": TMDB_KEY,
            "query": movie_name
        }

        # Searches for movies containing the given keyword via a GET request to the TMDB API
        response = requests.get(url=TMDB_ENDPOINT + '/search/movie', headers=TMDB_HEADERS, params=query_params)
        response.raise_for_status()
        results = response.json()["results"]

        # Presents the results to the client, and guides them to pick one to add to the list
        return render_template("select.html", movies=results)

    return render_template("add.html", form=add_form)


# Allows a client to alter/update a movie's rating and review fields
@app.route('/edit', methods=["GET", "POST"])
def rate_movie():

    # Identifies the movie to be updated
    movie_id = request.args.get("id")
    selected_movie = Movie.query.get(movie_id)
    rating_form = RateMovieForm()

    if rating_form.validate_on_submit():

        # Updates the rating and review fields with the appropriate (new) data
        selected_movie.rating = rating_form.new_rating.data
        selected_movie.review = rating_form.new_review.data
        db.session.commit()

        return redirect(url_for('home'))

    return render_template("edit.html", movie=selected_movie, form=rating_form)


# Allows a client to remove a movie from the list of favourites
@app.route('/delete')
def delete_movie():

    # Identifies the movie to be removed, and then deletes it from the database
    movie_id = request.args.get("id")
    selected_movie = Movie.query.get(movie_id)
    db.session.delete(selected_movie)
    db.session.commit()

    return redirect(url_for("home"))


# Runs an application which allows a client to configure a list of their favourite movies.
# Utilizes Flask, Flask-WTF, Flask-Bootstrap, and Flask-SQAlchemy
if __name__ == '__main__':

    app.run(debug=True, port=2500)
