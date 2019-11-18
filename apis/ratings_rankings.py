from alchemy import Session
from flask import Blueprint, request
from flask_restplus import Namespace, fields, Resource
from werkzeug.exceptions import NotFound, BadRequest
from tahelka.auth.token_authenticator import TokenAuthenticator
from tahelka.insight.rating_ranker import RatingRanker
from tahelka.analytics.recorder import Recorder

api = Namespace('rating_rankings')
parser = api.parser()
parser.add_argument('limit', type=int, help='Limit the results to this amount.')
parser.add_argument('order', type=str, help='The order of the ranking (ascending/descending).')

@api.route('')
class RatingRankings(Resource):
    @api.expect(parser)
    def get(self):
        auth_header = request.headers.get('Authorization')
        TokenAuthenticator(auth_header, False).authenticate()

        limit = request.args.get('limit', 5)
        order = str(request.args.get('order', 'ascending'))

        order = order == "ascending"    #order is true for ascending, false otherwise

        if limit == "all" :
            limit = -1
        else:
            limit = int(limit)

        data = RatingRanker(limit, order).rank()


        status_code = 200
        record = Recorder('rating_rankings', status_code)
        record.recordUsage()

        resp = {'data' : data }
        return resp, status_code
