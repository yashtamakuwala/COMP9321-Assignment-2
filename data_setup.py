from scripts import clean_crime
from scripts import clean_unemployment
from scripts import clean_lga
from scripts import clean_listing
from scripts import dump_to_db

from alchemy import Session
from tahelka.models.User import User
from tahelka.auth.hash_generator import HashGenerator
from tahelka.ml.trainer import Trainer

def createAdmin():
    session = Session()
    password = 'admin'
    hashed_password = HashGenerator(password).generate()
    admin = User('admin','admin','admin', hashed_password, True)

    session.add(admin)
    session.commit()

createAdmin()
Trainer().train()
