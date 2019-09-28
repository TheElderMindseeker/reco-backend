"""Various helpers for the system"""
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

bcrypt = Bcrypt()
jwt_manager = JWTManager()
