"""Application views"""
from flask import Blueprint


views = Blueprint('views', __name__)


@views.route('/hello')
def hello_world():
    return '<h1>Hello world</h1>'
