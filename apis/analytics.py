from alchemy import Session
from flask import Blueprint, request
from flask_restplus import Namespace, fields, Resource
from tahelka.models.Usage import Usage
from tahelka.auth.token_authenticator import TokenAuthenticator

api = Namespace('analytics')

analytics_model = api.model('Analytics',{
    'start_date' : fields.DateTime,
    "end_date": fields.DateTime,
    "user_id" : fields.String
})

@api.route('')
class Analytics(Resource):
    @api.expect(analytics_model)
    def get(self):

        auth_header = request.headers.get('Authorization')
        user_id = TokenAuthenticator(auth_header, True).authenticate()
        
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        user_id = request.args.get('user_id')

        # TODO: call all usages

        respJson = {'data': True}
        return respJson, 200