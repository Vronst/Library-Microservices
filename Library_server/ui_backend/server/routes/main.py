import os
import requests
from flask import Blueprint, flash, redirect, render_template, session, request, url_for
from werkzeug.wrappers.response import Response
from flask_login import current_user, login_required
from ..models import User, RecentRead, Library
from ..forms.forms_main import SearchForm
from .. import session as db_session


main = Blueprint(
    'main',
    __name__,
    template_folder=os.path.join(
        os.path.dirname(__file__), '../templates/main'))

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
    books: None | list[dict]
    # here I should receive books
    # books: list[dict]
    
    # for book in books:
    #     rating = book.get('rating', None)
    #     if rating:
    #         book['rating'] = round(rating)
    #         book['img'] = book['img'] | 'https://dummyimage.com/600x700/dee2e6/6c757d.jpg' 
        
    # TODO: Delete example book
    # book: dict = {
    #     'sale': True,
    #     'name': 'test',
    #     'rating': 4,
    #     'price': 3.50,
    #     'sale_price': 1.5,
    #     'owned': False,
    #     'author': 'adam',
    #     'genre': 'fantasy',
    #     'img': None
    # }
    books = {
    "ksiazkaID": 1,
    "tytul": "Pod Wulkanem",
    "autor": "Malcolm Lowry",
    "dostepnosc": True,
    "gatunek": "Literatura piękna",
    "dataWydania": "1947-01-01",
    "liczbaStron": 403,
    'img': 'https://dummyimage.com/600x700/dee2e6/6c757d.jpg'
    }
    import copy  #FIXME: delete this
    ...
    try:
        response = requests.get('http://localhost:7056/api/Books')
        books = response.text 
    except requests.exceptions.ConnectionError:
        books = None
        flash('Due to some error we couldn\'t load our books')
    session['books'] = [copy.deepcopy(books), copy.deepcopy(books)]  # FIXME: delete [] and add request to mateo db
    return render_template('index.html', books=[books, books])


@main.route('/book/<string:author>/<string:name>/')
def book_view(author, name) -> str:
    if books := session.get('books'):
        for book in books: 
            current_book = book if book.get('autor') == author and book.get('tytul') == name else None
            if current_book:
                break
    else:
        # TODO: query matis db
        ...
    return render_template('book_view.html', book=current_book, related_books=[1, 1])


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
            

@main.route('/add/<string:author>/<string:name>')
@login_required
def add_to_library(author, name) -> Response:
    new_book = Library(
        book_name=name,
        book_author=author,
        user_id=int(current_user.get_id()),
    )
    db_session.add(new_book)
    db_session.commit()
    return redirect(url_for('book_view', author=author, name=name))