"""Database models for application"""
# pylint: disable=no-member
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry

db = SQLAlchemy()


class Recycle(db.Model):
    """Trash processing unit"""
    __tablename__ = 'recycles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(256), nullable=False)
    position = db.Column(Geometry('POINT'))
    # Format: HH:MM
    open_time = db.Column(db.String(5), nullable=False)
    close_time = db.Column(db.String(5), nullable=False)
    # Separator: &
    trash_types = db.Column(db.String(512), nullable=False)
    bonus_program = db.Column(db.Boolean, nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()
