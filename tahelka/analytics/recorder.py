from tahelka.models.Usage import Usage
from alchemy import Session
from flask import g, request

class Recorder:
    def __init__(self, action, status_code):
        self.ip_address = request.remote_addr
        self.action = action
        self.status_code = status_code

    def recordUsage(self):
        session = Session()
        new_usage = Usage(self.get_user_id(), request.remote_addr, self.action, self.status_code)
        session.add(new_usage)
        session.commit()

    def get_user_id(self):
        if hasattr(g, 'user_id'):
            return g.user_id
        else:
            return None

