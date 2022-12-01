"""Feedback Application - Authorization/Authen/Bcrypt"""

from flask import Flask, redirect, session, render_template
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized

from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, DeleteForm, FeedbackForm

# initialize flask app instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///flask-feedback"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secretkey123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)

db.create_all()

@app.route("/")
def home():
    """Home redirects to register page"""
    return redirect("/register")


@app.errorhandler(404)
def not_found(error):
    """404 page"""
    return render_template('404.html'), 404


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register user: displays a form for registering and deals w the form submission"""
    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        user = User.register(username, password, first_name, last_name, email)

        db.session.commit()
        session['username'] = user.username

        return redirect(f"/users/{user.username}")

    else:
        return render_template('users/register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Display/render login form and handle submission"""
    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Invalid username or password. Try again."]
            return render_template("users/login.html", form=form)

    return render_template("users/login.html", form=form)


@app.route("/logout")
def logout():
    """Route for logging out"""
    session.pop("username")
    return redirect("/login")


@app.route("/users/<username>")
def display_user(username):
    """route to display user page"""
    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    form = DeleteForm()

    return render_template("users/display-user.html", user=user, form=form)


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """delete a user and redirect to login page"""
    if "username" not in session or username != session['username']:
        raise Unathorized()

    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")
    return redirect("/login")

# feedback routes!
@app.route("/users/<username>/feedback/new", methods=["GET", "POST"])
def create_feedback(username):
    """Display form for adding new feedback and handle submission"""
    if "username" not in session or username != session['username']:
        raise Unauthorized()

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(
            title=title,
            content=content,
            username=username,
        )

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    else:
        return render_template("feedback/new-feedback.html", form=form)


@app.route("/feedback/<int:feedback_id>/edit", methods=["GET", "POST"])
def edit_feedback(feedback_id):
    """Display the update feedback form and handle submission"""
    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    return render_template("/feedback/edit-feedback.html", form=form, feedback=feedback)


@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Handle submission of delete form and delete feedback"""
    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")