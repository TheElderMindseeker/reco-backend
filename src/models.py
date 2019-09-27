"""Database models for application"""
# pylint: disable=no-member
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """User of the system"""
    id = db.Column(db.Integer, primary_key=True)


class TrashUnit(db.Model):
    """Trash processing unit"""
    id = db.Column(db.Integer, primary_key=True)
