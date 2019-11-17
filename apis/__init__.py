from flask import Blueprint, g
from flask_restplus import Api
from werkzeug.exceptions import BadRequest, Unauthorized, Forbidden, NotFound

from apis.session import api as session
from apis.user import api as user
from apis.property import api as property
from apis.analytics import api as analytics
from apis.predictions import api as predictions
from apis.model_trainings import api as model_trainings
from apis.price_rankings import api as price_rankings
from apis.crime_rankings import api as crime_rankings
from apis.ratings_rankings import api as rating_rankings
from apis.unemployment_rankings import api as unemployment_ratings
from tahelka.analytics.recorder import Recorder

blueprint = Blueprint('apiv1', __name__, url_prefix='/api/v1')
api = Api(blueprint)    #TODO Add metadata

api.add_namespace(session)
api.add_namespace(user)
api.add_namespace(property)
api.add_namespace(analytics)
api.add_namespace(predictions)
api.add_namespace(model_trainings)
api.add_namespace(price_rankings)
api.add_namespace(unemployment_ratings)
api.add_namespace(rating_rankings)
api.add_namespace(crime_rankings)

@api.errorhandler(BadRequest)
def handle_bad_request(error):
    # Analytics
    status_code = 400
    Recorder(None, 'bad_request', status_code).recordUsage()

    response = {"message": "The request parameters are invalid."}
    return response, status_code

@api.errorhandler(NotFound)
def handle_not_found(error):
    # Analytics
    status_code = 404
    Recorder(None, 'not_found_error', status_code).recordUsage()

    response = {"message": "Resource not found."}
    return response, status_code

@api.errorhandler(Unauthorized)
def handle_unauthorized(error):
    print(g)
    # Analytics
    status_code = 401
    Recorder(None, 'unauthorized_error', status_code).recordUsage()

    response = {"message": "The provided credentials or token is incorrect."}
    return response, status_code

@api.errorhandler(Forbidden)
def handle_forbidden(error):
    # Analytics
    status_code = 403
    Recorder(None, 'forbidden_error', status_code).recordUsage()

    response = {
        "message": "You don't have permission to access this resource."
    }
    return response, status_code
