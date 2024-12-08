import os
import requests
from requests import Response as rResponse
from flask import Blueprint, flash, redirect, render_template, session, request, url_for
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

# TODO: change session to only store book id's and use them to query cache, like redis

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
    try:
        response: rResponse = connect_mati()
        books: list[dict] = response.json()
        img_checker(books) 
        # for book in books:
        #     book['img'] = 'https://dummyimage.com/600x700/dee2e6/6c757d.jpg' 
    except requests.exceptions.ConnectionError as e:
        books = []
        flash(f'Due to some error we couldn\'t load our books\n{e}')
    return render_template('index.html', books=books)


@main.route('/book/<string:author>/<string:name>/')
def book_view(author: str, name: str) -> str:
    book: requests = connect_mati(query={
        'author': author,
        'title': name,
    }).json()[0]
    img_checker(book)
    related_books: rResponse = connect_mati(query={'genre': book['gatunek']})
    in_library: Library | None = db_session.query(Library).filter(Library.book_author == author, Library.book_name == name).first()
    return render_template('book_view.html', book=book, related_books=related_books, in_library=in_library)


@main.route('/search/', methods=['GET', 'POST'])
def search() -> str:
    response: rResponse | list = []
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
            img_checker(response)
            
    return render_template('search.html', form=form, books=response, library=form.owned.data)
    
    
@main.route('/library/')
def all_books() -> str:
    ...
    return render_template('library.html')
    

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
    check_our_db = ...  # check if we have book
    
    if request.method == 'POST' and not check_user_db and check_our_db:
        if 'img' in request.form.keys():
            img = request.form['img']
        else:
            from ..utils import IMG
            img = IMG
        
        try:
            new_book = Library(
                book_name=name,
                book_author=author,
                user_id=int(current_user.get_id()),
                pages=request.form['pages'],
                img=img,
                genre=request.form['genre']
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
        