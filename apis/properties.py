from alchemy import Session
from flask import Blueprint, request, g
from flask_restplus import Namespace, fields, Resource
from tahelka.models.Property import Property
from tahelka.models.Usage import Usage
from werkzeug.exceptions import NotFound, BadRequest
from tahelka.util.util import is_all_none, validate_integer_param
from tahelka.analytics.recorder import Recorder
from tahelka.auth.token_authenticator import TokenAuthenticator
from sqlalchemy import text

api = Namespace("Properties Dataset", path='/properties',
                description="CRUD operations on the dataset")

property = api.model('Property', {
    'lga' : fields.String(required=True, description='Local government area of the property'),
    'property_type' : fields.String(required=True, description='The type of the property'),
    'room_type' : fields.String(required=True, description='Room type available in the property'),
    'guest_count' : fields.Integer(required=True, description='Number of persons that the property can accommodate'),
    'bed_count' : fields.Integer(required=True, description='Number of beds in the property'),
    'price' : fields.Integer(required=True, description='Per-night rent price of the property'),
})

property_update = api.model('Property Update', {
    'lga' : fields.String(description='Updated local government area of the property'),
    'property_type' : fields.String(description='Updated type of the property'),
    'room_type' : fields.String(description='Updated room type of the property'),
    'guest_count' : fields.Integer(description='Updated number of persons that the property can accommodate'),
    'bed_count' : fields.Integer(description='Updated number of beds in the property'),
    'price' : fields.Integer(description='Updated per-night rent price of the property'),
})

@api.route('')
@api.response(401, "The JWT provided is incorrect or expired.")
@api.response(403, "You are not authorized to access this resource.")
class Properties(Resource):
    get_description='''\
    Shows the list of properties stored in the dataset.
    The user is able to sort and filter the properties based on these attributes:
    - Local government area
    - Property type
    - Room type
    - Bed count
    - Guest count
    The user is also able to specify the order of the sorting (ascending/descending).
    Supports pagination by enabling the user to specify the number of properties \
    shown and the starting index of the list.
    '''
    @api.doc(description=get_description)
    @api.param('start', type=int, description='The list starts at this index.', default=0, minimum=0)
    @api.param('limit', type=int, description='Number of properties to be shown.', default=100, minimum=0)
    @api.param('sort', type=str, description="Sort based on this attribute", enum=['lga', 'property_type', 'room_type', 'guest_count', 'bed_count'])
    @api.param('order', type=str, description="Order of sorting (asc/desc)", default='asc', enum=['asc', 'desc'])
    @api.param('lga', type=str, description="Filter the properties by this Local Government Area.")
    @api.param('property_type', type=str, description="Filter the properties by this property type.")
    @api.param('room_type', type=str, description="Filter the properties by this room type.")
    @api.param('bed_count', type=int, description="Only show properties with this number of beds.", minimum=0)
    @api.param('guest_count', type=int, description="Only show properties with this number of guests", minimum=0)
    @api.response(200, "List of properties has successfully been shown.")
    @api.response(400, "The parameters submitted are invalid.")
    def get(self):
        '''
        Shows list of properties in the dataset.
        '''
        auth_header = request.headers.get('Authorization')
        TokenAuthenticator(auth_header, True).authenticate()

        start = request.args.get('start', 0)
        limit = request.args.get('limit', 100)
        sort = str(request.args.get('sort', ''))
        order = str(request.args.get('order', 'asc'))

        lga = str(request.args.get('lga',''))
        p_type = str(request.args.get('property_type',''))
        r_type = str(request.args.get('room_type',''))
        g_count = request.args.get('guest_count')
        b_count = request.args.get('bed_count')

        property_attributes = [
            'lga',
            'property_type',
            'room_type',
            'bed_count',
            'guest_count',
        ]

        session = Session()
        query = session.query(Property)

        sortText = str()
        if not sort:
            sortText = 'properties.id' + " " + order
        else:
            if sort not in property_attributes:
                raise BadRequest
            if order not in ['asc', 'desc', '']:
                raise BadRequest
            sortText = "properties." + sort + " " + order

        if lga:
            query = query.filter(text("properties.lga = '"+ lga + "'"))
        if p_type :
            query = query.filter(text("properties.property_type = '"+ p_type + "'"))
        if r_type :
            query = query.filter(text("properties.room_type = '"+ r_type + "'"))
        if b_count is not None:
            b_count = validate_integer_param(b_count)
            query = query.filter(text("properties.bed_count = "+ str(b_count)))
        if g_count is not None:
            g_count = validate_integer_param(g_count)
            query = query.filter(text("properties.guest_count = "+ str(g_count)))

        start = validate_integer_param(start)
        limit = validate_integer_param(limit)
        end = start + limit
        records = query.order_by(text(sortText))[start:end]

        respJson = list()
        for record in records:
            record = record.__dict__
            record.pop('_sa_instance_state', None)
            respJson.append(record)

        # Analytics
        status_code = 200
        record = Recorder('property_index', status_code)
        record.recordUsage()

        msg = {'data': respJson}

        return msg, status_code

    post_description='''\
    Creates a new property record to be stored in the dataset.
    These are the attributes of the new property that the user must specify:
    - Local government area
    - Property type
    - Room type
    - Bed count
    - Guest count
    - Per-night rent price
    '''
    @api.doc(description=post_description, body=property)
    @api.response(201, "Property creation successful.")
    def post(self):
        '''
        Creates a new property in the dataset.
        '''
        auth_header = request.headers.get('Authorization')
        TokenAuthenticator(auth_header, True).authenticate()

        lga = request.json['lga']
        p_type = request.json['property_type']
        r_type = request.json['room_type']
        g_count = request.json['guest_count']
        b_count = request.json['bed_count']
        price = request.json['price']

        if is_all_none(lga, price, p_type, g_count, b_count, r_type):
            raise BadRequest

        new_property = Property(lga, p_type, r_type, g_count, b_count, None,
                                price)
        session = Session()
        session.add(new_property)
        session.commit()

        # Analytics
        status_code = 201
        record = Recorder('property_create', status_code)
        record.recordUsage()

        response = {'message' : 'Property Added.'}
        return response, status_code

