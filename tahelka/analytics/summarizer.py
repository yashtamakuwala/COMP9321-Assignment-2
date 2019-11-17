from alchemy import Session
from sqlalchemy import func
from tahelka.models.Usage import Usage
from tahelka.models.User import User
from datetime import timedelta

class Summarizer:
    def __init__(self, date_start=None, date_end=None, user_id=None):
        self.date_start = date_start
        self.date_end = date_end
        self.user_id = user_id

    def summarize(self):
        self.session = Session()

        summary = {}
        summary['total'] = self.get_total()


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
        if self.date_start is not None:
            query = query.filter(Usage.used_at >= self.date_start)
        if self.date_end is not None:
            tomorrow = self.date_end + timedelta(days=1)
            query = query.filter(Usage.used_at < tomorrow)
        if self.user_id is not None:
            query = query.filter(Usage.user_id == self.user_id)

        return query.count()

    def get_action_groups(self):
        query = self.session.query(Usage.action, func.count(Usage.action))

        if self.date_start is not None:
            query = query.filter(Usage.used_at >= self.date_start)
        if self.date_end is not None:
            tomorrow = self.date_end + timedelta(days=1)
            query = query.filter(Usage.used_at < tomorrow)
        if self.user_id is not None:
            query = query.filter(Usage.user_id == self.user_id)

        return query.group_by(Usage.action).all()

    def get_status_groups(self):
        query = self.session.query(Usage.status_code, func.count(Usage.status_code))

        if self.date_start is not None:
            query = query.filter(Usage.used_at >= self.date_start)
        if self.date_end is not None:
            tomorrow = self.date_end + timedelta(days=1)
            query = query.filter(Usage.used_at < tomorrow)
        if self.user_id is not None:
            query = query.filter(Usage.user_id == self.user_id)

        return query.group_by(Usage.status_code).all()


'''
        if self.date_start == None and self.date_end == None and self.user_id == None:
            records = session.query(Usage).count()
            action_groups = session.query(Usage.action, func.count(Usage.action)).group_by(Usage.action).all()
            # per_action = session.query(Usage., func.count(Table.column)).group_by(Table.column).all()

            summary = {
                'total': records,
            }
            for action, count in action_groups:
                summary[action] = count


            print(summary)
            return summary
        elif self.date_start and self.date_end == None and self.user_id == None:
            query = session.query(Usage)
            if date_start is not None:
                query = query.filter(Usage.used_at >= self.date_start)
            if date_end is not None:
                query = query.filter(Usage.used_at >= self.date_start)
            if
            print(records)
        elif self.date_start == None and self.date_end and self.user_id == None:
            records = session.query(Usage).filter(Usage.used_at < self.date_end).count()

            print(records)
        elif self.date_start == None and self.date_end == None and self.user_id:
            records = session.query(Usage).filter(Usage.user_id == self.user_id).count()
            print(records)
        elif self.date_start and self.date_end and self.user_id == None:
            records = session.query(Usage).filter(Usage.used_at.between(self.date_start, self.date_end)).count()
            print(records)
        elif self.date_start and self.date_end == None and self.user_id:
            records = session.query(Usage).filter(Usage.used_at >= self.date_start).filter(Usage.user_id == self.user_id).count()
            print(records)
        elif self.date_start == None and self.date_end and self.user_id:
            records = session.query(Usage).filter(Usage.used_at < self.date_end).filter(Usage.user_id == self.user_id).count()
            print(records)
        elif self.date_start and self.date_end and self.user_id:
            records = session.query(Usage).filter(Usage.used_at.between(self.date_start, self.date_end)).filter(Usage.user_id == self.user_id).count()
            print(records)


        # summary = {
        #     "total": 100,
        # }
        #
        # for action in actions:
        #     summary[action] = 10

        # for status_code in status_codes:
        #     summary[status_code] =

        # return 
'''

# total: count
# per-action: count
# per-status_code

# Usages
# id user_id, action,
