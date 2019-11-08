from flask import Blueprint
from flask_restplus import Api
from werkzeug.exceptions import BadRequest, Unauthorized, Forbidden

from apis.session import api as session
from apis.user import api as user

blueprint = Blueprint('apiv1', __name__, url_prefix='/api/v1')
api = Api(blueprint)    #TODO Add metadata

api.add_namespace(session)
api.add_namespace(user)

@api.errorhandler(BadRequest)
def handle_bad_request(error):
    # Analytics

    response = {"message": "The request parameters are invalid."}
    return response, 400

@api.errorhandler(Unauthorized)
def handle_unauthorized(error):
    # Analytics

    response = {"message": "The provided credentials or token is incorrect."}
    return response, 401

@api.errorhandler(Forbidden)
def handle_forbidden(error):
    # Analytics

    response = {
        "message": "You don't have permission to access this resource."
    }
    return response, 403
