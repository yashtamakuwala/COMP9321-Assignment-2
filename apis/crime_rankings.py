from alchemy import Session
from flask import Blueprint, request
from flask_restplus import Namespace, fields, Resource
from werkzeug.exceptions import NotFound, BadRequest
from tahelka.auth.token_authenticator import TokenAuthenticator
from tahelka.insight.crime_ranker import CrimeRanker

api = Namespace('crime_rankings')

@api.route('')
class Price_Rankings(Resource):
    def get(self):
        
        auth_header = request.headers.get('Authorization')
        user_id = TokenAuthenticator(auth_header, False).authenticate()

        limit = request.args.get('limit', 5)
        order = str(request.args.get('order', 'ascending'))
       
        order = order == "ascending"    #order is true for ascending, false otherwise

        if limit == "all" :
            limit = -1
        else:
            limit = int(limit)

        data = CrimeRanker(limit, order).rank()

        resp = {'data' : data }
        return resp, 200