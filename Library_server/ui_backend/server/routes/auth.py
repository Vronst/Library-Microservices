import os
from datetime import datetime
# from wtforms import ValidationError # type: ignore
from flask import Blueprint, flash, redirect, render_template, request, url_for # type: ignore
from flask_login import login_user, login_required, logout_user
# from flask.wrappers import Response
from werkzeug.wrappers.response import Response as werResponse
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import User, RecentRead
from ..forms.forms_auth import RegistrationForm, LoginForm
from .. import session as db_session


auth: Blueprint = Blueprint('auth',
                            __name__,
                            template_folder=os.path.join(
                                os.path.dirname(__file__), '../templates/auth'
                            ))


@auth.route('/login', methods=['GET', 'POST'])
def login() -> werResponse | str:
    form: LoginForm = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user: User | None = db_session.query(User).filter(User.email == form.email.data).first() # type: ignore[attr-defined]
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash('Wrong email or password!') 
    if form.errors:
        flash(f'Login error: {form.errors}')
    return render_template('login.html', login=True, form=form)
    
    

@auth.route('/register', methods=['GET', 'POST'])    
def register() -> werResponse | str:
    form: RegistrationForm = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        password: str = generate_password_hash(form.password.data, salt_length=24)
        existing_user: User | None = db_session.query(User).filter_by(nick=form.nick.data).first()
        existing_user2: User | None = db_session.query(User).filter_by(email=form.email.data).first()
        if not existing_user and not existing_user2:
            user: User | None = User(
                nick=form.nick.data,
                name=form.name.data,
                surname=form.surname.data, 
                email=form.email.data, 
                password=password, 
                age=datetime.today().year - form.age.data.year
                )
            db_session.add(user) # type: ignore[attr-defined]
            db_session.commit() # type: ignore[attr-defined]
            
            login_user(user)
            return redirect(url_for('main.index'))
        elif existing_user2:
            flash('Account with this email already exists')
        elif existing_user:
            flash('Nick is already taken')
    if form.errors:
        flash(f'Registeration error: {form.errors}')
    return render_template('login.html', login=False, form=form)
        
        
    
@auth.route('/logout', methods=['GET'])    
@login_required
def logout() -> werResponse:
    logout_user()
    return redirect(url_for('main.index'))