from flask import Blueprint, request, g
from flask_restplus import Namespace, fields, Resource
from tahelka.auth.credentials_authenticator import CredentialsAuthenticator
from tahelka.analytics.recorder import Recorder
from tahelka.analytics.summarizer import Summarizer


api = Namespace('tokens')

credential = api.model('Credential', {
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})

@api.route('')
class Tokens(Resource):
    @api.doc(security=[], description="Login")
    @api.expect(credential)
    @api.response(201, "Login successful. Token sucessfully created.")
    @api.response(401, "The credentials provided are incorrect.")
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
            'message': 'Login successful. Token is successfully created.',
            'email': user.email,
            'is_admin': user.is_admin,
            'token': token
        }

        return response, status_code
