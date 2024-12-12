from flask_wtf import FlaskForm # type: ignore
from wtforms import ( # type: ignore
    StringField,
    PasswordField,
    EmailField,
    DateField,
    validators,
)  
from ..utils import birth_date_check


class RegistrationForm(FlaskForm):
    nick: StringField = StringField('Username', [validators.Length(min=6, max=16), validators.DataRequired()])
    name: StringField = StringField('Name', validators=[validators.length(min=3, max=25)])
    surname: StringField = StringField('Surname', validators=[validators.length(min=3, max=25)])
    email: EmailField = EmailField('Email', validators=[validators.DataRequired(), validators.length(min=8, max=16)])
    password: PasswordField = PasswordField('Password', validators=[validators.DataRequired()])
    repeat_password: PasswordField = PasswordField('Repeat password',
                                    validators=[
                                        validators.DataRequired(),
                                        validators.EqualTo(
                                            'password',
                                            message='Passwords must match!'
                                            )
                                        ]
                                    )

    
    
class LoginForm(FlaskForm):
    email: EmailField = EmailField('Email', validators=[validators.DataRequired(), validators.length(min=8, max=16)])
    password: PasswordField = PasswordField('Password', validators=[validators.DataRequired()])
        