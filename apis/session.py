from flask import Blueprint, request
from flask_restplus import Namespace, fields, Resource
from tahelka.auth.credentials_authenticator import CredentialsAuthenticator

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
        token = authenticator.authenticate()

        # Analytics here

        response = {
            'message': 'Login successful.',
            'token': token
        }
        return response, 201
