class Property(Base):

    def __init__(self, id, zip_code, property_type, room_type, guests_count, bed_count):

        self.id = id
        self.zip_code = zip_code
        self.property_type = property_type
        self.room_type = room_type
        self.guest_count = guests_count
        self.bed_count = bed_count


