from flask import Blueprint, render_template, abort, request, current_app as db, url_for
from flask.wrappers import Response
from flask_login import current_user, login_required
from jinja2 import TemplateNotFound
from ..models import User, Reading as Lb
from ..forms.forms_main import SearchForm


main = Blueprint('main', __name__, template_folder='templates')

# TODO: showing books after login in library and latest in index
# TODO: search route, famili library, all books, your library

@main.route('/')
def index() -> Response | str:
    """
    book -> {
        sale: bool,
        name: str,
        rating: float (will be changed to int),
        price: float,
        sale_price: float,
        owned: bool,
    }
    """

    ...  # here I should receive books
    # books: list[dict]
    
    # for book in books:
    #     rating = book.get('rating', None)
    #     if rating:
    #         book['rating'] = round(rating)
        
    # TODO: Delete example book
    book: dict = {
        'sale': True,
        'name': 'test',
        'rating': 4,
        'price': 3.50,
        'sale_price': 1.5,
        'owned': False,
    }
    ...
    return render_template('index.html', books=[book, book])


@main.route('/search/', methods=['GET', 'POST'])
def search() -> Response:
    form = SearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        if form.query.data:
            ...
            
    return render_template('search.html', form=form)
    
    
@main.route('/library/family_library/')
def family_library() -> Response:
   ...
   
   
@main.route('/library/user_library')
def user_library() -> Response:
    ...
    
    
@main.route('/library/')
def all_books() -> Response:
    ...
            