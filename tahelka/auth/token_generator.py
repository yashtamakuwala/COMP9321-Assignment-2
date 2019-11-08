from flask import current_app
import jwt
import time

class TokenGenerator:
    def __init__(self, user):
        self.user = user

    def generate(self):
        payload = self.construct_payload()
        secret = self.get_secret()
        return jwt.encode(payload, secret, algorithm='HS256').decode()

    def construct_payload(self):
        return {
            'id': self.user.id,
            'role': self.user.role,
            'expire_at': self.decide_expire_time()
        }

    def get_secret(self):
        return current_app.config['JWT_SECRET']

    def decide_expire_time(self):
        # Expire in 24 hours
        return int(time.time()) + (60 * 60 * 24)
