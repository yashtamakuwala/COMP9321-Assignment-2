from flask import jsonify

def handle_unauthorized(exception):
    # Analytics here
    
    response_dict = {
        'message': "The credentials are incorrect."
    }
    return jsonify(response_dict), 401
