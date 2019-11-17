from flask import Blueprint, request
from flask_restplus import Namespace, fields, Resource
from tahelka.models.Usage import Usage
from tahelka.auth.token_authenticator import TokenAuthenticator
from tahelka.ml.trainer import Trainer


api = Namespace('model_trainings')

@api.route('')
class Training(Resource):
    def post(self):

        auth_header = request.headers.get('Authorization')
        user_id = TokenAuthenticator(auth_header, True).authenticate()

        Trainer().train()

        msg = {
            'msg' : 'Model training initiated.'
        }

        return msg, 200