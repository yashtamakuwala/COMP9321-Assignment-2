from flask import Blueprint, request
from flask_restplus import Namespace, fields, Resource
from tahelka.models.Usage import Usage
from tahelka.auth.token_authenticator import TokenAuthenticator
from tahelka.analytics.recorder import Recorder

api = Namespace('model_trainings')

@api.route('')
class Training(Resource):
    def post(self):

        auth_header = request.headers.get('Authorization')
        TokenAuthenticator(auth_header, True).authenticate()

        # TODO: call function that trains the model in a background thread.
        msg = {
            'msg' : 'Model training initiated.'
        }

        ip_address = request.remote_addr
        status_code = 200
        record = Recorder(ip_address, 'model_training', status_code)
        record.recordUsage()

        return msg, status_code