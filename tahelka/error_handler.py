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

def handle_forbidden(exception):
    # Analytics here

    response_dict = {
        'message': "Insufficient authorization to access the resource."
    }
    return jsonify(response_dict), 403

def handle_not_found(exception):
    # Analytics here

    response_dict = {
        'message': "Resource not found."
    }
    return jsonify(response_dict), 404

def handle_internal_server_error(exception):
    # Analytics here

    response_dict = {
        'message': "Internal server error."
    }
    return jsonify(response_dict), 500