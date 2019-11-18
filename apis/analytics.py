from alchemy import Session
from flask import Blueprint, request
from flask_restplus import Namespace, fields, Resource
from tahelka.models.Usage import Usage
from tahelka.auth.token_authenticator import TokenAuthenticator
from tahelka.analytics.date_converter import DateConverter
from tahelka.analytics.summarizer import Summarizer
from tahelka.analytics.recorder import Recorder

api = Namespace('analytics')

parser = api.parser()
parser.add_argument('start_date', type=str, help='Show usage summary starting from this date. (Y-m-d)')
parser.add_argument('end_date', type=str, help='Show usage summary ending on this date. (Y-m-d)')
parser.add_argument('user_id', type=str, help='Show usage summary for this user ID.')

@api.route('')
class Analytics(Resource):
    @api.expect(parser)
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
