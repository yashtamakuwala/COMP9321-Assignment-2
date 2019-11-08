from flask import Blueprint, request
from tahelka.auth.credentials_authenticator import CredentialsAuthenticator
from tahelka.exceptions import BadRequestError

blueprint = Blueprint('session', __name__, url_prefix='/api/v1/sessions')

@api.route('/', methods=['POST'])
def create():
    validate_args()

    email = request.args['email']
    password = requests.args['password']
    authenticator = CredentialsAuthenticator(email, password)
    token = authenticator.authenticate()

    # Analytics here

    response_dict = {
        'message': 'Login successful.',
        'token': token
    }
    return jsonify(response_dict), 200

def validate_args():
    for param in ['email', 'password']:
        if param not in request.args:
            raise BadRequestError

        if not request.args[param]:
            raise BadRequestError
