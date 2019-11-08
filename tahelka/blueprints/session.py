from flask import Blueprint

blueprint = Blueprint(session, __name__, url_prefix='/api/v1/sessions')

@app.route('/')
def create():
    email = response.args['email']
    password = response.args['password']
    authenticator = CredentialsAuthenticator(email, password)
    token = authenticator.authenticate()

    # Analytics here

    response_dict = {
        'message': 'Login successful.'
        'token': token
    }
    return jsonify(response_dict), 200
