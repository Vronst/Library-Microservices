from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    EmailField,
    DateField,
    validators,
)
from .utils import birth_date_check


class RegistrationForm(FlaskForm):
    nick = StringField('Username', [validators.Length(min=6, max=16), validators.DataRequired()])
    name = StringField('Name', validators=[validators.length(min=3, max=25)])
    surname = StringField('Surname', validators=[validators.length(min=3, max=25)])
    email = EmailField('Email', validators=[validators.DataRequired(), validators.length(min=8, max=16)])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    repeat_password = PasswordField('Repeat password',
                                    validators=[
                                        validators.DataRequired(),
                                        validators.EqualTo(
                                            'password',
                                            message='Passwords must match!'
                                            )
                                        ]
                                    )
    age = DateField('Birth date', validators=[birth_date_check])

    
    
class LoginForm(FlaskForm):
    nick = StringField('Nick', validators=[validators.length(min=6, max=16), validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
        