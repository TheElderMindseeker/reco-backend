"""Configuration objects for application"""
from os import environ


class BaseConfig:
    """Common properties for all environments"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '3wW#Da_;Cu(;"NDuc=`W1f]G}>LYw|'
    JWT_SECRET_KEY = 'bGtHa,m^$=la;=>^KQ`9C,Ynvg"$TV'


class ProdConfig(BaseConfig):
    """Production config"""
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')


class TestConfig(BaseConfig):
    """Testingconfig"""
    SQLALCHEMY_DATABASE_URI = environ.get('TEST_DATABASE_URI')
