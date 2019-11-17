from flask import Blueprint, request, g
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
    @api.doc(description="Login")
    @api.expect(session)
    @api.response(201, "Login successful.")
    @api.response(401, "The credentials are incorrect.")
    def post(self):
        email = request.json['email']
        password = request.json['password']
        authenticator = CredentialsAuthenticator(email, password)
        user, token = authenticator.authenticate()

        # Analytics here
        status_code = 201
        record = Recorder('login', status_code)
        record.recordUsage()

        response = {
            'message': 'Login successful.',
            'email': user.email,
            'is_admin': user.is_admin,
            'token': token
        }

        return response, status_code
