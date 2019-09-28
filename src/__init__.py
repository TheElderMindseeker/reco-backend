"""Main file"""
from flask import Flask
from flask_migrate import Migrate

from src.helpers import bcrypt, jwt_manager
from src.models import db
from src.recycles import recycles
from src.views import views
from src.users import users


def create_app(config_object):
    """Application factory function"""
    app = Flask(__name__, static_folder=None, template_folder=None)
    app.config.from_object(config_object)

    app.register_blueprint(views)
    app.register_blueprint(recycles)
    app.register_blueprint(users)

    db.init_app(app)
    Migrate(app, db)
    bcrypt.init_app(app)
    jwt_manager.init_app(app)

    return app
