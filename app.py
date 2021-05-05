import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for, flash,
    redirect, session)
from flask_pymongo import PyMongo
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap
from bson.objectid import ObjectId
from forms import RegisterForm, LoginForm, CreatePostForm, CommentForm
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
    posts = list(mongo.db.blog_posts.find())
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
        session["user"] = form.name.data
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
            flash("That email or password does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(existing_user["password"], password):
            flash('That email and password dont match, please try again.')
            return redirect(url_for('login'))
        else:
            session["user"] = existing_user['name']
            flash(f"Welcome Back, {existing_user['name'].capitalize()}")
            return redirect(
                url_for("profile", username=session["user"]))
    return render_template("login.html", form=form)


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    username = mongo.db.users.find_one(
        {"name": session["user"]})["name"]
    posts = mongo.db.blog_posts.find({"author": username })
    # if logged in
    if session["user"]:
        return render_template("profile.html", username=username, posts=posts)
    # if not logged in, return to login page
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("user")
    return redirect(url_for("get_all_posts"))


@app.route("/post/<post_id>", methods=["GET", "POST"])
def show_post(post_id):
    form = CommentForm()
    requested_post = mongo.db.blog_posts.find_one({"_id": ObjectId(post_id)})
    requested_post_comments = mongo.db.blog_comments.find({"parent_post": ObjectId(post_id)})

    if form.validate_on_submit():
        if not session["user"]:
            flash("You need to login or register to comment.")
            return redirect(url_for("login"))

        new_comment = {
            "text": form.comment_text.data,
            "comment_author": session["user"],
            "parent_post": ObjectId(post_id)
        }

        mongo.db.blog_comments.insert_one(new_comment)
    return render_template("post.html", post=requested_post, comments=requested_post_comments, form=form)


@app.route("/create-post", methods=["GET", "POST"])
def create_post():
    if "user" in session:
        form = CreatePostForm()
        if form.validate_on_submit():
            new_post = {
                "title": form.title.data,
                "subtitle": form.subtitle.data,
                "body": form.body.data,
                "img_url": form.img_url.data,
                "author": session["user"],
                "date": date.today().strftime("%B %d, %Y")
            }
            mongo.db.blog_posts.insert_one(new_post)
            flash("Post Successfully Added")
            return redirect(url_for("get_all_posts"))
        return render_template("create_post.html", form=form)
    else:
        return redirect(url_for("login"))


@app.route("/edit-post/<post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = mongo.db.blog_posts.find_one({"_id": ObjectId(post_id)})

    edit_form = CreatePostForm(
        title=post["title"],
        subtitle=post["subtitle"],
        img_url=post["img_url"],
        author=session["user"],
        body=post["body"]
    )
    if edit_form.validate_on_submit():
        post["title"] = edit_form.title.data
        post["subtitle"] = edit_form.subtitle.data
        post["img_url"] = edit_form.img_url.data
        post["body"] = edit_form.body.data
        mongo.db.blog_posts.update({"_id": ObjectId(post_id)}, post)
        return redirect(url_for("show_post", post_id=post_id))
    return render_template("create_post.html", form=edit_form, is_edit=True)


@app.route("/delete/<post_id>")
def delete_post(post_id):
    mongo.db.blog_posts.remove({"_id": ObjectId(post_id)})
    flash("Post Successfully Deleted")
    return redirect(url_for('get_all_posts'))


@app.route("/delete_comment/<comment_id>")
def delete_comment(comment_id):
    mongo.db.blog_comments.remove({"_id": ObjectId(comment_id)})
    flash("Comment Successfully Deleted")
    post_id = request.args.get('post_id')
    return redirect(url_for("show_post", post_id=post_id))


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    posts = list(mongo.db.blog_posts.find({"$text": {"$search": query}}))
    return render_template("index.html", all_posts=posts)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)

    # app.run(debug=True)
