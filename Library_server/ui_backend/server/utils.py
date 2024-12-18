import requests
import hmac
import hashlib
from functools import wraps
from typing import Any, Optional, Callable
from datetime import date
from wtforms import ValidationError
from sqlalchemy import Engine, text
from flask_login import LoginManager, current_user
from flask import abort
from werkzeug.security import generate_password_hash
from .models import User, RecentRead


IMG: str = 'https://dummyimage.com/600x700/dee2e6/6c757d.jpg'
TOKEN_URL: str = 'http://pro_sec:8080/api/Auth/login'
ADMIN_TOKEN: str | None = None
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


def hash_secret(secret: str, key: str):
    hashed = hmac.new(key.encode(), secret.encode(), hashlib.sha256).hexdigest()
    return hashed

    
SECRET = hash_secret('adammati', '34B8PKD4789NDSS889FD53AD31467C52DBE53ED2SDG5D8D82DDNMNDSA')


# TODO: finish this
def get_token_mati(id_: int = 0) -> str:
    response: requests.Response = requests.post(
        TOKEN_URL,
        json={'user_id': str(int),
              'secret': SECRET},
        headers={
            'Content-Type': 'application/json'
        })
    with open('token.log', 'w') as file:
        file.write(response.text) 
    return response.text


# try:
#     ADMIN_TOKEN = get_token_mati()
# except requests.exceptions.ConnectionError:
#     ADMIN_TOKEN = None
    
def connect_mati(*, method: str='GET', payload: Optional[dict] = None, query: Optional[dict] = None, url: str = '', **kwargs) -> requests.Response:        
    global ADMIN_TOKEN
    if not ADMIN_TOKEN:
        ADMIN_TOKEN = get_token_mati()
    URL = 'http://pro_sec:8080/api/Books'
    response: requests.Response
    method = method.upper()
    token: str = ADMIN_TOKEN 
    # token = 'lol'
    headers: dict[str, Any] = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    if method == 'GET':
        if kwargs.get('tokens', False):
            response = requests.get(URL.split('/Books')[0] + '/Auth/tokens')
        else:
            if query:
                final_url: str = URL + url + '/0?'
                for key, value in query.items():
                    final_url += f'{key}={value.replace(' ', '%20')}&'
                response = requests.get(final_url, headers=headers)
            else:
                response = requests.get(URL + url, headers=headers) if url \
                    else requests.get(URL + '/all' ,headers=headers)
    elif method == 'POST':
        response = requests.post(URL + url, json=payload, headers=headers)
    elif method == 'PUT':
        response = requests.put(URL + '/put', json=payload, headers=headers )
    elif method == 'DELETE':
        response = requests.delete(URL + url, headers=headers)
    with open('response.log', 'w') as file:
        file.write(response.text + str(response.status_code))
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
    with engine.connect() as conn:
        # Drop the dependent tables first
        conn.execute(text("DROP TABLE IF EXISTS recently_read CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS families CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS libraries CASCADE"))
        
        # Now drop the users table
        conn.execute(text("DROP TABLE IF EXISTS users CASCADE"))
    Base.metadata.drop_all(bind=engine)
    # Recreate tables
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
