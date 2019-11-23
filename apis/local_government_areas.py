from alchemy import Session
from flask import Blueprint, request
from flask_restplus import Namespace, fields, Resource
from werkzeug.exceptions import NotFound, BadRequest
from tahelka.auth.token_authenticator import TokenAuthenticator
from tahelka.insight.price_ranker import PriceRanker
from tahelka.insight.rating_ranker import RatingRanker
from tahelka.insight.crime_ranker import CrimeRanker
from tahelka.insight.unemployment_ranker import UnemploymentRanker
from tahelka.analytics.recorder import Recorder
from tahelka.util.util import check_limit

api = Namespace('Local Government Areas', path='/local_government_areas',
                description='Rankings of local government areas around Sydney by various metrics')

@api.route('/price_ranking')
class PriceRanking(Resource):
    description='''\
    Ranks local government areas around Sydney by average per-night rent price\
    of properties in the area.
    The average rent prices are calculated by grouping the properties in the \
    Airbnb dataset by its local government area and averaging all the rent \
    price of the properties in each of the local government areas.
    The user could specify the number of local government areas to be shown.
    The user could also specify the sorting of the ranking (ascending/descending).
    '''
    @api.doc(description=description)
    @api.param('limit', type=int, description='Limit the results to this amount.', default=5)
    @api.param('order', type=str, description='The order of the ranking.', default='ascending', enum=['ascending', 'descending'])
    @api.response(200, "LGA price ranking has been successfully shown.")
    @api.response(400, "The query parameters specified are invalid.")
    @api.response(401, "The JWT provided is incorrect or expired.")
    def get(self):
        '''
        Shows ranking of local government areas around Sydney by average per-night rent price
        '''
        auth_header = request.headers.get('Authorization')
        TokenAuthenticator(auth_header, False).authenticate()

        limit = request.args.get('limit', 5)
        order = str(request.args.get('order', 'ascending'))

        order = order == "ascending"    #order is true for ascending, false otherwise

        limit = check_limit(limit)

        data = PriceRanker(limit, order).rank()

        status_code = 200
        record = Recorder('price_ranking', status_code)
        record.recordUsage()

        resp = {'data' : data }
        return resp, status_code

@api.route('/rating_ranking')
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

@api.route('/safety_ranking')
class SafetyRanking(Resource):
    description='''\
    Ranks local government areas around Sydney by monthly average \
    number of recorded crime offences.
    The monthly average of number of recorded crime offences are calculated \
    by averaging the sum of counts of all types of crime offences in each month since 1995 for \
    each local government areas.
    The user could specify the number of local government areas to be shown.
    The user could also specify the sorting of the ranking (ascending/descending).
    '''
    @api.doc(description=description)
    @api.param('limit', type=int, description='Limit the results to this amount.', default=5)
    @api.param('order', type=str, description='The order of the ranking.', default='ascending', enum=['ascending', 'descending'])
    @api.response(200, "LGA safety ranking has been successfully shown.")
    @api.response(400, "The query parameters specified are invalid.")
    @api.response(401, "The JWT provided is incorrect or expired.")
    def get(self):
        '''
        Shows ranking of local government areas around Sydney by monthly average number of crime offences
        '''
        auth_header = request.headers.get('Authorization')
        TokenAuthenticator(auth_header, False).authenticate()

        limit = request.args.get('limit', 5)
        order = str(request.args.get('order', 'ascending'))

        order = order == "ascending"    #order is true for ascending, false otherwise

        limit = check_limit(limit)

        data = CrimeRanker(limit, order).rank()

        status_code = 200
        record = Recorder('safety_ranking', status_code)
        record.recordUsage()

        resp = {'data' : data }
        return resp, status_code

@api.route('/unemployment_ranking')
class UnemploymentRanking(Resource):
    description='''\
    Ranks local government areas around Sydney by monthly average unemployment rate.
    The monthly average unemployment rates are calculated by averaging the \
    unemployment rate of each local government areas since 2010.
    The user could specify the number of local government areas to be shown.
    The user could also specify the sorting of the ranking (ascending/descending).
    '''
    @api.doc(description=description)
    @api.param('limit', type=int, description='Limit the results to this amount.', default=5)
    @api.param('order', type=str, description='The order of the ranking.', default='ascending', enum=['ascending', 'descending'])
    @api.response(200, "LGA unemployment rate ranking has been successfully shown.")
    @api.response(400, "The query parameters specified are invalid.")
    @api.response(401, "The JWT provided is incorrect or expired.")
    def get(self):
        '''
        Shows ranking of local government areas around Sydney by monthly average unemployment rate
        '''
        auth_header = request.headers.get('Authorization')
        TokenAuthenticator(auth_header, False).authenticate()

        limit = request.args.get('limit', 5)
        order = str(request.args.get('order', 'ascending'))

        order = order == "ascending"    #order is true for ascending, false otherwise

        limit = check_limit(limit)

        data = UnemploymentRanker(limit, order).rank()


        status_code = 200
        record = Recorder('unemployment_ranking', status_code)
        record.recordUsage()

        resp = {'data' : data }
        return resp, status_code
