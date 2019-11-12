class Summarizer:
    def __init__(self, user_id, ip_address, action, status_code):
        self.user_id = user_id
        self.ip_address = ip_address
        self.action = action
        self.status_code = status_code

    def summarize(self):
        return {"summary": "the summary"}
