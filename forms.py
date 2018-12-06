# import flask forms
# create validator functions to be called when forms are submitted

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email, Length


class RegisterForm(FlaskForm):
    """Form for registering a user."""

    username = StringField(
        "Username", validators=[InputRequired(),
                                Length(max=20)])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField(
        "Email", validators=[InputRequired(),
                             Email(), Length(max=50)])
    first_name = StringField(
        "First Name", validators=[InputRequired(),
                                  Length(max=30)])
    last_name = StringField(
        "Last Name", validators=[InputRequired(),
                                 Length(max=30)])


class LoginForm(FlaskForm):
    """Form for logging in a user"""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


class FeedbackForm(FlaskForm):
    """Form for adding feedback to a user"""

    title = StringField("Title", validators=[InputRequired()])
    content = TextAreaField(
        "Content", validators=[InputRequired(),
                               Length(max=500)])
