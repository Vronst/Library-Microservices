from flask_wtf import FlaskForm # type: ignore
from wtforms import ( # type: ignore
    StringField,
    PasswordField,
    EmailField,
    DateField,
    validators,
    IntegerField,
    BooleanField,
    DateTimeField,
)  


class FormUser(FlaskForm):
    admin: BooleanField = BooleanField('admin')
    nick: StringField = StringField('Username', [validators.Length(min=6, max=16), validators.DataRequired()])
    name: StringField = StringField('Name', validators=[validators.length(min=3, max=25)])
    surname: StringField = StringField('Surname', validators=[validators.length(min=3, max=25)])
    email: EmailField = EmailField('Email', validators=[validators.DataRequired(), validators.length(min=8, max=16)])
    password: PasswordField = PasswordField('Password', validators=[validators.Optional()])
    family_id: IntegerField = IntegerField('family_id', validators=[validators.Optional()])
    
    
class FormLibrary(FlaskForm):
    book_name: StringField = StringField('book_name', validators=[validators.Length(min=1, max=60)])
    book_author: StringField = StringField('book_author', validators=[validators.Length(max=60)])
    book_id: IntegerField = IntegerField('book_id', validators=[validators.Optional()])
    user_id: IntegerField = IntegerField('user_id', validators=[validators.Optional()])
    current_page: IntegerField = IntegerField('current_page', validators=[validators.Optional()])
    pages: IntegerField = IntegerField('pages', validators=[validators.Optional()])
    family_id: IntegerField = IntegerField('family_id', validators=[validators.Optional()])
    img: StringField = StringField('img', validators=[validators.Optional()])
    genre: StringField = StringField('genre', validators=[validators.Length(max=30)])
    
    
class FormFamily(FlaskForm):
    name: StringField = StringField('name', validators=[validators.Length(max=50)])
    
    
class FormRecent(FlaskForm):
    user_id: IntegerField = IntegerField('user_id')
    book_id: IntegerField = IntegerField('book_id')
    time_stamp: DateTimeField = DateTimeField('time_stamp')
    
    
class BookForm(FlaskForm):
    ksiazkaID: IntegerField = IntegerField('ksiazkaID', validators=[validators.DataRequired()])
    tytul: StringField = StringField('Tytul', validators=[validators.DataRequired()])
    autor: StringField = StringField('Autor', validators=[validators.DataRequired()])
    dostepnosc: BooleanField = BooleanField('Dostepnosc', default=False, validators=[validators.Optional()])
    gatunek: StringField = StringField('Gatunek', validators=[validators.DataRequired()])
    dataWydania: StringField = StringField('Data Wydania', validators=[validators.Optional()])
    liczbaStron: IntegerField = IntegerField('Liczba stron', validators=[validators.DataRequired()])


class FormBook(FlaskForm):
    tytul: StringField = StringField('Tytul', validators=[validators.DataRequired()])
    autor: StringField = StringField('Autor', validators=[validators.DataRequired()])
    dostepnosc: BooleanField = BooleanField('Dostepnosc', default=False, validators=[validators.Optional()])
    gatunek: StringField = StringField('Gatunek', validators=[validators.DataRequired()])
    dataWydania: StringField = StringField('Data Wydania', validators=[validators.Optional()])
    liczbaStron: IntegerField = IntegerField('Liczba stron', validators=[validators.DataRequired()])
    

class FormToken(FlaskForm):
    token_id: IntegerField = IntegerField('Token ID', validators=[validators.DataRequired()])
    user_id: IntegerField = IntegerField('User ID', validators=[validators.DataRequired()])