from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField


class SearchForm(FlaskForm):
    query: StringField = StringField()
    owned: BooleanField = BooleanField('Owned', default=False) 
    