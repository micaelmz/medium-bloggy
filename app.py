import os
import sqlite3
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for, flash,
    redirect, session)
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap
from forms import RegisterForm, LoginForm, CreatePostForm, CommentForm
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["DATABASE"] = os.environ.get("DATABASE")
app.secret_key = os.environ.get("SECRET_KEY")
Bootstrap(app)
ckeditor = CKEditor(app)

def get_db_connection():
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn

def query_db(query, args=(), one=False):
    conn = get_db_connection()
    cur = conn.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    conn.close()
    return (rv[0] if rv else None) if one else rv

def execute_db(query, args=()):
    conn = get_db_connection()
    cur = conn.execute(query, args)
    conn.commit()
    cur.close()
    conn.close()


# ---------------- #
#    APP ROUTES    #
# ---------------- #

# ----- HOME ----- #
@app.route("/")
def get_all_posts():
    '''
    Read all blog posts from the database.
    '''
    posts = query_db('SELECT * FROM blog_posts')
    return render_template("index.html", all_posts=posts)


# ----- REGISTER ----- #
@app.route('/register', methods=["GET", "POST"])
def register():
    '''
    Sign up for a new account.
    '''
    form = RegisterForm()
    if form.validate_on_submit():

        # check if email already exists in database
        existing_user = query_db('SELECT * FROM users WHERE email = ?', [form.email.data], one=True)

        if existing_user:
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        # hash and salt the password
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
        # insert new_user into the database
        execute_db('INSERT INTO users (email, password, name) VALUES (?, ?, ?)',
                   [new_user["email"], new_user["password"], new_user["name"]])

        # put the new user into 'session' cookie
        session["user"] = form.name.data
        flash("Registration Successful")
        return redirect(url_for("profile", username=session["user"]))
    return render_template("register.html", form=form)


# ----- LOGIN ----- #
@app.route('/login', methods=["GET", "POST"])
def login():
    '''
    Login to the site.

    Validation included.
    '''
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # check if email already exists
        existing_user = query_db('SELECT * FROM users WHERE email = ?', [email], one=True)
        # if email doesn't exist or password incorrect
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


# ----- PROFILE PAGE ----- #
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    '''
    Direct the user to their Profile page.

    Retrieve all the users Posts.
    '''
    username = query_db('SELECT * FROM users WHERE name = ?', [session["user"]], one=True)["name"]
    posts = query_db('SELECT * FROM blog_posts WHERE author = ?', [username])
    # if logged in
    if session["user"]:
        return render_template("profile.html", username=username, posts=posts)
    # if not logged in, return to login page
    return redirect(url_for("login"))


# ----- LOGOUT ----- #
@app.route("/logout")
def logout():
    '''
    Logout the user.

    Redirect the user to the home page.
    '''
    session.pop("user")
    return redirect(url_for("get_all_posts"))


# ----- READ A POST BY ITS ID ----- #
@app.route("/post/<post_id>", methods=["GET", "POST"])
def show_post(post_id):
    '''
    Read a Post by Id.

    Allow the user to Comment if logged in.
    '''
    form = CommentForm()
    # find the requested post
    requested_post = query_db('SELECT * FROM blog_posts WHERE id = ?', [post_id], one=True)
    requested_post_comments = query_db('SELECT * FROM blog_comments WHERE parent_post = ?', [post_id])

    # commenting on a post
    if form.validate_on_submit():
        if not session["user"]:
            flash("You need to login or register to comment.")
            return redirect(url_for("login"))

        new_comment = {
            "text": form.comment_text.data,
            "comment_author": session["user"],
            "parent_post": post_id
        }

        execute_db('INSERT INTO blog_comments (text, comment_author, parent_post) VALUES (?, ?, ?)',
                   [new_comment["text"], new_comment["comment_author"], new_comment["parent_post"]])
    return render_template("post.html", post=requested_post,
                           comments=requested_post_comments, form=form)


# ----- CREATE A NEW POST ----- #
@app.route("/create-post", methods=["GET", "POST"])
def create_post():
    '''
    Create a new Post.

    Inject all form data to a new blog post document on submit.
    '''
    if "user" in session:
        # create a Form for data entry
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
            execute_db('INSERT INTO blog_posts (title, subtitle, body, img_url, author, date) VALUES (?, ?, ?, ?, ?, ?)',
                       [new_post["title"], new_post["subtitle"], new_post["body"], new_post["img_url"], new_post["author"], new_post["date"]])
            flash("Post Successfully Added")
            return redirect(url_for("get_all_posts"))
        return render_template("create_post.html", form=form)
    else:
        return redirect(url_for("login"))


# ----- EDIT A POST BY ID ----- #
@app.route("/edit-post/<post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    '''
    Edit a Post by Id.

    Update all Post data on submit.
    '''
    post = query_db('SELECT * FROM blog_posts WHERE id = ?', [post_id], one=True)

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
        execute_db('UPDATE blog_posts SET title = ?, subtitle = ?, img_url = ?, body = ? WHERE id = ?',
                   [post["title"], post["subtitle"], post["img_url"], post["body"], post_id])
        return redirect(url_for("show_post", post_id=post_id))
    return render_template("create_post.html", form=edit_form, is_edit=True)


# ----- DELETE A POST BY ID ----- #
@app.route("/delete/<post_id>")
def delete_post(post_id):
    '''
    Delete a Post by Id.

    Redirect back to main page on submit.
    '''
    execute_db('DELETE FROM blog_posts WHERE id = ?', [post_id])
    flash("Post Successfully Deleted")
    return redirect(url_for('get_all_posts'))


# ----- DELETE A COMMENT BY ID ----- #
@app.route("/delete_comment/<comment_id>")
def delete_comment(comment_id):
    '''
    Delete a Comment by Id.
    '''
    execute_db('DELETE FROM blog_comments WHERE id = ?', [comment_id])
    flash("Comment Successfully Deleted")
    post_id = request.args.get('post_id')
    return redirect(url_for("show_post", post_id=post_id))


# ----- SEARCH FOR A POST BY TITLE, SUBTITLE ----- #
@app.route("/search", methods=["GET", "POST"])
def search():
    '''
    Search for a Post by Title, Subtitle.
    '''
    query = request.form.get("query")
    posts = query_db('SELECT * FROM blog_posts WHERE title LIKE ? OR subtitle LIKE ?', ['%' + query + '%', '%' + query + '%'])
    return render_template("index.html", all_posts=posts)


# ----- HANDLE 404 ERROR ----- #
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# ----- HANDLE 403 ERROR ----- #
@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403


# ----- HANDLE 500 ERROR ----- #
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
