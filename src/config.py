"""Configuration objects for application"""
from os import environ


class BaseConfig:
    """Common properties for all environments"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(BaseConfig):
    """Production config"""
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URI')


class TestConfig(BaseConfig):
    """Testingconfig"""
    SQLALCHEMY_DATABASE_URI = environ.get('TEST_DATABASE_URI')
