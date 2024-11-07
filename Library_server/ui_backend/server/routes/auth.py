from datetime import datetime
from wtforms import ValidationError
from flask import Blueprint, flash, redirect, render_template, abort, request, current_app as db, url_for
from flask_login import login_user, login_required, logout_user, current_user
from flask.wrappers import Response
from werkzeug.security import generate_password_hash, check_password_hash
from jinja2 import TemplateNotFound
from ..models import User, Reading as Lb
from ..forms import RegistrationForm, LoginForm


auth = Blueprint('auth', __name__, template_folder='templates')
# TODO: ValidationError handling


@auth.route('/login', methods=['GET', 'POST'])
def login() -> Response:
    try:
        form = LoginForm()
        if request.method == 'POST' and form.validate_on_submit():
            user = db.session.query(User).filter(User.nick == form.nick.data).first()
            password = check_password_hash(user.password, form.password.data)
            if password:
                login_user(user)
                return redirect(url_for('main.index'))
            else:
                flash('Wrong nick or password!') 
        return render_template('login.html', login=True, form=form)
    except TemplateNotFound:
        abort(404)
    

@auth.route('/register', methods=['GET', 'POST'])    
def register() -> Response:
    try:
        form = RegistrationForm()
        if request.method == 'POST' and form.validate_on_submit():
            password = generate_password_hash(form.password.data, salt_length=24)
            user = User(
                nick=form.nick.data,
                name=form.name.data,
                surname=form.surname.data, 
                email=form.email.data, 
                password=password, 
                age=datetime.today().year - form.age.data.year
                )
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash(f'Error{form.errors}')
        return render_template('login.html', login=False, form=form)
    except TemplateNotFound:
        abort(404)
    except ValidationError as e:
        print(e)
        ...
        
        
    
@login_required
@auth.route('/logout', methods=['GET'])    
def logout() -> Response:
    logout_user()
    return redirect(url_for('main.index'))