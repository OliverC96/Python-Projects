# Importing relevant modules/libraries
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user
from flask import Flask, render_template, redirect, url_for, request, flash, abort
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_ckeditor import CKEditor
from datetime import datetime as dt
from twilio.rest import Client
from functools import wraps
from flask_gravatar import Gravatar
from dotenv import load_dotenv
import os
import smtplib

# Retrieving environment variables for easy access
load_dotenv()

# Declaring constants (API endpoints, authorization tokens, etc.)
MY_EMAIL = os.getenv("MY_EMAIL")
EMAIL_PASS = os.getenv("EMAIL_PASS")
SERVER_DOMAIN = "smtp.gmail.com"
SERVER_PORT = 587

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")
MY_NUMBER = os.getenv("MY_NUMBER")

# Creating and configuring the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
login_manager = LoginManager()
login_manager.init_app(app)
ckeditor = CKEditor(app)
Bootstrap(app)

# Creating and configuring the associated database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

curr_date = dt.now().strftime('%B %-d, %Y')
curr_year = dt.now().year
comment_date = dt.now().strftime('%Y-%m-%d')

gravatar = Gravatar(
    app=app,
    size=50,
    rating="g",
    default="retro",
    force_default=False,
    force_lower=False,
    use_ssl=False,
    base_url=None
)


# Configuring a form which allows a client to specify the parameters of a new blog post
class CreatePostForm(FlaskForm):

    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


# A table in the database containing information regarding site users/clients
class BlogUser(UserMixin, db.Model):

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    posts = relationship("BlogPost", back_populates="author")
    comments = relationship("Comment", back_populates="comment_author")


# A table in the database containing information regarding each blog post
class BlogPost(db.Model):

    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = relationship("BlogUser", back_populates="posts")
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    comments = relationship("Comment", back_populates="parent_post")


# A table in the database containing information regarding each comment (in response to a blog post)
class Comment(db.Model):

    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    parent_post = relationship("BlogPost", back_populates="comments")
    comment_author = relationship("BlogUser", back_populates="comments")
    text = db.Column(db.Text, nullable=False)
    date_stamp = db.Column(db.Text, nullable=False)


# Defining a user loader method to implement the Flask-Login module
@login_manager.user_loader
def load_user(user_id):

    return BlogUser.query.get(int(user_id))


# A decorator which secures the specified route by providing access only to the admin of the site
def admin_only(f):

    @wraps(f)
    def decorated_func(*args, **kwargs):

        # Returns a 403 Forbidden Access error if the current user is not authorized to access the route
        if current_user.id != 1:

            return abort(403)

        return f(*args, **kwargs)

    return decorated_func


# Homepage
@app.route('/')
def get_all_posts():

    posts = BlogPost.query.all()

    return render_template("index.html", all_posts=posts, year=curr_year)


# Renders the specified blog post, and its corresponding comments
@app.route("/post/<int:index>", methods=["GET", "POST"])
def show_post(index):

    requested_post = BlogPost.query.get(index)

    if request.method == "POST":

        # Authenticated user
        if current_user.is_authenticated:

            new_comment = Comment(
                text=request.form.get("comment"),
                comment_author=current_user,
                parent_post=requested_post,
                date_stamp=comment_date
            )

            db.session.add(new_comment)
            db.session.commit()

            return redirect(url_for("show_post", index=index))

        # User not authenticated - redirects user to the login route
        else:

            flash("Please login to make a comment on this blog post.")

            return redirect(url_for("login"))

    return render_template("post.html", post=requested_post, year=curr_year)


