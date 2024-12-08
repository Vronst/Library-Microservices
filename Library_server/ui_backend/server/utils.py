import requests
from typing import Optional
from datetime import date
from wtforms import ValidationError
from sqlalchemy import Engine, text
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from .models import User


IMG = 'https://dummyimage.com/600x700/dee2e6/6c757d.jpg'
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id) -> None | User:
    from . import session as db_session

    return db_session.get(User, user_id) 

    
def connect_mati(*, method: str='GET', payload: Optional[dict] = None, query: Optional[dict] = None, url: str = '') -> requests:
    URL = 'http://pro_sec:8080/api/Books'
    response: requests
    method = method.upper()
    if method == 'GET':
        if query:
            final_url: str = URL + url + '/0?'
            for key, value in query.items():
                final_url += f'{key}={value.replace(' ', '%20')}&'
            response = requests.get(final_url)
        else:
            response = requests.get(URL + url)
    elif method == 'POST':
        ...
        
    return response

    
def img_checker(book: list[dict] | dict) -> list[dict] | dict:
    UPDATE: dict = {'img': IMG}
    
    if isinstance(book, list):
        list(map(lambda book: book.update(UPDATE) if not book.get('img', None) else book, book))
    elif not book.get('img', None):
        book.update(UPDATE)
    return book


def birth_date_check(form, field) -> None:
    if field.data == None:
        return
    minimum_age = date.today().replace(year=date.today().year - 5)
    if field.data < date(1900, 1, 1) or field.data > minimum_age:
        raise ValidationError("Invalid date")
    

def reset_database() -> None:
    from server import get_engine
    from server import Base
    
    engine: Engine = get_engine()
    
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    engine.dispose()
    print("Database successfuly reseted")


def populate_users_db() -> None:
    from server import session as db_session

    user = User(
        nick='adam',
        name='adam',
        surname='adam',
        email='adam@adam.pl',
        password=generate_password_hash('adam', salt_length=24)
    )
    admin = User(
        nick='admin',
        admin=True,
        name='admin',
        surname='admin',
        email='admin@admin.pl',
        password=generate_password_hash('admin', salt_length=24)
    )
    db_session.add(user)
    db_session.add(admin)
    db_session.commit()
    print("Database successfuly populated")
