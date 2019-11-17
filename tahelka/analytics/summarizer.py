from alchemy import Session
from sqlalchemy import func
from tahelka.models.Usage import Usage
from tahelka.models.User import User
from datetime import timedelta

class Summarizer:
    def __init__(self, start_date=None, end_date=None, user_id=None):
        self.session = Session()
        self.start_date = start_date
        self.end_date = end_date
        self.user_id = user_id

    def summarize(self):
        summary = {'total': self.get_total()}

        action_groups = self.get_action_groups()
        per_action_count = {}
        for action_group, count in action_groups:
            per_action_count[action_group] = count

        status_groups = self.get_status_groups()
        status_code_count = {}
        for status_group, count in status_groups:
            status_code_count[status_group] = count

        summary['actions'] = per_action_count
        summary['status_codes'] = status_code_count

        print(summary)
        return summary

    def get_total(self):
        query = self.session.query(Usage)
        if self.start_date is not None:
            query = query.filter(Usage.used_at >= self.start_date)
        if self.end_date is not None:
            tomorrow = self.end_date + timedelta(days=1)
            query = query.filter(Usage.used_at < tomorrow)
        if self.user_id is not None:
            query = query.filter(Usage.user_id == self.user_id)

        return query.count()

    def get_action_groups(self):
        query = self.session.query(Usage.action, func.count(Usage.action))

        if self.start_date is not None:
            query = query.filter(Usage.used_at >= self.start_date)
        if self.end_date is not None:
            tomorrow = self.end_date + timedelta(days=1)
            query = query.filter(Usage.used_at < tomorrow)
        if self.user_id is not None:
            query = query.filter(Usage.user_id == self.user_id)

        return query.group_by(Usage.action).all()

    def get_status_groups(self):
        query = self.session.query(Usage.status_code, func.count(Usage.status_code))

        if self.start_date is not None:
            query = query.filter(Usage.used_at >= self.start_date)
        if self.end_date is not None:
            tomorrow = self.end_date + timedelta(days=1)
            query = query.filter(Usage.used_at < tomorrow)
        if self.user_id is not None:
            query = query.filter(Usage.user_id == self.user_id)

        return query.group_by(Usage.status_code).all()