# Allows a new user to register an account with the application
@app.route('/register', methods=["GET", "POST"])
def register_user():

    if request.method == "POST":

        user_email = request.form.get("email")
        user = BlogUser.query.filter_by(email=user_email).first()

        # Email already exists in the database - redirects user to the login route
        if user:

            flash("Account with that email already exists - login here instead")

            return redirect(url_for("login"))

        else:

            # Generates a secure password (salts and hashes the entered password)
            secure_pass = generate_password_hash(
                password=request.form.get("password"),
                method="pbkdf2:sha256",
                salt_length=8
            )

            new_user = BlogUser(
                name=request.form.get("name"),
                email=user_email,
                password=secure_pass,
            )

            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)

            return redirect(url_for("get_all_posts"))

    return render_template("register.html")


# Allows a returning/existing user to log in to the application
@app.route('/login', methods=["GET", "POST"])
def login():

    if request.method == "POST":

        user_email = request.form.get("email")
        password = request.form.get("password")
        user = BlogUser.query.filter_by(email=user_email).first()

        if user:

            # Password matches the one stored in the database
            if check_password_hash(user.password, password):

                # Authenticates user
                login_user(user)

                return redirect(url_for("get_all_posts"))

            # Incorrect password
            else:

                flash("Incorrect password - please try again")

                return redirect(url_for("login"))

        # Invalid email address - redirects user to the register route
        else:

            flash("No account found with that email - register here instead")

            return redirect(url_for("register_user"))

    return render_template("login.html")


# Allows the admin to create a new blog post, and add it to the database
@admin_only
@app.route('/new-post', methods=["GET", "POST"])
def create_post():

    post_form = CreatePostForm()

    if post_form.validate_on_submit():

        new_post = BlogPost(
            title=request.form.get("title"),
            subtitle=request.form.get("subtitle"),
            body=request.form.get("body"),
            author=current_user,
            img_url=request.form.get("img_url"),
            date=curr_date
        )

        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for("get_all_posts"))

    return render_template("make-post.html", form=post_form, page_header="Create New Post")


# Allows the admin to edit fields of an existing blog post in the database (specified by the post_id parameter)
@admin_only
@app.route("/edit-post/<post_id>", methods=["GET", "POST"])
def edit_post(post_id):

    selected_post = BlogPost.query.get(post_id)

    # Renders the new blog post form pre-populated with the current values stored in the database
    edit_form = CreatePostForm(
        title=selected_post.title,
        subtitle=selected_post.subtitle,
        img_url=selected_post.img_url,
        body=selected_post.body,
        author=current_user.name,
    )

    if edit_form.validate_on_submit():

        selected_post.title = request.form.get("title")
        selected_post.subtitle = request.form.get("subtitle")
        selected_post.img_url = request.form.get("img_url")
        selected_post.body = request.form.get("body")

        db.session.commit()

        return redirect(url_for("show_post", index=post_id))

    return render_template("make-post.html", form=edit_form, page_header="Edit Post")


# Removes the specified post from the database (only the admin can delete a post)
@admin_only
@app.route('/delete-post/<int:post_id>')
def delete_post(post_id):

    selected_post = BlogPost.query.get(post_id)
    db.session.delete(selected_post)
    db.session.commit()

    return redirect(url_for("get_all_posts"))


# Removes the specified comment from the database (admin can delete any comment, user can only delete their own comments)
@admin_only
@app.route('/delete-comment/<int:post_id>/<int:comment_id>')
def delete_comment(comment_id, post_id):

    selected_comment = Comment.query.filter_by(id=comment_id).first()
    db.session.delete(selected_comment)
    db.session.commit()

    return redirect(url_for("show_post", index=post_id))


# About section
@app.route("/about")
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


# Contact section (containing a functional contact form)
@app.route('/contact', methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        email = request.form["email"]
        body = request.form["message"]

        send_email(email, body)
        send_sms(body)

    return render_template("contact.html", year=curr_year, method=request.method)


# Logs out the user, and redirects to the homepage route
@app.route('/logout')
def logout():

    logout_user()

    return redirect(url_for("get_all_posts"))


# Runs a functional blog application implementing Flask-Bootstrap, Flask-Login, Flask-WTF, Flask-SQLAlchemy and Werkzeug
if __name__ == "__main__":

    app.run(port=3900)
