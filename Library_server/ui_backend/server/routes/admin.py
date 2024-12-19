import os
import requests
from datetime import datetime
from typing import Any, Callable, Optional, Type
from flask import Blueprint, flash, render_template, request, redirect, url_for
from werkzeug.wrappers.response import Response
from werkzeug.security import generate_password_hash
from flask_login import login_required
from flask_wtf import FlaskForm
from ..models import User, RecentRead, Library, Family, Base
from ..forms.forms_admin import (
    FormFamily,
    FormLibrary,
    FormRecent,
    FormUser,
    BookForm,
    FormBook,
    FormToken,
)
from .. import session as db_session
from ..utils import is_admin, connect_mati


stf: dict = {
    'User': FormUser,
    'Library': FormLibrary,
    'RecentRead': FormRecent,
    'Family': FormFamily,
    'Tokens': FormToken,
    'Books': [FormBook, BookForm]
}
stm: dict[str, Type[Base]] = {
    'User': User,
    'Library': Library,
    'RecentRead': RecentRead,
    'Family': Family,
}
admin = Blueprint('admin',
                  __name__,
                  template_folder=os.path.join(
                      os.path.dirname(__file__), '../templates/admin'
                  ))


@admin.route('/')
@login_required
@is_admin
def index() -> str:
    len_user: int = len(db_session.query(User).all())
    len_library: int = len(db_session.query(Library).all())
    len_recent: int = len(db_session.query(RecentRead).all())
    len_family: int = len(db_session.query(Family).all())
    try:
        len_books: int = len(connect_mati().json())
    except requests.exceptions.JSONDecodeError:
        len_books = 0
    try:
        len_tokens: int = len(connect_mati(tokens=True).json())
    except requests.exceptions.JSONDecodeError:
        len_tokens = 0
        
    databases = {
        'User': len_user,
        'RecentRead': len_recent,
        'Library': len_library,
        'Family': len_family,
        'Books': len_books,
        'Tokens': len_tokens,
        }
    return render_template('admin_index.html', databases=databases)


@admin.route('/db/<string:db>', methods=['GET'])
@login_required
@is_admin
def edit_db(db: str) -> str | Response | tuple[str, int]:
    data: list[Any]
    columns: list[str]
    if db == 'Books':
        columns = [
            'tytul',
            'autor',
            'dostepnosc',
            'gatunek',
            'dataWydania',
            'liczbaStron'
        ]
        try:
            data = connect_mati().json()
        except requests.exceptions.JSONDecodeError:
            data = []
    elif db == 'Tokens':
        columns = [
            'user_id',
            'secret',
        ]
        try:
            data = connect_mati(tokens=True).json()
        except requests.exceptions.JSONDecodeError:
            data = []
    else:
        query: Callable = lambda x: db_session.query(stm[x]).all()
        data = query(db)        
        columns = [column.key for column in stm[db].__table__.columns
                if column.key not in ['password', 'id']]
    return render_template('db_view.html', data=data, columns=columns, db=db)


@admin.route('/db/<string:db>/', methods=['POST'])
@admin.route('/db/<string:db>/<int:id>', methods=['POST', 'DELETE', 'PUT', 'PATCH'])
@login_required
@is_admin
def edit_form(db: str, id: int | None = None) -> str | tuple[str, int] | Response:
    # Yes i know it should be id_ or smth else then id..
    # This function could be beter organises so TODO: organise it better
    # matis db
    form: FlaskForm
    columns: list[str]
    token: bool = False
    redirection: bool = False

    if request.method == 'DELETE':
        
        if db == 'Books':
            connect_mati(method='DELETE', url=f'/{id}')
            return '', 204
        model = db_session.query(stm[db]).get(id)
        db_session.delete(model)
        db_session.commit()
        return '', 204

    match db:
        case 'Books':
            columns = [
                'ksiazkaID',
                'tytul',
                'autor',
                'dostepnosc',
                'gatunek',
                'dataWydania',
                'liczbaStron'
            ]
            if id:
                book = connect_mati(url=f'/{id}').json()
                form = stf[db][1](**book)
            else:
                columns.remove('ksiazkaID')
                form =stf[db][0]()
            if form.validate_on_submit():
                payload: dict = {**form.data}
                # will it fix mateo?
                fix_mateo: Callable = lambda x: x[0].upper() + x[1:]
                payload = {fix_mateo(key): value for key, value in payload.items()}
                if id:
                    response: requests.Response = connect_mati(method='PUT', payload=payload, url=f'/{id}')
                else:
                    response = connect_mati(method='POST', payload=payload)
                if response.status_code not in [204, 201]:
                    with open('admin.log', 'w') as file:
                        file.write(response.text + str(response.status_code))
                    flash('Connection failed')
                redirection = True
        case 'Tokens':
            columns = [
                'token_id',
                'user_id'
                ]
            if id:
                token_data = connect_mati(token=id).json()
                form = stf[db](**token_data)
            else:
                columns.remove('token_id')    
                form = stf[db]()
            if form.validate_on_submit():
                payload = {**form.data}
                if id:
                    response = connect_mati(method='PUT', payload=payload, url=f'/{id}')
                else:
                    response = connect_mati(method='POST',payload=payload, tokens=True, user_id=form.user_id.data)
                redirection = True 
            token = True
        case _:
            ignore: list[str] = ['id']
            obj: Base | None = db_session.query(stm[db]).get(ident=id)
            form = stf[db](obj=obj) if id else stf[db]()  
            columns = [column.key for column in stm[db].__table__.columns
                    if column.key not in ignore]
            if form.validate_on_submit():
                if id:
                    model = db_session.query(stm[db]).get(ident=id)
                    if 'password' in form.data:
                        if form.data.get('password') == None and model:
                            form.password.data = model.password  
                        else:
                            form.password.data = generate_password_hash(form.data.get('password'), salt_length=24)
                    form.populate_obj(model)
                else:
                    form_data: dict[str, Any] = {key: value for key, value in form.data.items() if key not in ['csrf_token']}
                    if 'password' in form.data:
                        form_data['password'] = generate_password_hash(form.data['password'], salt_length=24)
                    model = stm[db](**form_data)
                    db_session.add(model)
                db_session.commit()
                redirection = True
    if redirection:
        return redirect(url_for('admin.edit_db', db=db))  
    else:
        return render_template('edit_form.html', form=form, columns=columns, id=id, db=db, token=token)  