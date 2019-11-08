from alchemy import Engine
from tahelka.models.Base import Base
from tahelka.models.User import User
from tahelka.models.Property import Property
from tahelka.models.Usage import Usage

Base.metadata.create_all(Engine)
