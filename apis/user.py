from alchemy import Session
from flask import Blueprint, request, g
from flask_restplus import Namespace, fields, Resource
from tahelka.auth.hash_generator import HashGenerator
from tahelka.models.User import User
from werkzeug.exceptions import BadRequest
from tahelka.analytics.recorder import Recorder

api = Namespace('users')

user = api.model('User', {
    'first_name': fields.String(),
    'last_name': fields.String(),
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})

@api.route('')
class Users(Resource):
    @api.expect(user)
    @api.doc(description="Register User")
    @api.response(201, "Registration successful.")
    def post(self):
        # Get params
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        email = request.json['email']
        password = request.json['password']

        # Check email
        session = Session()
        if session.query(User).filter(User.email == email).first():
            raise BadRequest

        # Create new user
        hashed_password = HashGenerator(password).generate()
        new_user = User(first_name, last_name, email, hashed_password)
        session.add(new_user)
        session.commit()

        # Put the current user id in global
        g.user_id = new_user.id

        # Analytics here
        Recorder("register", 201).recordUsage()

        # method = request.method
        # ip_address = request.remote_addr
        # record = Recorder(None, ip_address, method, 201)
        # record.recordUsage()

        response = {'message': 'Registration successful.'}
        return response, 201
