from alchemy import Session
from flask import Blueprint, request
from flask_restplus import Namespace, fields, Resource
from werkzeug.exceptions import NotFound, BadRequest
from tahelka.auth.token_authenticator import TokenAuthenticator
from tahelka.insight.rating_ranker import RatingRanker
from tahelka.analytics.recorder import Recorder
from tahelka.util.util import check_limit

api = Namespace('Local Areas by Tenant Rating', path='/local_government_areas/rating_ranking',
                description='Ranking local government areas by average rating given by Airbnb tenants')

@api.route('')
class RatingRanking(Resource):
    description='''\
    Ranks local government areas around Sydney by ratings given by Airbnb tenants\
    of the properties in the area.
    The average ratings are calculated by grouping the properties in the \
    Airbnb dataset by its local government area and averaging all the average \
    rating given by Airbnb tenants of the properties in each of the local \
    government areas.
    The user could specify the number of local government areas to be shown.
    The user could also specify the sorting of the ranking (ascending/descending).
    '''
    @api.doc(description=description)
    @api.param('limit', type=int, description='Limit the results to this amount.', default=5)
    @api.param('order', type=str, description='The order of the ranking.', default='descending', enum=['ascending', 'descending'])
    @api.response(200, "LGA rating ranking has been successfully shown.")
    @api.response(400, "The query parameters specified are invalid.")
    @api.response(401, "The JWT provided is incorrect or expired.")
    def get(self):
        '''
        Shows ranking of local government areas around Sydney by average ratings given by Airbnb tenants
        '''
        auth_header = request.headers.get('Authorization')
        TokenAuthenticator(auth_header, False).authenticate()

        limit = request.args.get('limit', 5)
        order = str(request.args.get('order', 'descending'))

        order = order == "ascending"    #order is true for ascending, false otherwise

        limit = check_limit(limit)

        data = RatingRanker(limit, order).rank()


        status_code = 200
        record = Recorder('rating_ranking', status_code)
        record.recordUsage()

        resp = {'data' : data }
        return resp, status_code
