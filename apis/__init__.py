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

description = '''\
A RESTful service to help people to settle in the Sydney area.
This service uses machine learning techniques to learn patterns from these datasets:
- Airbnb property listings around Sydney
- Monthly crime offences per local government areas since 1995
- Monthly unemployment rate per local government areas since 2010

Based on these datasets, the service predicts rent price of a property based on some of its attributes.
The attributes are room type, property type, number of beds, and number of people it can accommodates, monthly average crime offences, and monthly unemployment rate.
The users specify local government area, property type, room type, number of beds, and number of guests, then this service will predict the rent price of a property with those specifications.

Besides that, the service also gives rankings of local government areas around Sydney based on some metrics.
These metrics are average per-night rent price, average airbnb tenants rating, monthly average number of crime offences, and monthly average unemployment rate.
These rankings could help the user in deciding which local government area it wants to settle in.
\
'''

api = Api(
    blueprint,
    authorizations=authorizations,
    version='1.0',
    title='Tahelka Service API',
    description=description,
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

    response = {
        "message": "The provided credentials or token is incorrect or expired."
    }
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
