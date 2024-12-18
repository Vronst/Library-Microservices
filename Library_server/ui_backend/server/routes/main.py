import os
from typing import Iterable
import requests
from requests import Response as rResponse
from flask import Blueprint, flash, redirect, render_template, session, request, url_for
# from sqlalchemy import Query
from werkzeug.wrappers.response import Response
from flask_login import current_user, login_required
from ..models import User, RecentRead, Library, Family
from ..forms.forms_main import SearchForm
from ..utils import connect_mati, img_checker
from .. import session as db_session


main = Blueprint(
    'main',
    __name__,
    template_folder=os.path.join(
        os.path.dirname(__file__), '../templates/main'))

# Maybe add redis to store recent books? or  id's

@main.route('/')
def index() -> str:
    """
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
    """
    books: list | list[Library] = []
    if current_user.is_authenticated:
        recent: list[RecentRead] = current_user.latest
        books = [book.library for book in recent]
    return render_template('library.html', books=books, index=True)


@main.route('/book/<string:author>/<string:name>/')
def book_view(author: str, name: str) -> str:
    book: dict = connect_mati(query={
        'author': author,
        'title': name,
    }).json()[0]
    img_checker(book)
    related_books: dict = connect_mati(query={'genre': book['gatunek']}).json()  # add [:n] where n is limiter
    img_checker(related_books)
    in_library: Library | None = db_session.query(Library).filter(Library.book_author == author, Library.book_name == name).first()
    return render_template('book_view.html', book=book, related_books=related_books, in_library=in_library)


@main.route('/search/', methods=['GET', 'POST'])
def search() -> str:
    response: Iterable[Library] | list | dict = []
    form = SearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        if form.owned.data:
            response = db_session.query(Library).filter(
                Library.user_id == int(current_user.get_id())
            )
            if form.author.data:
                response = response.filter(Library.book_author.ilike(form.author.data))
            if form.title.data:
                response = response.filter(Library.book_name.ilike(form.title.data))
            response = response.all()
        else:
            query: dict = {}
            if author := form.author.data:
                query.update({'author': author})
            if title := form.title.data:
                query.update({'title': title})
            response = connect_mati(query=query).json()
            if isinstance(response, dict) or isinstance(response, list):
                img_checker(response)
            
    return render_template('search.html', form=form, books=response, library=form.owned.data)
    
    
@main.route('/library/')
def all_books() -> str:
    exceptions: list[Exception] | list = []
    try:
        response: rResponse = connect_mati()
        books: list[dict] = response.json()
        img_checker(books) 
    except requests.exceptions.ConnectionError as e:
        books = []
        exceptions.append(e)
    except requests.exceptions.JSONDecodeError as e:
        books = []
        exceptions.append(e)
    if exceptions:
        flash(f'Due to some error we couldn\'t load our books\n{exceptions}')
    return render_template('index.html', books=books)
    

@main.route('/library/family_library/')
@login_required
def family_library() -> str:
   family = current_user.family_id
   # family = db_session.query(Family).filter(Family.id == current_user.family_id)
   family_books: dict = {}
   if family:
    family_books = {user.name: user.library for user in family.users}
    for user in family.users:
        family_books[user.name] = user.library.all()
   return render_template('library.html', family_books=family_books)
   
   
@main.route('/library/my_library', methods=['GET'])
@login_required
def user_library() -> str:
    books: list[Library] = db_session.query(Library).filter(
        Library.user_id == int(current_user.get_id())  
        ).all()
    return render_template('library.html', pofile=f"{current_user.name}'s Library", books=books)


@main.route('/library/my_library/<string:author>/<string:name>', methods=['POST', 'DELETE'])
@login_required
def edit_library(author: str, name: str) -> tuple[str, int] | Response:
    check_user_db = db_session.query(Library).filter(Library.book_author == author, Library.book_name == name).first()
    check_our_db = connect_mati(query={
        'author': author,
        'title': name
        }).json()[0]  # check if we have book
    
    if request.method == 'POST' and not check_user_db and check_our_db:
        if 'img' in request.form.keys():
            img = request.form['img']
        else:
            from ..utils import IMG
            img = IMG
        # Could be better since we can get everything from check_our_db instead of
        # passing params through forms
        try:
            new_book = Library(
                book_name=name,
                book_author=author,
                user_id=int(current_user.get_id()),
                pages=request.form['pages'],
                img=img,
                genre=request.form['genre'],
                book_id = check_our_db.get('ksiazkaID', None)
            )
            db_session.add(new_book)
            db_session.commit()
        except KeyError:
            flash('KeyError, action aborted')
        return redirect(url_for('main.book_view', author=author, name=name))
    elif request.method == 'DELETE' and check_user_db:
        db_session.delete(check_user_db)
        db_session.commit()
        return '', 204 
    else:
        flash('You already own this book')
        return redirect(url_for('main.user_library'))
        

@main.route('/read/<string:author>/<string:name>')
@login_required
def read_book(author: str, name: str) -> Response:
    from ..utils import add_recent_read
    book: Library | None = db_session.query(Library).filter(
        Library.book_author == author,
        Library.book_name == name
    ).first()
    if book:
        book_id = book.id
        add_recent_read(int(current_user.get_id()), book_id=book_id)
    return redirect(url_for('main.index'))