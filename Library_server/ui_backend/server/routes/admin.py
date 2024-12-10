import os
from typing import Any
from flask import Blueprint, render_template
from werkzeug.wrappers.response import Response
from flask_login import login_required
from ..models import User, RecentRead, Library, Family
# from ..forms.forms_admin import 
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


@admin.route('/db/<string:db>', methods=['POST', 'GET'])
@login_required
@is_admin
def edit_db(db: str) -> str:
    data: list[Any]
    stf: dict = {
        'User': User,
        'Library': Library,
        'RecentRead': RecentRead,
        'Family': Family,
    }
    query = lambda x: db_session.query(stf[x]).all()
    data = query(db)        
    return render_template('db_view.html', data=data)
