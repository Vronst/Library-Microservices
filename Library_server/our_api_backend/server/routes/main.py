from flask import Blueprint, current_app as db
from flask.wrappers import Response


main = Blueprint('main', __name__)


@main.route('/')
def to_be_renamed() -> Response:
    ...