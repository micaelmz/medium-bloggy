import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for, flash,
    redirect, session)
from flask_pymongo import PyMongo
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap
from bson.objectid import ObjectId
from forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")
Bootstrap(app)
ckeditor = CKEditor(app)
mongo = PyMongo(app)


@app.route("/")
def get_all_posts():
    posts = mongo.db.blog_posts.find()
    return render_template("index.html", all_posts=posts)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # check if username already exists in database
        existing_user = mongo.db.users.find_one(
            {"email": form.email.data})

        if existing_user:
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = {
            "email": form.email.data,
            "password": hash_and_salted_password,
            "name": form.name.data
        }
        # insert user into database
        mongo.db.users.insert_one(new_user)

        # put the new user into 'session' cookie
        session["user"] = form.email.data
        flash("Registration Successful")
        return redirect(url_for("profile", username=session["user"]))
    return render_template("register.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # check if username already exists
        existing_user = mongo.db.users.find_one({"email": email})
        # Email doesn't exist or password incorrect.
        if not existing_user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(existing_user["password"], password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            session["user"] = email
            flash(f"Welcome, {existing_user['email']}")
            return redirect(
                url_for("profile", username=session["user"]))
    return render_template("login.html", form=form)


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    username = mongo.db.users.find_one(
        {"email": session["user"]})["email"]
    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("get_all_posts"))


@app.route("/post/<post_id>", methods=["GET", "POST"])
def show_post(post_id):
    requested_post = mongo.db.blog_posts.find_one({"_id": ObjectId(post_id)})
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)

    # app.run(debug=True)
