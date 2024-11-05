from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from .models import User, Reading as Lb

main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
def index() -> str:
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)
