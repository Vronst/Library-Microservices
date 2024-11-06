from datetime import date
from wtforms import ValidationError


def birth_date_check(form, field) -> None:
    minimum_age = date.today().replace(year=date.today().year - 5)
    if field.data < date(1900, 1, 1) or field.data > date(minimum_age):
        raise ValidationError("Invalid date")
    