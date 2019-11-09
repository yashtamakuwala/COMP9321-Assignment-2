from alchemy import Session
from flask import Blueprint, request
from flask_restplus import Namespace, fields, Resource
from tahelka.models.Property import Property
from werkzeug.exceptions import NotFound, BadRequest
from pprint import pprint
from tahelka.util.util import *

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
@api.param('start')
@api.param('limit')
class PropertyList(Resource):
    def get(self):
        start = request.args.get('start')
        limit = request.args.get('limit')

        start = int(start)
        limit = int(limit)

        session = Session()
        records = session.query(Property).order_by(Property.id)[start:limit]
        
        respJson = list()
        for record in records:
            record = record.__dict__
            record.pop('_sa_instance_state', None)
            respJson.append(record)

        msg = {'data':respJson}
        return msg, 200

    def post(self):
        zip_code = request.json['zip_code']
        p_type = request.json['property_type']
        r_type = request.json['room_type']
        g_count = request.json['guest_count']
        b_count = request.json['bed_count']
        p_range = request.json['price_range']

        if areFieldsEmpty(zip_code, p_range, p_type, g_count, b_count, r_type):
            raise BadRequest

        new_property = Property(zip_code, p_type, r_type, g_count, b_count, p_range)
        session = Session()
        session.add(new_property)
        session.commit()

        response = {'message' : 'Property Added.'}
        return response, 201

@api.route('/<int:id>')
class Properties(Resource):
    def get(self, id):

        session = Session()
        prop = session.query(Property).filter(Property.id == id).first()

        if prop is None:
            raise NotFound

        prop = prop.__dict__
        prop.pop('_sa_instance_state', None)

        return prop, 200

    def patch(self, id):
        session = Session()
        prop = session.query(Property).filter(Property.id == id).first()

        # Resource not found
        if prop is None:
            raise NotFound

        zip_code = request.json.get('zip_code', None)
        p_type = request.json.get('property_type', None)
        r_type = request.json.get('room_type', None)
        g_count = request.json.get('guest_count', None)
        b_count = request.json.get('bed_count', None)
        p_range = request.json.get('price_range', None)
        
        # Empty request
        if areFieldsEmpty(zip_code, p_range, p_type, g_count, b_count, r_type):
            raise BadRequest

        if zip_code is not None:
            prop.zip_code = zip_code

        if p_type is not None:
            prop.property_type = p_type
        
        if r_type is not None:
            prop.room_type = r_type

        if g_count is not None:
            prop.guest_count = g_count

        if b_count is not None:
            prop.bed_count = b_count

        if p_range is not None:
            prop.price_range = p_range
        
        session.commit()
        msg = {'message':'Property '+str(id)+' updated successfully.'}
        return msg, 200

    def delete(self, id):
        session = Session()
        prop = session.query(Property).filter(Property.id == id).first()

        # Resource not found
        if prop is None:
            raise NotFound

        session.delete(prop)
        session.commit()
        msg = {'message':'Property '+str(id)+' deleted successfully.'}
        return msg, 200

    def put(self, id):
        session = Session()
        prop = session.query(Property).filter(Property.id == id).first()

        # Resource not found
        if prop is None:
            raise NotFound

        zip_code = request.json.get('zip_code')
        p_type = request.json.get('property_type')
        r_type = request.json.get('room_type')
        g_count = request.json.get('guest_count')
        b_count = request.json.get('bed_count')
        p_range = request.json.get('price_range')

        prop.zip_code = zip_code
        prop.property_type = p_type
        prop.room_type = r_type
        prop.guest_count = g_count
        prop.bed_count = b_count
        prop.price_range = p_range
        
        session.commit()
        msg = {'message':'Property '+str(id)+' updated successfully.'}
        return msg, 200