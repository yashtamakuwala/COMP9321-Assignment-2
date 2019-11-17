from alchemy import Session
from sqlalchemy import func
from tahelka.models.Usage import Usage

class Summarizer:
    def __init__(self, date_start, date_end, user_id):
        self.date_start = date_start
        self.date_end = date_end
        self.user_id = user_id

    def summarize(self):
        session = Session()

        if self.date_start == None and self.date_end == None and self.user_id == None:
            records = session.query(Usage).count()
            per_action = session.query(Usage).group_by(Usage.action).count()
            # per_action = session.query(Usage., func.count(Table.column)).group_by(Table.column).all()
            print(records)
            print(per_action)
        elif self.date_start and self.date_end == None and self.user_id == None:
            records = session.query(Usage).filter(Usage.used_at >= self.date_start).count()
            print(records)
        elif self.date_start == None and self.date_end and self.user_id == None:
            records = session.query(Usage).filter(Usage.used_at <= self.date_end).count()

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
            records = session.query(Usage).filter(Usage.used_at <= self.date_end).filter(Usage.user_id == self.user_id).count()
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

        # return summary

# total: count
# per-action: count
# per-status_code

# Usages
# id user_id, action,
