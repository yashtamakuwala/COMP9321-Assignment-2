from unittest import TestCase
from faker import Faker
faker = Faker()

from tahelka.auth.token_extractor import TokenExtractor
import time
from werkzeug.exceptions import Forbidden, Unauthorized

class TestTokenExtractor(TestCase):
    def test_happy(self):
        token = faker.word()
        auth_header = f'Bearer {token}'

        extractor = TokenExtractor(auth_header)
        self.assertEqual(extractor.extract(), token)

    def test_wrong_header(self):
        extractor = TokenExtractor(faker.sentence())
        with self.assertRaises(Unauthorized):
            extractor.extract()

    def test_not_bearer_header(self):
        token = faker.sentence()
        auth_header = f'{faker.word()} {token}'

        extractor = TokenExtractor(auth_header)
        with self.assertRaises(Unauthorized):
            extractor.extract()
