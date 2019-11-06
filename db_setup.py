from alchemy import Engine
from models.Base import Base
from models.User import User
from models.Property import Property
from models.Usage import Usage

Base.metadata.create_all(Engine)
