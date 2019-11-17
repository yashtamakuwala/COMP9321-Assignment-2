from flask import Blueprint, request
from flask_restplus import Namespace, fields, Resource
from tahelka.ml.predictor import Predictor
from werkzeug.exceptions import NotFound, BadRequest
from tahelka.auth.token_authenticator import TokenAuthenticator

api = Namespace('predictions')

@api.route('')
class PriceRange(Resource):
    def get(self):
        auth_header = request.headers.get('Authorization')
        user_id = TokenAuthenticator(auth_header, False).authenticate()

        lga = request.args['lga']
        p_type = request.args['property_type']
        r_type = request.args['room_type']
        g_count = request.args['guest_count']
        b_count = request.args['bed_count']

        p  = Predictor(lga, p_type, r_type, g_count, b_count)
        msg = p.predict()

        return msg, 200
