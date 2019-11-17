from alchemy import Session
from flask import Blueprint, request
from flask_restplus import Namespace, fields, Resource
from tahelka.models.Usage import Usage
from tahelka.auth.token_authenticator import TokenAuthenticator
from tahelka.analytics.date_converter import DateConverter
from tahelka.analytics.summarizer import Summarizer
from tahelka.analytics.recorder import Recorder

api = Namespace('analytics')

analytics_model = api.model('Analytics',{
    'start_date' : fields.DateTime,
    "end_date": fields.DateTime,
    "user_id" : fields.String
})

@api.route('')
class Analytics(Resource):
    @api.expect(analytics_model)
    def get(self):
        auth_header = request.headers.get('Authorization')
        TokenAuthenticator(auth_header, True).authenticate()
        
        start_date_string = request.args.get('start_date')
        end_date_string = request.args.get('end_date')
        user_id = request.args.get('user_id')

        start_date = DateConverter(start_date_string).convert()
        end_date = DateConverter(end_date_string).convert()

        summary = Summarizer(user_id=user_id, start_date=start_date, end_date=end_date)

        status_code = 200
        record = Recorder('analytics', status_code)
        record.recordUsage()

        return summary, status_code