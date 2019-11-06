class Usage(Base):

    def __init__(self, id, user_id, path, used_at, ip_address, status_code):
        self.id = id
        self.user_id = user_id
        self.path = path
        self.used_at = used_at
        self.ip_address = ip_address
        self.status_code = status_code