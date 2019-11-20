from flask import Blueprint, request
from flask_restplus import Namespace, fields, Resource
from tahelka.ml.predictor import Predictor
from tahelka.analytics.recorder import Recorder
from werkzeug.exceptions import NotFound, BadRequest
from tahelka.util.util import validate_integer_param
from tahelka.auth.token_authenticator import TokenAuthenticator

api = Namespace('property-price-prediction')

@api.route('')
class PropertyPricePrediction(Resource):
    @api.doc(description="Show price prediction of a property based on the specified attributes.")
    @api.param('lga', type=str, description='The local government area of the property.', required=True)
    @api.param('property_type', type=str, description='The type of the property.', required=True)
    @api.param('room_type', type=str, description="The room type to rent on the property.", required=True)
    @api.param('guest_count', type=int, description="The number of people to be the tenant of the property.", required=True, minimum=0)
    @api.param('bed_count', type=int, description="The number of beds available on the property.", required=True, minimum=0)
    @api.response(200, "Price range prediction done successfully.")
    @api.response(400, "The query parameters specified are invalid.")
    @api.response(401, "The JWT provided is incorrect or expired.")
    def get(self):
        auth_header = request.headers.get('Authorization')
        TokenAuthenticator(auth_header, False).authenticate()

        lga = request.args['lga']
        p_type = request.args['property_type']
        r_type = request.args['room_type']
        g_count = request.args['guest_count']
        b_count = request.args['bed_count']

        g_count = validate_integer_param(g_count)
        b_count = validate_integer_param(b_count)

        p  = Predictor(lga, p_type, r_type, g_count, b_count)
        msg = p.predict()

        status_code = 200
        record = Recorder('property_price_prediction', status_code)
        record.recordUsage()

        return msg, status_code
