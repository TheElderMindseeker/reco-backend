from flask import Blueprint, jsonify
from flask_restful import Resource, Api, reqparse, fields, marshal_with

from src.models import db, Recycle

recycles = Blueprint('recycles', __name__)
api = Api(recycles)


recycles_parser = reqparse.RequestParser()

recycles_parser.add_argument('name', type=str, required=True)
recycles_parser.add_argument('address', type=str, required=True)
recycles_parser.add_argument('position', type=str, required=True)
recycles_parser.add_argument('open_time', type=str, required=True)
recycles_parser.add_argument('close_time', type=str, required=True)
recycles_parser.add_argument('trash_types', type=str, required=True)
recycles_parser.add_argument('bonus_program', type=bool, required=True)


class RecyclesList(Resource):
    """List of recycle units"""
    def get(self):
        """Get list of recycle units"""
        ids = db.session.query(Recycle.id).all()
        return jsonify(ids)

    def post(self):
        """Create new recycle unit"""
        args = recycles_parser.parse_args()
        new_recycle = Recycle(
            name=args['name'],
            address=args['address'],
            position=args['position'],
            open_time=args['open_time'],
            close_time=args['close_time'],
            trash_types=args['trash_types'],
            bonus_program=args['bonus_program'],
        )
        new_recycle.save()


recycle_fields = {
    'name': fields.String,
    'address': fields.String,
    'position': fields.String,
    'open_time': fields.String,
    'close_time': fields.String,
    'trash_types': fields.String,
    'bonus_program': fields.Boolean,
}


class Recycles(Resource):
    """Individual resources"""
    @marshal_with(recycle_fields)
    def get(self, rec_id):
        """Get recycle info by id"""
        got_recycle = Recycle.query.get(rec_id)
        if not got_recycle:
            return jsonify(errorMessage='Recycle not found'), 404

        return got_recycle

    def put(self, rec_id):
        """Update recycle by id"""
        pass

    def delete(self, rec_id):
        """Delete recycle with specified id"""


api.add_resource(RecyclesList, '/recycles')
api.add_resource(Recycles, '/recycles/<int:rec_id>')
