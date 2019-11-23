from flask import Blueprint, request
from flask_restplus import Namespace, fields, Resource
from tahelka.ml.predictor import Predictor
from tahelka.analytics.recorder import Recorder
from werkzeug.exceptions import NotFound, BadRequest
from tahelka.auth.token_authenticator import TokenAuthenticator

api = Namespace('predictions')
parser = api.parser()
parser.add_argument('lga', type=str, help='The local government area of the property.', required=True)
parser.add_argument('property_type', type=str, help='The type of the property.', required=True)
parser.add_argument('room_type', type=str, help='The room type to rent on the property.', required=True)
parser.add_argument('guest_count', type=str, help='The number of people to be the tenant of the property.', required=True)
parser.add_argument('bed_count', type=str, help='The number of beds available on the property.', required=True)

@api.route('')
class Predictions(Resource):
    @api.doc(description="Prediction based on the inputs.")
    @api.param('lga', description='The local government area of the property.')
    @api.param('property_type', description='The type of the property.')
    @api.param('room_type', description="The room type to rent on the property.")
    @api.param('guest_count', description="The number of people to be the tenant of the property.")
    @api.param('bed_count', description="The number of beds available on the property.")
    @api.expect(parser)
    @api.response(200, "Prediciton done successfully")
    @api.response(401, "The credentials are incorrect.")
    def get(self):
        auth_header = request.headers.get('Authorization')
        TokenAuthenticator(auth_header, False).authenticate()

        lga = request.args['lga']
        p_type = request.args['property_type']
        r_type = request.args['room_type']
        g_count = request.args['guest_count']
        b_count = request.args['bed_count']

        p  = Predictor(lga, p_type, r_type, g_count, b_count)
        msg = p.predict()

        status_code = 200
        record = Recorder('predictions', status_code)
        record.recordUsage()

        return msg, status_code
