from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField


class SearchForm(FlaskForm):
    author: StringField = StringField()
    title: StringField = StringField()
    owned: BooleanField = BooleanField('Owned', default=False) 
    