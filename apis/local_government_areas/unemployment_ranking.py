from alchemy import Session
from flask import Blueprint, request
from flask_restplus import Namespace, fields, Resource
from werkzeug.exceptions import NotFound, BadRequest
from tahelka.auth.token_authenticator import TokenAuthenticator
from tahelka.insight.unemployment_ranker import UnemploymentRanker
from tahelka.analytics.recorder import Recorder
from tahelka.util.util import check_limit

api = Namespace('Local Areas by Unemployment', path='/local_government_areas/unemployment_ranking',
                description='Ranking of local government areas by monthly average unemployment rate')

@api.route('')
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
