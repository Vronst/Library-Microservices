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
    password: PasswordField = PasswordField('Password', validators=[validators.DataRequired()])
    age: DateField = DateField('Birth date')
    family_id: IntegerField = IntegerField('family_id')
    
    
class FormLibrary(FlaskForm):
    book_name: StringField = StringField('book_name', validators=[validators.Length(min=1, max=60)])
    book_author: StringField = StringField('book_author', validators=[validators.Length(max=60)])
    book_id: IntegerField = IntegerField('book_id')
    user_id: IntegerField = IntegerField('user_id')
    current_page: IntegerField = IntegerField('current_page')
    pages: IntegerField = IntegerField('pages')
    family_id: IntegerField = IntegerField('family_id')
    img: StringField = StringField('img')
    genre: StringField = StringField('genre', validators=[validators.Length(max=30)])
    
    
class FormFamily(FlaskForm):
    name: StringField = StringField('name', validators=[validators.Length(max=50)])
    
    
class FormRecent(FlaskForm):
    user_id: IntegerField = IntegerField('user_id')
    book_id: IntegerField = IntegerField('book_id')
    time_stamp: DateTimeField = DateTimeField('time_stamp')
    