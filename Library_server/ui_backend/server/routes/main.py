from flask import Blueprint, render_template, abort, request, current_app as db, url_for
from flask.wrappers import Response
from flask_login import current_user, login_required
from jinja2 import TemplateNotFound
from ..models import User, Reading as Lb


main = Blueprint('main', __name__, template_folder='templates')

# TODO: showing books after login in library and latest in index
# TODO: search route, famili library, all books, your library

@main.route('/')
def index() -> Response:
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)


@main.route('/search/', methods=['GET', 'POST'])
def search() -> Response:
    ...
    
    
@main.route('/library/family_library/')
def family_library() -> Response:
   ...
   
   
@main.route('/library/user_library')
def user_library() -> Response:
    ...
    
    
@main.route('/library/')
def all_books() -> Response:
    ...
            