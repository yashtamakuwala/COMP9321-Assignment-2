from flask import Blueprint, g
from flask_restplus import Api
from werkzeug.exceptions import BadRequest, Unauthorized, Forbidden, NotFound

from apis.tokens import api as tokens
from apis.users import api as users
from apis.properties import api as properties
from apis.usage_summary import api as usage_summary
from apis.property_price_prediction import api as property_price_prediction
from apis.model import api as model
from apis.local_government_areas.price_ranking import api as price_ranking
from apis.local_government_areas.safety_ranking import api as safety_ranking
from apis.local_government_areas.rating_ranking import api as rating_ranking
from apis.local_government_areas.unemployment_ranking import api as unemployment_ranking
from tahelka.analytics.recorder import Recorder

blueprint = Blueprint('apiv1', __name__, url_prefix='/api/v1')

authorizations = {
    'HTTP Bearer Authentication': {
        'type': 'apiKey',
        'name': 'Authorization',
        'in': 'header'
    }
}

api = Api(
    blueprint,
    authorizations=authorizations,
    version='1.0',
    title='Tahelka Service API',
    description='A RESTful service to help people to settle in the Sydney area.',
    security='HTTP Bearer Authentication'
)

api.add_namespace(tokens)
api.add_namespace(users)
api.add_namespace(properties)
api.add_namespace(usage_summary)
api.add_namespace(property_price_prediction)
api.add_namespace(model)
api.add_namespace(price_ranking)
api.add_namespace(safety_ranking)
api.add_namespace(rating_ranking)
api.add_namespace(unemployment_ranking)

@api.errorhandler(BadRequest)
def handle_bad_request(error):
    # Analytics
    status_code = 400
    Recorder('bad_request', status_code).recordUsage()

    response = {"message": "The request parameters are invalid."}
    return response, status_code

@api.errorhandler(NotFound)
def handle_not_found(error):
    # Analytics
    status_code = 404
    Recorder('not_found_error', status_code).recordUsage()

    response = {"message": "Resource not found."}
    return response, status_code

@api.errorhandler(Unauthorized)
def handle_unauthorized(error):
    print(g)
    # Analytics
    status_code = 401
    Recorder('unauthorized_error', status_code).recordUsage()

    response = {"message": "The provided credentials or token is incorrect."}
    return response, status_code

@api.errorhandler(Forbidden)
def handle_forbidden(error):
    # Analytics
    status_code = 403
    Recorder('forbidden_error', status_code).recordUsage()

    response = {
        "message": "You don't have permission to access this resource."
    }
    return response, status_code
