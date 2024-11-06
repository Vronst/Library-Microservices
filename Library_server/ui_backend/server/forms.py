from wtforms import (
    Form,
    StringField,
    PasswordField,
    EmailField,
    DateField,
    validators,
)
from .utils import birth_date_check


class RegistrationForm(Form):
    nick = StringField('Username', [validators.Length(min=6, max=16), validators.DataRequired()])
    name = StringField('Name', validators=[validators.length(min=3, max=25)])
    surname = StringField('Surname', validators=[validators.length(min=3, max=25)])
    email = EmailField('Email', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    age = DateField('Birth date', validators=[birth_date_check])

    
    
class LoginForm(Form):
    nick = StringField('Nick', validators=[validators.length(min=6, max=16), validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
        