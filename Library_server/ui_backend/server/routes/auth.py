from wtforms import ValidationError
from flask import Blueprint, render_template, abort, request, current_app as db
from jinja2 import TemplateNotFound
from ..models import User, Reading as Lb
from ..forms import RegistrationForm, LoginForm


main = Blueprint('auth', __name__, template_folder='templates')


@main.route('/login', methods=['GET', 'POST'])
def login() -> str:
    try:
        form = LoginForm()
        if request.method == 'POST' and form.validate():
            user = ...
        return render_template('login.html', login=True)
    except TemplateNotFound:
        abort(404)
    

@main.route('/register', methods=['GET', 'POST'])    
def register() -> str:
    try:
        form = RegistrationForm()
        if request.method == 'POST' and form.validate():
            password = ... # TODO: hash password for security
            user = User(form.nick, form.name, form.surname, form.email, password, form.age)
            db.session.add(user)
        return render_template('login', login=False)
    except TemplateNotFound:
        abort(404)
    except ValidationError:
        ...
        
        
    
@main.route('/logout', methods=['GET'])    
def logout() -> str:
    ...