@api.route('/<int:id>')
@api.param('id','The Property identifier')
@api.response(401, "The JWT provided is incorrect or expired.")
@api.response(403, "You are not authorized to access this resource.")
@api.response(404, "Property with the specified ID does not exist.")
class PropertyResource(Resource):
    get_description='''\
    Show the attributes of a specified property in the dataset.
    The user specifies the property to be shown by giving its ID.
    If a property with the specified ID does not exist or has been deleted, \
    an HTTP 404 response would be given.
    '''
    @api.doc(description=get_description)
    @api.response(200, "Detail of a property has successfully been shown.")
    def get(self, id):
        '''
        Shows detail of a property in the dataset.
        '''
        auth_header = request.headers.get('Authorization')
        TokenAuthenticator(auth_header, True).authenticate()

        session = Session()
        prop = session.query(Property).filter(Property.id == id).first()

        if prop is None:
            raise NotFound

        prop = prop.__dict__
        prop.pop('_sa_instance_state', None)

        # Analytics
        status_code = 200
        record = Recorder('property_show', status_code)
        record.recordUsage()

        return prop, status_code

    patch_description='''\
    Updates some of the attributes of a specified property in the dataset.
    The user specifies the property to be updated by giving its ID.
    If a property with the specified ID does not exist or has been deleted, \
    an HTTP 404 response would be given.
    In the request body, the user specified the attributes to be updated and \
    the corresponding new value.
    Only the specified attributes would be updated.
    Attributes that are not specified would not be changed.
    '''
    @api.doc(description=patch_description, body=property_update)
    @api.response(200, "Property update successful.")
    def patch(self, id):
        '''
        Updates a property in the dataset.
        '''
        auth_header = request.headers.get('Authorization')
        TokenAuthenticator(auth_header, True).authenticate()

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
        if is_all_none(lga, price, p_type, g_count, b_count, r_type):
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
        status_code = 200
        record = Recorder('property_patch', status_code)
        record.recordUsage()

        msg = {'message':'Property '+str(id)+' updated successfully.'}
        return msg, status_code

    delete_description='''\
    Deletes a specified property from the dataset.
    The user specifies the property to be deleted by giving its ID.
    If a property with the specified ID does not exist or has been deleted, \
    an HTTP 404 response would be given.
    '''
    @api.doc(description=delete_description)
    @api.response(200, "Property deletion successful.")
    def delete(self, id):
        '''
        Deletes a property in the dataset.
        '''
        auth_header = request.headers.get('Authorization')
        TokenAuthenticator(auth_header, True).authenticate()

        session = Session()
        prop = session.query(Property).filter(Property.id == id).first()

        # Resource not found
        if prop is None:
            raise NotFound

        session.delete(prop)
        session.commit()

        # Analytics
        status_code = 200
        record = Recorder('property_delete', status_code)
        record.recordUsage()

        msg = {'message':'Property '+str(id)+' deleted successfully.'}
        return msg, status_code

    put_description='''\
    Replaces a specified property in the dataset.
    The user specifies the property to be replaced by giving its ID.
    If a property with the specified ID does not exist or has been deleted,
    an HTTP 404 response would be given.
    In the request body, the user must specify all of the attributes \
    of the replacement property.
    The attributes are:
    - Local government area
    - Property type
    - Room type
    - Bed count
    - Guest count
    - Per-night Rent price
    '''
    @api.doc(description=put_description, body=property)
    @api.response(200, "Property replacement successful.")
    def put(self, id):
        '''
        Replaces a property in the dataset.
        '''
        auth_header = request.headers.get('Authorization')
        TokenAuthenticator(auth_header, True).authenticate()

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
        status_code = 200
        record = Recorder('property_put', status_code)
        record.recordUsage()

        msg = {'message':'Property '+str(id)+' updated successfully.'}
        return msg, status_code
