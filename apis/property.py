from alchemy import Session
from flask import Blueprint, request
from flask_restplus import Namespace, fields, Resource
from tahelka.models.Property import Property
from tahelka.models.Usage import Usage
from werkzeug.exceptions import NotFound, BadRequest
from tahelka.util.util import areFieldsEmpty
from tahelka.analytics.recorder import Recorder
from tahelka.auth.token_authenticator import TokenAuthenticator

api = Namespace('properties')

listing = api.model('Property', {
    'lga' : fields.Integer(required=True),
    'property_type' : fields.String(required=True),
    'room_type' : fields.String(required=True),
    'guest_count' : fields.Integer(required=True),
    'bed_count' : fields.Integer(required=True),
    'price' : fields.Integer(required=True),
})

# TODO: check for user role
@api.route('')
@api.param('start')
@api.param('limit')
class PropertyList(Resource):
    def get(self):
        auth_header = request.headers.get('Authorization')
        user_id = TokenAuthenticator(auth_header, True).authenticate()

        start = int(request.args.get('start', 0))
        limit = int(request.args.get('limit', 100))
        end = start + limit

        session = Session()
        records = session.query(Property).order_by(Property.id)[start:end]

        respJson = list()
        for record in records:
            record = record.__dict__
            record.pop('_sa_instance_state', None)
            respJson.append(record)

        # Analytics
        ip_address = request.remote_addr
        record = Recorder(user_id, ip_address, 'property_index', 200)
        record.recordUsage()

        msg = {'data': respJson}
        return msg, 200

    def post(self):
        auth_header = request.headers.get('Authorization')
        user_id = TokenAuthenticator(auth_header, True).authenticate()

        lga = request.json['lga']
        p_type = request.json['property_type']
        r_type = request.json['room_type']
        g_count = request.json['guest_count']
        b_count = request.json['bed_count']
        price = request.json['price']

        if areFieldsEmpty(lga, price, p_type, g_count, b_count, r_type):
            raise BadRequest

        new_property = Property(lga, p_type, r_type, g_count, b_count, None,
                                price)
        session = Session()
        session.add(new_property)
        session.commit()

        # Analytics
        ip_address = request.remote_addr
        record = Recorder(user_id, ip_address, 'property_create', 201)
        record.recordUsage()

        response = {'message' : 'Property Added.'}
        return response, 201

@api.route('/<int:id>')
class Properties(Resource):
    def get(self, id):
        auth_header = request.headers.get('Authorization')
        user_id = TokenAuthenticator(auth_header, True).authenticate()

        session = Session()
        prop = session.query(Property).filter(Property.id == id).first()

        if prop is None:
            raise NotFound

        prop = prop.__dict__
        prop.pop('_sa_instance_state', None)

        # Analytics
        method = request.method
        ip_address = request.remote_addr
        record = Recorder(user_id, ip_address, 'property_show', 200)
        record.recordUsage()

        return prop, 200

    def patch(self, id):
        auth_header = request.headers.get('Authorization')
        user_id = TokenAuthenticator(auth_header, True).authenticate()

        session = Session()
        prop = session.query(Property).filter(Property.id == id).first()

        # Resource not found
        if prop is None:
            raise NotFound

        lga = request.json.get('lga')
        p_type = request.json.get('property_type')
        r_type = request.json.get('room_type')
        g_count = request.json.get('guest_count')
        b_count = request.json.get('bed_count')
        price = request.json.get('price')

        # Empty request
        if areFieldsEmpty(lga, price, p_type, g_count, b_count, r_type):
            raise BadRequest

        if lga is not None:
            prop.lga = lga

        if p_type is not None:
            prop.property_type = p_type

        if r_type is not None:
            prop.room_type = r_type

        if g_count is not None:
            prop.guest_count = g_count

        if b_count is not None:
            prop.bed_count = b_count

        if price is not None:
            prop.price = price

        session.commit()

        # Analytics
        method = request.method
        ip_address = request.remote_addr
        record = Recorder(user_id, ip_address, 'property_patch', 200)
        record.recordUsage()

        msg = {'message':'Property '+str(id)+' updated successfully.'}
        return msg, 200

    def delete(self, id):
        auth_header = request.headers.get('Authorization')
        user_id = TokenAuthenticator(auth_header, True).authenticate()

        session = Session()
        prop = session.query(Property).filter(Property.id == id).first()

        # Resource not found
        if prop is None:
            raise NotFound

        session.delete(prop)
        session.commit()

        # Analytics
        method = request.method
        ip_address = request.remote_addr
        record = Recorder(user_id, ip_address, 'property_delete', 200)
        record.recordUsage()

        msg = {'message':'Property '+str(id)+' deleted successfully.'}
        return msg, 200

    def put(self, id):
        auth_header = request.headers.get('Authorization')
        user_id = TokenAuthenticator(auth_header, True).authenticate()

        session = Session()
        prop = session.query(Property).filter(Property.id == id).first()

        # Resource not found
        if prop is None:
            raise NotFound

        lga = request.json.get('lga')
        p_type = request.json.get('property_type')
        r_type = request.json.get('room_type')
        g_count = request.json.get('guest_count')
        b_count = request.json.get('bed_count')
        price = request.json.get('price')

        prop.lga = lga
        prop.property_type = p_type
        prop.room_type = r_type
        prop.guest_count = g_count
        prop.bed_count = b_count
        prop.price = price

        session.commit()

        # Analytics
        method = request.method
        ip_address = request.remote_addr
        record = Recorder(user_id, ip_address, 'property_put', 200)
        record.recordUsage()

        msg = {'message':'Property '+str(id)+' updated successfully.'}
        return msg, 200
