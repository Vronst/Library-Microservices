import os
from typing import Any, Optional
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

# TODO: Admin page whith option to add things

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
    stm: dict = {
        'User': User,
        'Library': Library,
        'RecentRead': RecentRead,
        'Family': Family,
    }
    query = lambda x: db_session.query(stm[x]).all()
    data = query(db)        
    columns = [column.key for column in stm[db].__table__.columns
            if column.key not in ['password', 'id']]
    return render_template('db_view.html', data=data, columns=columns)


# TODO: Finish this and start matis form !!!
@admin.route('/db/<string:db>/<int:id>', methods=['POST', 'DELETE', 'PUT', 'PATCH'])
@login_required
@is_admin
def edit_form(db: str, id: int) -> str | Response:
    if request.method in ['POST', 'PUT', 'PATCH']:
        stf: dict[str, FlaskForm] = {
            'User': FormUser,
            'Library': FormLibrary,
            'RecentRead': FormRecent,
            'Family': FormFamily
        }
        form: FlaskForm = stf[db](obj=) if not request.method == 'POST' else stf[db]()
        return redirect(url_for('admin.index'))
    elif request.method == 'DELETE':
        ...
        return '', 204
    else:
        return '', 405
