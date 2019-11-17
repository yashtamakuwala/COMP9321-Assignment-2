from tahelka.models.Usage import Usage
from alchemy import Session

class Recorder:
    def __init__(self, user_id, ip_address, action, status_code):
        self.user_id = user_id
        self.ip_address = ip_address
        self.action = action
        self.status_code = status_code

    def recordUsage(self):
        session = Session()
        new_usage = Usage(self.user_id, self.ip_address, self.action, self.status_code)
        session.add(new_usage)
        session.commit()