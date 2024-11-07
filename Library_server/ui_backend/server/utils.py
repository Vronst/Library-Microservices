from flask import current_app as db
from datetime import date
from wtforms import ValidationError
from flask_login import LoginManager
from .models import User


login_manager = LoginManager()
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id) -> None:
    return db.session.get(User, user_id)


def birth_date_check(form, field) -> None:
    minimum_age = date.today().replace(year=date.today().year - 5)
    if field.data < date(1900, 1, 1) or field.data > minimum_age:
        raise ValidationError("Invalid date")
    