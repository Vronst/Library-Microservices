import os
import requests
from flask import Blueprint, flash, redirect, render_template, session, request, url_for
from werkzeug.wrappers.response import Response
from flask_login import current_user, login_required
from ..models import User, RecentRead, Library, Family
from ..forms.forms_main import SearchForm
from .. import session as db_session


main = Blueprint(
    'main',
    __name__,
    template_folder=os.path.join(
        os.path.dirname(__file__), '../templates/main'))

# TODO: change session to only store book id's and use them to query cache, like redis

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
    
    # 'https://dummyimage.com/600x700/dee2e6/6c757d.jpg' 
        
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
    # try:
    #     response = requests.get('http://localhost:7056/api/Books')
    #     books = response.text 
    # except requests.exceptions.ConnectionError:
    #     books = None
    #     flash('Due to some error we couldn\'t load our books')
    session['books'] = [copy.deepcopy(books), copy.deepcopy(books)]  # FIXME: delete [] and add request to mateo db
    return render_template('index.html', books=[books, books])


@main.route('/book/<string:author>/<string:name>/')
def book_view(author: str, name: str) -> str:
    if books := session.get('books', None):
        ...  # query matis db for books since session should hold only id's / check redis?
        for book in books: 
            current_book = book if book.get('autor') == author and book.get('tytul') == name else None
            if current_book:
                session['current_book'] = current_book
                break
    else:
        # TODO: query matis db
        ...
    in_library: Library | None = db_session.query(Library).filter(Library.book_author == author, Library.book_name == name).first()
    return render_template('book_view.html', book=current_book, related_books=[1, 1], in_library=in_library)


@main.route('/search/', methods=['GET', 'POST'])
def search() -> str:
    form = SearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        if form.query.data:
            ...
            
    return render_template('search.html', form=form)
    
    
@main.route('/library/')
def all_books() -> str:
    ...
    return render_template('library.html')
    

@main.route('/library/family_library/')
@login_required
def family_library() -> str:
   family = current_user.family_id
   return render_template('library.html')
   
   
@main.route('/library/my_library', methods=['GET'])
@login_required
def user_library() -> str:
    books: list[Library] = db_session.query(Library).filter(
        Library.user_id == int(current_user.get_id())  
        ).all()
    ...
    return render_template('library.html', pofile=f"{current_user.name}'s Library", books=books)


# @main.route('/library/my_library/<string:author>/<string:name>')
# @login_required
# def owned_book(author: str, name:str) -> str | Response:
#     book = db_session.query(Library).filter(
#         Library.user_id == current_user.get_id(),
#         Library.book_author == author,
#         Library.book_name == name)
#     if book:
#         ...
#         return render_template('book.html')
#     else:
#         # TODO: query matis db and based on result redirect to correct page
#         if ...:
#             return redirect(url_for('main.book_view'))
#         else:
#             return redirect(url_for('main.user_library'))
        

@main.route('/library/my_library/<string:author>/<string:name>', methods=['POST', 'DELETE'])
@login_required
def edit_library(author: str, name: str) -> tuple[str, int] | Response:
    check_user_db = db_session.query(Library).filter(Library.book_author == author, Library.book_name == name).first()
    check_our_db = ...  # check if we have book
    
    if request.method == 'POST' and not check_user_db and check_our_db:
        new_book = Library(
            book_name=name,
            book_author=author,
            user_id=int(current_user.get_id()),
            pages=session['current_book']['liczbaStron']
        )
        db_session.add(new_book)
        db_session.commit()
        return redirect(url_for('main.book_view', author=author, name=name))
    elif request.method == 'DELETE' and check_user_db:
        db_session.delete(check_user_db)
        db_session.commit()
        return '', 204 
    else:
        flash('You already own this book')
        return redirect(url_for('main.user_library'))
        


# @main.route('/')    
