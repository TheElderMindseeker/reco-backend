from flask import Blueprint, abort
from flask_jwt_extended import create_access_token
from flask_restful import Api, Resource, marshal_with, reqparse

from src.helpers import bcrypt
from src.models import User

users = Blueprint('users', __name__)
api = Api(users)

user_parser = reqparse.RequestParser()
user_parser.add_argument('phone', type=str, required=True)
user_parser.add_argument('password', type=str, required=True)


class UsersList(Resource):
    """Users of the system"""
    def get(self):
        """Login"""
        args = user_parser.parse_args()
        real_phone = args['phone'].replace(' ', '+')
        got_user = User.query.filter_by(phone=real_phone).first_or_404()
        if bcrypt.check_password_hash(got_user.password_hash, args['password']):
            access_token = create_access_token(
                got_user.phone, user_claims={'operator': got_user.is_operator})
            return {'token': access_token}
        abort(400)

    def post(self):
        """Create new user"""
        args = user_parser.parse_args()
        password_hash = str(bcrypt.generate_password_hash(args['password']), 'utf-8')
        new_user = User(phone=args['phone'], password_hash=password_hash)
        new_user.save()
        return dict()


api.add_resource(UsersList, '/users')
