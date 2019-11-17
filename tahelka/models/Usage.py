from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from tahelka.models.Base import Base
from datetime import datetime

class Usage(Base):
    __tablename__ = "usages"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    ip_address = Column(String)
    action = Column(String, nullable=False)
    status_code = Column(Integer, nullable=False)
    used_at = Column(DateTime, nullable=False)

    def __init__(self, user_id, ip_address, action, status_code):
        self.user_id = user_id
        self.ip_address = ip_address
        self.action = action
        self.status_code = status_code
        self.used_at = datetime.now()
