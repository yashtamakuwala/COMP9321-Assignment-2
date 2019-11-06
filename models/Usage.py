from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from models.Base import Base

class Usage(Base):
    __tablename__ = "usages"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    ip_address = Column(String)
    status_code = Column(Integer)
    path = Column(String)
    used_at = Column(DateTime)

    def __init__(self, id, user_id, path, used_at, ip_address, status_code):
        self.id = id
        self.user_id = user_id
        self.path = path
        self.used_at = used_at
        self.ip_address = ip_address
        self.status_code = status_code
