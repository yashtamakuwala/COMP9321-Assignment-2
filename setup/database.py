from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///tahelka.db', echo=True)
Base = declarative_base()

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    role = Column(Boolean)
    password = Column(String)



class Usage(Base):

    __tablename__ = "usages"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    path = Column(String)
    used_at = Column(DateTime)
    ip_address = Column(String)
    status_code = Column(Integer)


class Property(Base):

    __tablename__ = "properties"

    id = Column(Integer, primary_key=True)
    zip_code = Column(Integer)
    property_type = Column(String)
    room_type = Column(String)
    guest_count = Column(Integer)
    bed_count = Column(Integer)
    price_range = Column(String)

Base.metadata.create_all(engine)





