from datetime import date
from wtforms import ValidationError
from flask_login import LoginManager
from .models import User


login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id) -> None | User:
    from . import session as db_session

    return db_session.get(User, user_id) 


def birth_date_check(form, field) -> None:
    if field.data == None:
        return
    minimum_age = date.today().replace(year=date.today().year - 5)
    if field.data < date(1900, 1, 1) or field.data > minimum_age:
        raise ValidationError("Invalid date")
    