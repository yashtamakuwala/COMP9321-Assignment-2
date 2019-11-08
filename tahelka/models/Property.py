from sqlalchemy import Column, Integer, String
from tahelka.models.Base import Base

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True)
    zip_code = Column(Integer)
    property_type = Column(String)
    room_type = Column(String)
    guest_count = Column(Integer)
    bed_count = Column(Integer)
    price_range = Column(String)

    def __init__(self, id=None, zip_code, property_type, room_type,
                 guests_count, bed_count, price_range):
        self.id = id
        self.zip_code = zip_code
        self.property_type = property_type
        self.room_type = room_type
        self.guest_count = guests_count
        self.bed_count = bed_count
        self.price_range = price_range
