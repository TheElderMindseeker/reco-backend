"""Database models for application"""
# pylint: disable=no-member
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry

db = SQLAlchemy()


class User(db.Model):
    """User of the system: customer or operator"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(16), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    points = db.Column(db.Integer, nullable=False, default=0)
    is_operator = db.Column(db.Boolean, nullable=False, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()


class Recycle(db.Model):
    """Trash processing unit"""
    __tablename__ = 'recycles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(256), nullable=False)
    position = db.Column(Geometry('POINT'), nullable=False)
    # Format: HH:MM
    open_time = db.Column(db.String(5), nullable=False)
    close_time = db.Column(db.String(5), nullable=False)
    # Separator: &
    trash_types = db.Column(db.String(512), nullable=False)
    bonus_program = db.Column(db.Boolean, nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()


class TrashPoint(db.Model):
    """"""
    __tablename__ = 'trash_points'

    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(Geometry('POINT'), nullable=False)
    contacts = db.Column(db.String(256), nullable=False)
    address = db.Column(db.String(256), nullable=False)
    trash_types = db.Column(db.String(512), nullable=False)
    comment = db.Column(db.String(512), nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()
