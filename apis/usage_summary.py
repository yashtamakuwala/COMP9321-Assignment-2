from alchemy import Session
from flask import Blueprint, request
from flask_restplus import Namespace, fields, Resource
from tahelka.models.Usage import Usage
from tahelka.auth.token_authenticator import TokenAuthenticator
from tahelka.analytics.date_converter import DateConverter
from tahelka.analytics.summarizer import Summarizer
from tahelka.analytics.recorder import Recorder

api = Namespace('API Usage Summary', path='/usage_summary',
                description='Summary of recorded usage of the API')

@api.route('')
class UsageSummary(Resource):
    description='''\
    Shows a summary of the recorded usage of the API with specified query parameters.
    The user could specify the date interval of the records to be considered.
    This endpoint is also able to show a summary of the API usage by a particular user.<br />
    The summary includes:
    - The total count of usage of the API
    - The usage counts of different endpoints
    - Counts of different HTTP response status codes given by the service
    '''
    @api.doc(description=description)
    @api.param('start_date', type=str, description='Only consider records starting from this date (Y-m-d)', format='date')
    @api.param('end_date', type=str, description='Only consider records ending on this date. (Y-m-d)', format='date')
    @api.param('user_id', type=int, description='Only consider usage by this user ID.')
    @api.response(200, "API usage summary has been successfully shown.")
    @api.response(401, "The JWT provided is incorrect or expired.")
    @api.response(403, "You are not authorized to access this resource.")
    def get(self):
        '''
        Shows a summary of the recorded usage of the API
        '''
        auth_header = request.headers.get('Authorization')
        TokenAuthenticator(auth_header, True).authenticate()

        start_date_string = request.args.get('start_date')
        end_date_string = request.args.get('end_date')
        user_id = request.args.get('user_id')

        start_date = DateConverter(start_date_string).convert()
        end_date = DateConverter(end_date_string).convert()

        summarizer = Summarizer(user_id=user_id, start_date=start_date,
                                end_date=end_date)
        summary = summarizer.summarize()

        status_code = 200
        record = Recorder('usage_summary', status_code)
        record.recordUsage()

        return summary, status_code
