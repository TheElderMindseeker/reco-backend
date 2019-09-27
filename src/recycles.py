from flask import Blueprint
from flask_restful import Resource, Api

recycles = Blueprint('recycles', __name__)
api = Api(recycles)


class RecyclesList(Resource):
    """List of recycle units"""
    def get(self):
        """Get list of recycle units"""

    def post(self):
        """Create new recycle unit"""
