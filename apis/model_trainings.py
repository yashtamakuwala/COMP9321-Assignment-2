from flask import Blueprint, request
from flask_restplus import Namespace, fields, Resource
from tahelka.models.Usage import Usage
from tahelka.auth.token_authenticator import TokenAuthenticator
<<<<<<< HEAD
from tahelka.ml.trainer import Trainer

=======
from tahelka.analytics.recorder import Recorder
>>>>>>> 8c68da52bbcbfd9c273699dc752732bb0e15acf4

api = Namespace('model_trainings')

@api.route('')
class Training(Resource):
    def post(self):

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
