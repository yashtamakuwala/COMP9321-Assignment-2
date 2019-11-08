from flask import jsonify

def handle_bad_request(exception):
    # Analytics here

    response_dict = {
        'message': "The parameters of the request are invalid."
    }
    return jsonify(response_dict), 400

def handle_unauthorized(exception):
    # Analytics here

    response_dict = {
        'message': "The credentials are incorrect or the token is invalid."
    }
    return jsonify(response_dict), 401
