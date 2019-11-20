from alchemy import Session
from flask import Blueprint, request, g
from flask_restplus import Namespace, fields, Resource
from tahelka.auth.hash_generator import HashGenerator
from tahelka.models.User import User
from werkzeug.exceptions import BadRequest
from tahelka.analytics.recorder import Recorder

api = Namespace('Registration', path='/users',
                description='New user registration')

user = api.model('User', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password that will be used by the user when logging in to the service')
})

@api.route('')
class Users(Resource):
    description = '''\
    Creates a new user.
    Accepts the first name, last name, email, and password of a new user.
    Rejects email that has been registered before.
    Hashes the password using bcrypt.
    Saves the new user attributes and the hashed password to the database.\
    '''
    @api.doc(security=[], description=description)
    @api.expect(user)
    @api.response(201, "Registration successful.")
    @api.response(400, "The parameters submitted are invalid or the provided email has been registered.")
    def post(self):
        '''
        Registers a new user
        '''
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

        response = {'message': 'Registration successful.'}
        return response, 201
