import os
from typing import Any, Callable, Optional, Type
from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.wrappers.response import Response
from flask_login import login_required
from flask_wtf import FlaskForm
from ..models import User, RecentRead, Library, Family, Base
from ..forms.forms_admin import (
    FormFamily,
    FormLibrary,
    FormRecent,
    FormUser,
)
from .. import session as db_session
from ..utils import is_admin


stf: dict[str, Type[FlaskForm]] = {
    'User': FormUser,
    'Library': FormLibrary,
    'RecentRead': FormRecent,
    'Family': FormFamily
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
    databases = {
        'User': len_user,
        'RecentRead': len_recent,
        'Library': len_library,
        'Family': len_family
        }
    return render_template('admin_index.html', databases=databases)


@admin.route('/db/<string:db>', methods=['GET'])
@login_required
@is_admin
def edit_db(db: str, id: Optional[int] = None) -> str | Response | tuple[str, int]:
    data: list[Any]
    query: Callable = lambda x: db_session.query(stm[x]).all()
    data = query(db)        
    columns: list[str] = [column.key for column in stm[db].__table__.columns
            if column.key not in ['password', 'id']]
    return render_template('db_view.html', data=data, columns=columns, db=db)


# TODO: Finish this and start matis form !!!
@admin.route('/db/<string:db>/<int:id>', methods=['POST', 'DELETE', 'PUT', 'PATCH'])
@login_required
@is_admin
def edit_form(db: str, id: int) -> str | tuple[str, int]:
    # Yes i know it should be id_ or smth else then id..
    if request.method in ['PUT', 'PATCH', 'POST']:
        obj: Base | None = db_session.query(stm[db]).get(ident=id)
        post_check = request.form['_method'] if '_method' in request.form.keys() else False
        form: FlaskForm = stf[db](obj=obj) if not request.method == 'POST' or post_check == 'PUT' else stf[db]()
        columns: list[str] = [column.key for column in stm[db].__table__.columns
                if column.key not in ['password', 'id']]
        return render_template('edit_form.html', form=form, columns=columns)
    elif request.method == 'DELETE':
        ...
        return '', 204
    else:
        return '', 405
