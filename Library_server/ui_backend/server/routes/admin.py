import os
from flask import Blueprint, render_template
from werkzeug.wrappers.response import Response
from flask_login import login_required
from ..models import User, RecentRead, Library
# from ..forms.forms_admin import 
from .. import session as session_db


admin = Blueprint('admin',
                  __name__,
                  template_folder=os.path.join(
                      os.path.dirname(__file__), '../templates/admin'
                  ))


@admin.route('/')
@login_required
def index() -> str:
    ...
    return render_template('index.html')


@admin.route('/db/users/')
@login_required
def users_view() -> str:
    ...
    return render_template('db_view.html')


@admin.route('/db/libraries/')
@login_required
def libraries_view() -> str:
    ...
    return render_template('db_view.html')


@admin.route('/db/recentread/')
@login_required
def recentread_view() -> str:
    ...
    return render_template('db_view.html')
