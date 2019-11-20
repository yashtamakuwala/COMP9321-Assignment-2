from alchemy import Session
from flask import Blueprint, request
from flask_restplus import Namespace, fields, Resource
from tahelka.models.Usage import Usage
from tahelka.auth.token_authenticator import TokenAuthenticator
from tahelka.analytics.date_converter import DateConverter
from tahelka.analytics.summarizer import Summarizer
from tahelka.analytics.recorder import Recorder

api = Namespace('usage-summary')

@api.route('')
class UsageSummary(Resource):
    @api.doc(description="Show list of Stats based on Date and User Id.")
    @api.param('start_date', type=str, description='Only consider usage starting from this date (Y-m-d)', format='date')
    @api.param('end_date', type=str, description='Only consider usage ending on this date. (Y-m-d)', format='date')
    @api.param('user_id', type=int, description='Only consider usage of this user ID.')
    @api.response(200, "API usage summary has been successfully shown.")
    @api.response(401, "The JWT provided is incorrect or expired.")
    @api.response(403, "You are not authorized to access this resource.")
    def get(self):
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
