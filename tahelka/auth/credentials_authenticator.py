from alchemy import Session
from flask import current_app
from tahelka.auth.hash_matcher import HashMatcher
from tahelka.auth.token_generator import TokenGenerator
from tahelka.models.User import User
from werkzeug.exceptions import Unauthorized

class CredentialsAuthenticator:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def authenticate(self):
        user = self.find_user()
        if user is None:
            raise Unauthorized

        matcher = HashMatcher(self.password, user.password)
        if not matcher.is_matched():
            raise Unauthorized

        return TokenGenerator(user).generate()

    def find_user(self):
        session = Session()
        return session.query(User).filter(User.email == self.email).first()
