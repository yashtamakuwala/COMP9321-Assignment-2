from alchemy import Session
from tahelka.exceptions import UnauthorizedError
from tahelka.models import User

class CredentialsAuthenticator:
    def __init__(email, password):
        self.email = email
        self.password = password

    def authenticate(self):
        user = self.find_user()
        if user is None:
            raise UnauthorizedError

        matcher = HashMatcher(self.password, user.password)
        if not matcher.is_matched():
            raise UnauthorizedError

        return 'Token'

    def find_user(self):
        session = Session()
        return session.query.filter(User.email == self.email)
