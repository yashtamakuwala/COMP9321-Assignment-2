class Summarizer:
    def __init__(self, date_start=None, date_end=None, user_id=None):
        self.date_start = date_start
        self.date_end = date_end
        self.user_id = user_id
        pass

    def summarize(self):
        summary = {
            "total": 100,
        }

        for action in actions:
            summary[action] = 10

        # for status_code in status_codes:
        #     summary[status_code] =

        return summary

# total: count
# per-action: count
# per-status_code

# Usages
# id user_id, action,
