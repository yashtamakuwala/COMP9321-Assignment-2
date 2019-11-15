from flask import Blueprint
from flask_restplus import Api
from werkzeug.exceptions import BadRequest, Unauthorized, Forbidden, NotFound

from apis.session import api as session
from apis.user import api as user
from apis.property import api as property
from apis.analytics import api as analytics
from apis.predictions import api as predictions
from apis.model_trainings import api as model_trainings

blueprint = Blueprint('apiv1', __name__, url_prefix='/api/v1')
api = Api(blueprint)    #TODO Add metadata

api.add_namespace(session)
api.add_namespace(user)
api.add_namespace(property)
api.add_namespace(analytics)
api.add_namespace(predictions)
api.add_namespace(model_trainings)

@api.errorhandler(BadRequest)
def handle_bad_request(error):
    # Analytics

    response = {"message": "The request parameters are invalid."}
    return response, 400

@api.errorhandler(NotFound)
def handle_not_found(error):
    # Analytics

    response = {"message": "Resource not found."}
    return response, 404

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
