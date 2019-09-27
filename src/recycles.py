from flask import Blueprint
from flask_restful import Api, Resource

from src.models import Recycle

recycles = Blueprint('recycles', __name__)
api = Api(recycles)


class RecyclesList(Resource):
    """List of recycle units"""
    def get(self):
        """Get list of recycle units"""
    def post(self):
        """Create new recycle unit"""


api.add_resource(RecyclesList, '/recycles')
