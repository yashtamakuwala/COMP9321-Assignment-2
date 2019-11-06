from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Engine = create_engine('sqlite:///orm.db', echo=True)
Session = sessionmaker(bind=Engine)
