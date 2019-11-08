from sqlalchemy import Column, Integer, String
from tahelka.models.Base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    role = Column(String)
    password = Column(String)

    def __init__(self, id, first_name, last_name, email, role, password):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.role = role
        self.password = password
