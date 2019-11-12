class Predictor:
    def __init__(self, zip_code, property_type, room_type, guest_count,
                 bed_count):
        self.zip_code = zip_code
        self.property_type = property_type
        self.room_type = room_type
        self.guest_count = guest_count
        self.bed_count = bed_count

    def predict(self):
        pass
