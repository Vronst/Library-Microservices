from flask import Blueprint, render_template, abort, request, url_for
from flask.wrappers import Response
from flask_login import current_user, login_required
from ..models import User, RecentRead, Library
from ..forms.forms_main import SearchForm
from .. import session as db_session


main = Blueprint('main', __name__, template_folder='templates')

# TODO: showing books after login in library and latest in index
# TODO: search route, famili library, all books, your library

@main.route('/')
def index() -> str:
    """
    book -> {
        sale: bool,
        name: str,
        rating: float (will be changed to int),
        price: float,
        sale_price: float,
        owned: bool,
        author: str,
        genre: str,
        img: str,
        desc: str,
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
        'author': 'adam',
        'genre': 'fantasy',
    }
    ...
    return render_template('index.html', books=[book, book])


@main.route('/book/<string:author>/<string:name>')
def book_view(author, name) -> str:
    ...
    return render_template('book_view.html')


@main.route('/search/', methods=['GET', 'POST'])
def search() -> str:
    form = SearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        if form.query.data:
            ...
            
    return render_template('search.html', form=form)
    
    
@main.route('/library/family_library/')
@login_required
def family_library() -> str:
   ...
   return render_template('library.html')
   
   
@main.route('/library/my_library')
@login_required
def user_library() -> str:
    books: list[Library] = db_session.query(Library).filter(
        Library.user_id == int(current_user.get_id())  
        ).all()
    ...
    return render_template('library.html', pofile=f"{current_user.name}'s Library", books=books)
    
    
@main.route('/library/')
def all_books() -> str:
    ...
    return render_template('library.html')
            