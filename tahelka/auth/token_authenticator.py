from flask import current_app
import jwt
from jwt.exceptions import InvalidTokenError
import time
from werkzeug.exceptions import Forbidden, Unauthorized

from tahelka.auth.token_extractor import TokenExtractor

class TokenAuthenticator:
    def __init__(self, auth_header, must_be_admin):
        self.auth_header = auth_header
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
            payload = jwt.decode(self.extract_token(), secret,
                                 algorithms='HS256')
        except(InvalidTokenError):
            raise Unauthorized

        return payload

    def extract_token(self):
        return TokenExtractor(self.auth_header).extract()

    def validate_payload(self, payload):
        for key in ['id', 'expired_at']:
            if key not in payload:
                raise Unauthorized

    def is_expired(self, payload):
        return int(time.time()) > int(payload['expired_at'])
