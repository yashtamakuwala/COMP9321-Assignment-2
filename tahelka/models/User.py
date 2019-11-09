from sqlalchemy import Column, Integer, String
from tahelka.models.Base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, nullable=False, unique=True)
    role = Column(Integer, nullable=False)
    password = Column(String, nullable=False)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.role = 0   #0 for normal user and 1 for Admin user
        self.password = password
