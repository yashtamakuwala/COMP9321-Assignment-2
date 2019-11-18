from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch
from faker import Faker
from random import randrange
faker = Faker()

from tahelka.auth.token_generator import TokenGenerator
from tahelka.auth.token_authenticator import TokenAuthenticator
import time
from werkzeug.exceptions import Forbidden, Unauthorized

class TestTokenAuth(TestCase):
    def test_happy_admin(self):
        user = Mock()
        id = randrange(1, 100)
        user.id = id
        user.is_admin = True

        secret = faker.sentence()

        with patch('tahelka.auth.token_generator.current_app') as app:
            app.config = {'JWT_SECRET': secret}

            generator = TokenGenerator(user)
            token = generator.generate()

        with patch('tahelka.auth.token_authenticator.current_app') as app:
            with patch('tahelka.auth.token_authenticator.g') as g:
                app.config = {'JWT_SECRET': secret}

                auth_header = f'Bearer {token}'
                authenticator = TokenAuthenticator(auth_header, True)
                authenticator.authenticate()
                self.assertEqual(g.user_id, id)

    def test_happy_non_admin(self):
        user = Mock()
        id = randrange(1, 100)
        user.id = id
        user.is_admin = False

        secret = faker.sentence()

        with patch('tahelka.auth.token_generator.current_app') as app:
            app.config = {'JWT_SECRET': secret}

            generator = TokenGenerator(user)
            token = generator.generate()

        with patch('tahelka.auth.token_authenticator.current_app') as app:
            with patch('tahelka.auth.token_authenticator.g') as g:
                app.config = {'JWT_SECRET': secret}

                auth_header = f'Bearer {token}'
                authenticator = TokenAuthenticator(auth_header, False)
                authenticator.authenticate()
                self.assertEqual(g.user_id, id)

    def test_forbidden(self):
        user = Mock()
        id = randrange(1, 100)
        user.id = id
        user.is_admin = False

        secret = faker.sentence()

        with patch('tahelka.auth.token_generator.current_app') as app:
            app.config = {'JWT_SECRET': secret}

            generator = TokenGenerator(user)
            token = generator.generate()

        with patch('tahelka.auth.token_authenticator.current_app') as app:
            with patch('tahelka.auth.token_authenticator.g') as g:
                app.config = {'JWT_SECRET': secret}

                auth_header = f'Bearer {token}'
                authenticator = TokenAuthenticator(auth_header, True)
                with self.assertRaises(Forbidden):
                    authenticator.authenticate()
                self.assertEqual(g.user_id, user.id)

    def test_wrong_token(self):
        with patch('tahelka.auth.token_authenticator.current_app') as app:
            with patch('tahelka.auth.token_authenticator.g') as g:
                app.config = {'JWT_SECRET': faker.sentence()}

                auth_header = f'Bearer {faker.sentence()}'
                authenticator = TokenAuthenticator(auth_header, True)
                with self.assertRaises(Unauthorized):
                    authenticator.authenticate()

    def test_expired(self):
        user = Mock()
        id = randrange(1, 100)
        user.id = id
        user.is_admin = False

        secret = faker.sentence()
        expired_time = time.time() + (60 * 60 * 24) + randrange(1, 100)

        with patch('tahelka.auth.token_generator.current_app') as app:
            app.config = {'JWT_SECRET': secret}

            generator = TokenGenerator(user)
            token = generator.generate()

        with patch('tahelka.auth.token_authenticator.current_app') as app:
            app.config = {'JWT_SECRET': secret}
            with patch('tahelka.auth.token_authenticator.g') as g:
                with patch(
                    'tahelka.auth.token_authenticator.time.time'
                ) as mock_time:
                    mock_time.return_value = expired_time

                    auth_header = f'Bearer {token}'
                    authenticator = TokenAuthenticator(auth_header, False)
                    with self.assertRaises(Unauthorized):
                        authenticator.authenticate()
                    self.assertEqual(g.user_id, id)
