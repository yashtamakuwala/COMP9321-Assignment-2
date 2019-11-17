from flask import Blueprint, request
from flask_restplus import Namespace, fields, Resource
from tahelka.auth.credentials_authenticator import CredentialsAuthenticator
from tahelka.analytics.recorder import Recorder
from tahelka.analytics.summarizer import Summarizer

api = Namespace('sessions')

session = api.model('Session', {
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})

@api.route('')
class Sessions(Resource):
    def post(self):
        email = request.json['email']
        password = request.json['password']
        authenticator = CredentialsAuthenticator(email, password)
        user, token = authenticator.authenticate()

        # Analytics here
        user_id = user.id
        method = request.method
        ip_address = request.remote_addr
        record = Recorder(user_id, ip_address, 'Login', 201)
        record.recordUsage()

        response = {
            'message': 'Login successful.',
            'email': user.email,
            'is_admin': user.is_admin,
            'token': token
        }

        summ = Summarizer()
        summ.summarize()

        return response, 201
