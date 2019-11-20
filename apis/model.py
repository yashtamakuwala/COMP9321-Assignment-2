from flask import Blueprint, request
from flask_restplus import Namespace, fields, Resource
from tahelka.models.Usage import Usage
from tahelka.auth.token_authenticator import TokenAuthenticator
from tahelka.ml.trainer import Trainer
from tahelka.analytics.recorder import Recorder

api = Namespace('Model Retraining', path='/model',
                description='Replaces the current machine learning model by retraining a new model')

@api.route('')
class Model(Resource):
    description='''
    Replaces the current machine learning model by retraining a new model.<br />
    No parameters needed to be specified.
    The model will be retrained automatically.
    This endpoint is used to replace the current machine learning model after \
    updating the properties dataset using the CRUD operations provided by \
    this service.
    '''
    @api.doc(description=description)
    @api.response(200, "The ML Model has been retrained successfully.")
    @api.response(401, "The JWT provided is incorrect or expired.")
    @api.response(403, "You are not authorized to access this resource.")
    def put(self):
        auth_header = request.headers.get('Authorization')
        TokenAuthenticator(auth_header, True).authenticate()

        Trainer().train()

        msg = {
            'message' : 'The ML Model has been retrained successfully.'
        }

        status_code = 200
        record = Recorder('train_model', status_code)
        record.recordUsage()

        return msg, status_code
