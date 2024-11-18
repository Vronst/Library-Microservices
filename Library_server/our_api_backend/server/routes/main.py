from flask import Blueprint, current_app as db, request
from flask.wrappers import Response


main = Blueprint('main', __name__)


@main.route('/v1/query')
def search_query() -> Response:
    query: str = request.args.get('query')

    if query:
        ...
    