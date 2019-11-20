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
    @api.param('start_date', type=str, description='Show usage summary starting from this date. (Y-m-d)')
    @api.param('end_date', type=str, description='Show usage summary ending on this date. (Y-m-d)')
    @api.param('user_id', type=int, description='Show usage summary for this user ID.')
    @api.response(200, "Success.")
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
        record = Recorder('analytics', status_code)
        record.recordUsage()

        return summary, status_code
