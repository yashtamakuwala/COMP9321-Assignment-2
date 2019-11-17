from sqlalchemy import Column, Integer, String
from tahelka.models.Base import Base

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True)
    lga = Column(String)
    property_type = Column(String)
    room_type = Column(String)
    guest_count = Column(Integer)
    bed_count = Column(Integer)
    rating = Column(Integer)
    price = Column(Integer)

    def __init__(self, lga, property_type, room_type, guest_count,
                 bed_count, rating, price):
        
        self.lga = lga
        self.property_type = property_type
        self.room_type = room_type
        self.guest_count = guest_count
        self.bed_count = bed_count
        self.rating = rating
        self.price= price
