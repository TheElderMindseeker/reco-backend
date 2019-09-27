from flask import Blueprint, jsonify
from flask_restful import Resource, Api

from src.models import db, Recycle

recycles = Blueprint('recycles', __name__)
api = Api(recycles)


class RecyclesList(Resource):
    """List of recycle units"""
    def get(self):
        """Get list of recycle units"""
        ids = db.session.query(Recycle.id).all()
        return jsonify(ids)


    def post(self):
        """Create new recycle unit"""


api.add_resource(RecyclesList, '/recycles')
