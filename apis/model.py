from flask import Blueprint, request
from flask_restplus import Namespace, fields, Resource
from tahelka.models.Usage import Usage
from tahelka.auth.token_authenticator import TokenAuthenticator
from tahelka.ml.trainer import Trainer
from tahelka.analytics.recorder import Recorder

api = Namespace('model')

@api.route('')
class Training(Resource):
    def put(self):

        auth_header = request.headers.get('Authorization')
        TokenAuthenticator(auth_header, True).authenticate()

        Trainer().train()

        msg = {
            'msg' : 'Model training initiated.'
        }

        status_code = 200
        record = Recorder('put_model', status_code)
        record.recordUsage()

        return msg, status_code
