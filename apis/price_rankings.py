from alchemy import Session
from flask import Blueprint, request
from flask_restplus import Namespace, fields, Resource
from werkzeug.exceptions import NotFound, BadRequest
from tahelka.auth.token_authenticator import TokenAuthenticator
from tahelka.insight.price_ranker import PriceRanker
from tahelka.analytics.recorder import Recorder

api = Namespace('price_rankings')

@api.route('')
class PriceRankings(Resource):
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

        data = PriceRanker(limit, order).rank()

        status_code = 200
        record = Recorder('price_rankings', status_code)
        record.recordUsage()

        resp = {'data' : data }
        return resp, status_code
