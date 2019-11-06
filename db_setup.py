from sqlalchemy import create_engine
from models.Base import Base
from models.User import User
from models.Property import Property
from models.Usage import Usage

engine = create_engine('sqlite:///tahelka.db', echo=True)

Base.metadata.create_all(engine)
