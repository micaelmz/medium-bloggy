import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for, flash,
    redirect, session)
from flask_pymongo import PyMongo
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap
from bson.objectid import ObjectId
from forms import RegisterForm
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
            # User already exists
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

        mongo.db.users.insert_one(new_user)

        # put the new user into 'session' cookie
        session["user"] = form.email.data
        flash("Registration Successful")
        # login_user(new_user)
        return redirect(url_for("profile", username=session["user"]))
    return render_template("register.html", form=form)


# tell our app how and where to run our application
if __name__ == "__main__":
    app.run(debug=True)
