from flask import current_app
import jwt
from jwt.exceptions import InvalidTokenError
import time
from werkzeug.exceptions import Forbidden, Unauthorized

class TokenAuthenticator:
    def __init__(self, token, must_be_admin):
        self.token = token
        self.must_be_admin = must_be_admin

    def authenticate(self):
        # Decode
        payload = self.decode_token()
        TokenAuthenticator.validate_payload(payload)

        # Check expiry
        if TokenAuthenticator.is_expired(payload):
            raise Unauthorized

        # Check role
        if self.must_be_admin and 'is_admin' not in payload:
            raise Forbidden

        return payload['id']

    def decode_token(self):
        secret = current_app.config['JWT_SECRET']
        try:
            payload = jwt.decode(self.token, secret, algorithms='HS256')
        except(InvalidTokenError):
            raise Unauthorized

        return payload

    def validate_payload(payload):
        for key in ['id', 'expired_at']:
            if key not in payload:
                raise Unauthorized

    def is_expired(payload):
        return int(time.time()) > int(payload['expired_at'])
