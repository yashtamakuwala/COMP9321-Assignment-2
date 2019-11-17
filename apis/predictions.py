from flask import Blueprint, request
from flask_restplus import Namespace, fields, Resource
from tahelka.ml.predictor import Predictor
from tahelka.analytics.recorder import Recorder
from werkzeug.exceptions import NotFound, BadRequest
from tahelka.auth.token_authenticator import TokenAuthenticator

api = Namespace('predictions')

@api.route('')
class Predictions(Resource):
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
