from alchemy import Session
from flask import Blueprint, request
from flask_restplus import Namespace, fields, Resource
from tahelka.models.Property import Property
from werkzeug.exceptions import BadRequest
from pprint import pprint

api = Namespace('properties')

listing = api.model('Property', {
    'zip_code' : fields.Integer(),
    'property_type' : fields.String(), 
    'room_type' : fields.String(), 
    'guest_count' : fields.Integer(), 
    'bed_count' : fields.Integer(), 
    'price_range' : fields.String(), 
})

# TODO: check for user role
@api.route('')
class Properties(Resource):
    def post(self):
        start = request.json['start']
        limit = request.json['limit']

        session = Session()
        records = session.query(Property).order_by(Property.id).all()
        
        for record in records:
            pprint(record.id)

        # return record.__dict__, 200
        return {'Hello':'world'}


@api.route('/add')
class Properties(Resource):
    def post(self):
        zip_code = request.json['zip_code']
        p_type = request.json['property_type']
        r_type = request.json['room_type']
        g_count = request.json['guest_count']
        b_count = request.json['bed_count']
        p_range = request.json['price_range']

        new_property = Property(zip_code, p_type, r_type, g_count, b_count, p_range)
        session = Session()
        session.add(new_property)
        session.commit()

        response = {'message' : 'Property Added.'}
        return response, 201