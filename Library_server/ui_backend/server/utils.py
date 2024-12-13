import requests
from functools import wraps
from typing import Any, Optional, Callable
from datetime import date
from wtforms import ValidationError
from sqlalchemy import Engine, text
from flask_login import LoginManager, current_user
from flask import abort
from werkzeug.security import generate_password_hash
from .models import User, RecentRead


IMG = 'https://dummyimage.com/600x700/dee2e6/6c757d.jpg'
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id) -> None | User:
    from . import session as db_session

    return db_session.get(User, user_id) 


def is_admin(func: Callable) -> object:
    @wraps(func)
    def wrapper(*args, **kwargs) -> object:
        if not current_user.is_admin:
            return abort(403)
        else:
            return func(*args, **kwargs)
    return wrapper


def get_token_mati() -> str:
    response: requests.Response = requests.post(
        'http://pro_sec:13601/api/Auth/login',
        json={'username': 'admin',
         'password': 'password'},
        headers={
            'Content-Type': 'application/json'
        })
    return response.text
    
def connect_mati(*, method: str='GET', payload: Optional[dict] = None, query: Optional[dict] = None, url: str = '') -> requests.Response:
    URL = 'http://pro_sec:8080/api/Books'
    response: requests.Response
    method = method.upper()
    headers: dict[str, Any] = {
        'Content-Type': 'application/json'
    }
    if method == 'GET':
        if query:
            final_url: str = URL + url + '/0?'
            for key, value in query.items():
                final_url += f'{key}={value.replace(' ', '%20')}&'
            response = requests.get(final_url, headers=headers)
        else:
            response = requests.get(URL + url, headers=headers)
    elif method == 'POST':
        response = requests.post(URL + url, json=payload, headers=headers)
    elif method == 'PUT':
        response = requests.put(URL + url, json=payload, headers=headers )
    elif method == 'DELETE':
        response = requests.delete(URL + url, headers=headers)
    print(response, response.text)  # should log it?   
    return response

    
def img_checker(book: list[dict] | dict) -> list[dict] | dict:
    UPDATE: dict = {'img': IMG}
    
    if isinstance(book, list):
        list(map(lambda book: book.update(UPDATE) if not book.get('img', None) else book, book))
    elif not book.get('img', None):
        book.update(UPDATE)
    return book

    
def add_recent_read(user_id: int, book_id: int) -> None:
    # should add sorting by timestamp
    from . import session as db_session
    check: RecentRead | None = db_session.query(RecentRead).filter(RecentRead.book_id == book_id).first()
    if check:
        return

    book_check: list[RecentRead] = db_session.query(RecentRead).filter(
        RecentRead.user_id == user_id
    ).all()

    if len(book_check) >= 6:
        db_session.delete(book_check[0])
        
    new_entry: RecentRead = RecentRead(
        user_id=user_id,
        book_id=book_id
    )
    
    db_session.add(new_entry)
    db_session.commit()


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
