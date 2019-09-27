"""Main file"""
from flask import Flask
from flask_migrate import Migrate
from src.views import views

from src.models import db
from src.helpers import bcrypt


def create_app(config_object):
    """Application factory function"""
    app = Flask(__name__, static_folder=None, template_folder=None)
    app.config.from_object(config_object)

    app.register_blueprint(views)

    db.init_app(app)
    Migrate(app, db)
    bcrypt.init_app(app)

    return app
