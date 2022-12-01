"""Forms for our feedback application"""

from wtforms import StringField, PasswordField
from wtforms.validators import Length, Email, Optional, NumberRange, InputRequired
from flask_wtf import FlaskForm

class RegisterForm(FlaskForm):
    """Registration form"""
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6,max=55)])
    email = StringField("Email", validators=[InputRequired(), Email(), Length(max=50)])
    first_name = StringField("First name", validators=[InputRequired(), Length(max=30)])
    last_name = StringField("Last name", validators=[InputRequired(), Length(max=30)])


class LoginForm(FlaskForm):
    """Login form"""
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6,max=55)])


class DeleteForm(FlaskForm):
    """Blank form"""


class FeedbackForm(FlaskForm):
    """Feedback form/create new feedback"""
    title = StringField("Title", validators=[InputRequired(), Length(max=100)])
    content = StringField("Content", validators=[InputRequired()])
