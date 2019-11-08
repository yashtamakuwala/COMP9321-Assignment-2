from flask import current_app
import jwt
from jwt.exceptions import InvalidTokenError
from werkzeug.exceptions import Forbidden, Unauthorized

class TokenAuthenticator:
    def __init__(self, token, role):
        self.token = token
        self.role = role

    def authenticate(self):
        # Decode
        payload = self.decode_token()
        TokenAuthenticator.validate_payload(payload)

        # Check expiry
        if TokenAuthenticator.is_expired(payload):
            raise Unauthorized

        # Check role
        if not payload['role'] == self.role:
            raise Forbidden

        return payload['id']

    def decode_token(self):
        secret = current_app.config['JWT_SECRET']
        try:
            payload = jwt.decode(self.token, secret, )
        except(InvalidTokenError):
            raise Unauthorized

        return payload

    def validate_payload(payload):
        for key in ['id', 'role', 'expired_at']:
            if key not in payload:
                raise Unauthorized

    def is_expired(payload):
        return int(time.time()) > int(payload['expired_at'])
