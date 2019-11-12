class Summarizer:
    def __init__(self, date_start=None, date_end=None, user_id=None):
        self.date_start = date_start
        self.date_end = date_end
        self.user_id = user_id

    def summarize(self):
        return {"summary": "the summary"}
