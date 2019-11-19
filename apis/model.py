from flask import Blueprint, request
from flask_restplus import Namespace, fields, Resource
from tahelka.models.Usage import Usage
from tahelka.auth.token_authenticator import TokenAuthenticator
from tahelka.ml.trainer import Trainer
from tahelka.analytics.recorder import Recorder

api = Namespace('model')

parser = api.parser()
parser.add_argument('Authorization', location="headers",
                    help='Bearer \<JSON Web Token\>', required=True)


@api.route('')
class Training(Resource):
    @api.doc(description="Retraining the model")
    @api.response(200, "The ML Model has been retrained successfully")
    @api.expect(parser)
    def put(self):
        auth_header = request.headers.get('Authorization')
        TokenAuthenticator(auth_header, True).authenticate()

        Trainer().train()

        msg = {
            'message' : 'The ML Model has been retrained successfully.'
        }

        status_code = 200
        record = Recorder('put_model', status_code)
        record.recordUsage()

        return msg, status_code
