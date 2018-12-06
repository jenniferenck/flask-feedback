"""Example flask app that stores passwords hashed with Bcrypt. Yay!"""

from flask import Flask, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres:///feedback"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)


@app.route('/')
def redirect_user():
    """Sends user to register page"""

    # check session to see if user is already logged in

    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Show a form to register and create new user"""

    # generates the form from forms.py
    form = RegisterForm()

    # checks for valid info in the form
    if form.validate_on_submit():
        # creating instance of new user
        # shortcut for collecting form data on each field (e.g. username, email, fn, ln)
        form_data = form.data.copy()
        form_data.pop('csrf_token', None)
        user = User.register(**form_data)

        # need to add register method for registering a new user

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            # in case we violate the unique constraint
            form.username.errors = ["Username already exists."]
            return render_template("register.html", form=form)

        session["username"] = user.username

        return redirect(f"/users/{user.username}")

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Show login form that when submitted shows the secret page"""

    form = LoginForm()

    if form.validate_on_submit():
        # shortcut for collecting form data on each field (e.g. username, email, fn, ln)
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username
            return redirect(f'/users/{username}')
        else:
            # re-render the login page with an error
            form.username.errors = [
                'The username/password combination you entered was incorrect'
            ]
            return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)


@app.route('/users/<username>')
def profile(username):
    """Check session if user is logged in then render template, otherwise redirect to login"""

    # session['username']:
    if 'username' not in session:
        raise Unauthorized("Sorry, you're not logged in yet")
        # redirect('login.html')
    else:
        user = User.query.filter_by(username=username).first()
        feedbacks = Feedback.query.filter_by(username=username).all()
        return render_template(
            'user_profile.html', user=user, feedbacks=feedbacks)


@app.route('/logout')
def logout_user():
    """Log user out and clear session when logout button is selected"""

    session.clear()

    return redirect('/')


@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    """When delete user is selected, remove user and children posts from DB"""

    if session['username'] != username:
        raise Unauthorized("Sorry, you're not authorized to do that!")
        # redirect('login.html')
    else:
        user = User.query.filter_by(username=username).first()

        db.session.delete(user)
        db.session.commit()
        return redirect('/')


############ FEEDBACK ###########################


@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    """Show feedback form that when submitted adds feedback with username also collected"""

    if session['username'] != username:
        raise Unauthorized("Sorry, you're not authorized to do that!")
        # redirect('login.html')
    else:
        form = FeedbackForm()

        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data

            feedback = Feedback(
                title=title, content=content, username=username)
            db.session.add(feedback)
            db.session.commit()
            return redirect(f'/users/{username}')
        else:
            return render_template(
                'add_feedback.html', form=form, action='Add')


@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    """Display feedback form and commit changes to DB"""

    feedback = Feedback.query.get_or_404(feedback_id)

    # join using backref to access user info - check for feedback attached to username
    if "username" not in session or session['username'] != feedback.username:
        raise Unauthorized("Sorry, you're not authorized to do that!")

    # review THIS!
    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.user.username}")

    return render_template(
        "add_feedback.html", feedback=feedback, form=form, action='Update')


@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    """Delete feedback post and commit changes to DB"""

    feedback = Feedback.query.get_or_404(feedback_id)
    username = feedback.username

    # check if user is the owner of the feedback
    if "username" not in session or session['username'] != feedback.username:
        raise Unauthorized("Sorry, you're not authorized to do that!")

    db.session.delete(feedback)
    db.session.commit()

    return redirect(f"/users/{username}")
