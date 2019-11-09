from flask import current_app
import jwt
import time

class TokenGenerator:
    def __init__(self, user):
        self.user = user

    def generate(self):
        payload = self.construct_payload()
        secret = current_app.config['JWT_SECRET']
        return jwt.encode(payload, secret, algorithm='HS256').decode()

    def construct_payload(self):
        payload = {
            'id': self.user.id,
            'expired_at': TokenGenerator.decide_expire_time()
        }

        if self.user.is_admin:
            payload['is_admin'] = True

        return payload

    def decide_expire_time():
        # Expire in 24 hours
        return int(time.time()) + (60 * 60 * 24)
